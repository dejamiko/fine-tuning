from datasets import load_dataset, concatenate_datasets
from testing import evaluate_models

polish = load_dataset('facebook/flores', 'pol_Latn')
polish_dev = polish['dev'].select_columns(['sentence'])
english = load_dataset('facebook/flores', 'eng_Latn')
english_dev = english['dev'].select_columns(['sentence']).rename_column('sentence', 'reference')
combined_dataset_dev = concatenate_datasets([english_dev, polish_dev], axis=1)

pl_en_dataset_dev = combined_dataset_dev.rename_column('sentence', 'source')

en_pl_dataset_dev = combined_dataset_dev.rename_column('reference', 'source')
en_pl_dataset_dev = en_pl_dataset_dev.rename_column('sentence', 'reference')

evaluate_models(en_pl_dataset_dev, pl_en_dataset_dev, 'results-flores-dev.txt')
