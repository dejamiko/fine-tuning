from datasets import load_dataset
from transformers import AutoTokenizer
from hyperparamSearch import hyperparameter_search

EPOCH_NUM = 50
max_length = 128

DATASET = 'para_crawl'
MODEL_NAME = 'alirezamsh/small100'

raw_dataset = load_dataset(DATASET, 'enpl').filter(lambda example, idx: idx % 50 == 0, with_indices=True)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, return_tensors='pt', tgt_lang='en')

model_name_cleaned = MODEL_NAME.replace('/', '-') + 'pl-en'

# The preprocessing function was adapted from the huggingface example
# https://huggingface.co/docs/transformers/tasks/translation
def tokenize_help(examples):
    inputs = [ex['pl'] for ex in examples['translation']]
    targets = [ex['en'] for ex in examples['translation']]
    model_inputs = tokenizer(
        inputs, text_target=targets, max_length=max_length, truncation=True
    )
    return model_inputs


hyperparameter_search(raw_dataset, tokenizer, MODEL_NAME, model_name_cleaned, DATASET, EPOCH_NUM, tokenize_help)
