import torch
from accelerate import Accelerator
from huggingface_hub import login, get_full_repo_name, Repository
from torch.utils.data.dataloader import DataLoader
from tqdm import tqdm
from transformers import AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer, AdamW, \
    get_scheduler
import evaluate
import numpy as np


# the train function is adapted from the huggingface example https://huggingface.co/docs/transformers/tasks/translation
def train_model(raw_dataset, tokenizer, model_name, model_name_cleaned, dataset_name, epoch_num,
                tokenize_help, max_length, resume_from_checkpoint=False):
    global metric
    login('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')
    split_datasets = raw_dataset['train'].train_test_split(train_size=0.9, seed=20)
    split_datasets['validation'] = split_datasets.pop('test')
    tokenized_datasets = split_datasets.map(
        tokenize_help,
        batched=True,
        remove_columns=split_datasets['train'].column_names,
    )
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
    metric = evaluate.load('sacrebleu')

    dataset_name = dataset_name.replace('/', '-')

    def compute_metrics(eval_preds):
        preds, labels = eval_preds
        # In case the model returns more than the prediction logits
        if isinstance(preds, tuple):
            preds = preds[0]

        decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

        # Replace -100s in the labels as we can't decode them
        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

        # Some simple post-processing
        decoded_preds = [pred.strip() for pred in decoded_preds]
        decoded_labels = [[label.strip()] for label in decoded_labels]

        result = metric.compute(predictions=decoded_preds, references=decoded_labels)
        return {'bleu': result['score']}

    args = Seq2SeqTrainingArguments(
        f'{model_name_cleaned}-{dataset_name}-finetune',
        evaluation_strategy='no',
        save_strategy='epoch',
        learning_rate=2e-5,
        per_device_train_batch_size=32,
        per_device_eval_batch_size=64,
        weight_decay=0.01,
        save_total_limit=2,
        num_train_epochs=epoch_num,
        predict_with_generate=True,
        fp16=True,
        push_to_hub=True,
    )
    trainer = Seq2SeqTrainer(
        model,
        args,
        train_dataset=tokenized_datasets['train'],
        eval_dataset=tokenized_datasets['validation'],
        data_collator=data_collator,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )
    before_training = trainer.evaluate(max_length=max_length)
    file = open(dataset_name + '-' + str(epoch_num) + '-' + model_name_cleaned + '.txt', 'w')
    file.write(str(before_training))
    file.write('\n')
    file.close()

    trainer.train(resume_from_checkpoint=resume_from_checkpoint)
    trainer.push_to_hub()

    after_training = trainer.evaluate(max_length=max_length)
    file = open(dataset_name + '-' + str(epoch_num) + '-' + model_name_cleaned + '.txt', 'a')
    file.write(str(after_training))
    file.close()


# the accelerate function is adapted from the huggingface example
# https://huggingface.co/docs/accelerate/index
def train_accelerate(raw_dataset, tokenizer, model_name, model_name_cleaned, dataset_name, epoch_num,
                     tokenize_help):
    login('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')

    split_datasets = raw_dataset['train'].train_test_split(train_size=0.9, seed=20)

    split_datasets['validation'] = split_datasets.pop('test')

    tokenized_datasets = split_datasets.map(
        tokenize_help,
        batched=True,
        remove_columns=split_datasets['train'].column_names,
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    metric = evaluate.load('sacrebleu')

    dataset_name = dataset_name.replace('/', '-')

    def compute_metrics(eval_preds):
        preds, labels = eval_preds
        # In case the model returns more than the prediction logits
        if isinstance(preds, tuple):
            preds = preds[0]

        decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

        # Replace -100s in the labels as we can't decode them
        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

        # Some simple post-processing
        decoded_preds = [pred.strip() for pred in decoded_preds]
        decoded_labels = [[label.strip()] for label in decoded_labels]

        result = metric.compute(predictions=decoded_preds, references=decoded_labels)
        return {'bleu': result['score']}

    tokenized_datasets.set_format('torch')
    train_dataloader = DataLoader(
        tokenized_datasets['train'],
        shuffle=True,
        collate_fn=data_collator,
        batch_size=8,
    )
    eval_dataloader = DataLoader(
        tokenized_datasets['validation'], collate_fn=data_collator, batch_size=8
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    optimizer = AdamW(model.parameters(), lr=2e-5)

    accelerator = Accelerator()
    model, optimizer, train_dataloader, eval_dataloader = accelerator.prepare(
        model, optimizer, train_dataloader, eval_dataloader
    )

    num_update_steps_per_epoch = len(train_dataloader)
    num_training_steps = epoch_num * num_update_steps_per_epoch

    lr_scheduler = get_scheduler(
        'linear',
        optimizer=optimizer,
        num_warmup_steps=0,
        num_training_steps=num_training_steps,
    )

    model_name = f'{model_name_cleaned}-{dataset_name}-accelerate'
    repo_name = get_full_repo_name(model_name)

    output_dir = f'{model_name_cleaned}-{dataset_name}-accelerate'
    repo = Repository(output_dir, clone_from=repo_name)

    def postprocess(predictions, labels):
        predictions = predictions.cpu().numpy()
        labels = labels.cpu().numpy()

        decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)

        # Replace -100 in the labels as we can't decode them.
        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

        # Some simple post-processing
        decoded_preds = [pred.strip() for pred in decoded_preds]
        decoded_labels = [[label.strip()] for label in decoded_labels]
        return decoded_preds, decoded_labels

    progress_bar = tqdm(range(num_training_steps))

    for epoch in range(epoch_num):
        # Training
        model.train()
        for batch in train_dataloader:
            outputs = model(**batch)
            loss = outputs.loss
            accelerator.backward(loss)

            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()
            progress_bar.update(1)

        # Evaluation
        model.eval()
        for batch in tqdm(eval_dataloader):
            with torch.no_grad():
                generated_tokens = accelerator.unwrap_model(model).generate(
                    batch['input_ids'],
                    attention_mask=batch['attention_mask'],
                    max_length=128,
                )
            labels = batch['labels']

            # Necessary to pad predictions and labels for being gathered
            generated_tokens = accelerator.pad_across_processes(
                generated_tokens, dim=1, pad_index=tokenizer.pad_token_id
            )
            labels = accelerator.pad_across_processes(labels, dim=1, pad_index=-100)

            predictions_gathered = accelerator.gather(generated_tokens)
            labels_gathered = accelerator.gather(labels)

            decoded_preds, decoded_labels = postprocess(predictions_gathered, labels_gathered)
            metric.add_batch(predictions=decoded_preds, references=decoded_labels)

        results = metric.compute()

        print(f"epoch {epoch}, BLEU score: {results['score']:.2f}")
        file = open(dataset_name + '-' + str(epoch_num) + '-' + model_name_cleaned + '.txt', 'a')
        file.write(f"epoch {epoch}, BLEU score: {results['score']:.2f}")
        file.write('\n')
        file.close()

        # Save and upload
        accelerator.wait_for_everyone()
        unwrapped_model = accelerator.unwrap_model(model)
        unwrapped_model.save_pretrained(output_dir, save_function=accelerator.save)
        if accelerator.is_main_process:
            tokenizer.save_pretrained(output_dir)
            repo.push_to_hub(
                commit_message=f'Training in progress epoch {epoch}', blocking=False
            )
