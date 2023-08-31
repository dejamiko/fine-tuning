from datasets import load_dataset
from transformers import AutoTokenizer

from training import train_accelerate

DATASET = 'opus100'
EPOCH_NUM = 50
max_length = 128
MODEL_NAME = 'gsarti/opus-mt-tc-en-pl'

model_name_cleaned = MODEL_NAME.replace('/', '-')

raw_dataset = load_dataset(DATASET, 'en-pl')

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, return_tensors='pt')


# The preprocessing function was adapted from the huggingface example
# https://huggingface.co/docs/transformers/tasks/translation
def tokenize_help(examples):
    inputs = [ex['en'] for ex in examples['translation']]
    targets = [ex['pl'] for ex in examples['translation']]
    model_inputs = tokenizer(
        inputs, text_target=targets, max_length=max_length, truncation=True
    )
    return model_inputs


train_accelerate(raw_dataset, tokenizer, MODEL_NAME, model_name_cleaned, DATASET, EPOCH_NUM, tokenize_help)
