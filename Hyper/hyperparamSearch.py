import evaluate
import numpy as np
from transformers import AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer
from huggingface_hub import login


# the beginning of the search function is adapted from the huggingface example
# https://huggingface.co/docs/transformers/tasks/translation
def hyperparameter_search(raw_dataset, tokenizer, model_name, model_name_cleaned, dataset_name, epoch_num,
                          tokenize_help):
    split_dataset = raw_dataset['train'].train_test_split(train_size=0.9, seed=20)

    split_dataset['validation'] = split_dataset.pop('test')

    login('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')

    def init_model(trial):
        return AutoModelForSeq2SeqLM.from_pretrained(model_name)

    global metric
    tokenized_datasets = split_dataset.map(
        tokenize_help,
        batched=True,
        remove_columns=split_dataset['train'].column_names,
    )
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
    metric = evaluate.load('sacrebleu')

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
        save_total_limit=3,
        num_train_epochs=epoch_num,
        predict_with_generate=True,
        fp16=True,
        push_to_hub=True,
    )
    trainer = Seq2SeqTrainer(
        model=None,
        args=args,
        train_dataset=tokenized_datasets['train'],
        eval_dataset=tokenized_datasets['validation'],
        data_collator=data_collator,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
        model_init=init_model,
    )
    best_trial = trainer.hyperparameter_search(
        direction='maximize',
        backend='optuna',
        n_trials=10,
    )
    print(best_trial)
    # save to file
    with open(f'{model_name_cleaned}-{dataset_name}-hyper.txt', 'w') as f:
        f.write(str(best_trial))
