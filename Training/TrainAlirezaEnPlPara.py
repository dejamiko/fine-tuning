from datasets import load_dataset
from transformers import AutoTokenizer

from training import train_model

DATASET = 'para_crawl'
EPOCH_NUM = 50
max_length = 128
MODEL_NAME = 'alirezamsh/small100'

model_name_cleaned = MODEL_NAME.replace('/', '-') + '-en-pl'

raw_dataset = load_dataset(DATASET, 'enpl')

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, return_tensors='pt', tgt_lang='pl')


# The preprocessing function was adapted from the huggingface example
# https://huggingface.co/docs/transformers/tasks/translation
def tokenize_help(examples):
    inputs = [ex['en'] for ex in examples['translation']]
    targets = [ex['pl'] for ex in examples['translation']]
    model_inputs = tokenizer(
        inputs, text_target=targets, max_length=max_length, truncation=True
    )
    return model_inputs


train_model(raw_dataset, tokenizer, MODEL_NAME, model_name_cleaned, DATASET, EPOCH_NUM, tokenize_help, max_length)
