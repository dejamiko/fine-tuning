from datasets import load_dataset
from transformers import AutoTokenizer
from hyperparamSearch import hyperparameter_search

EPOCH_NUM = 50
max_length = 128

DATASET = 'kde4'
MODEL_NAME = 'Helsinki-NLP/opus-mt-en-mul'

raw_dataset = load_dataset(DATASET, lang1='en', lang2='pl')

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, return_tensors='pt')

model_name_cleaned = MODEL_NAME.replace('/', '-')

# The preprocessing function was adapted from the huggingface example
# https://huggingface.co/docs/transformers/tasks/translation
def tokenize_help(examples):
    inputs = [ex['en'] for ex in examples['translation']]
    targets = [ex['pl'] for ex in examples['translation']]
    model_inputs = tokenizer(
        inputs, text_target=targets, max_length=max_length, truncation=True
    )
    return model_inputs


hyperparameter_search(raw_dataset, tokenizer, MODEL_NAME, model_name_cleaned, DATASET, EPOCH_NUM, tokenize_help)
