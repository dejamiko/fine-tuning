from datasets import load_dataset, concatenate_datasets
from testing import evaluate_models

polish = load_dataset('facebook/flores', 'pol_Latn')
polish_dev = polish['dev'].select_columns(['sentence'])
polish_test = polish['devtest'].select_columns(['sentence'])
english = load_dataset('facebook/flores', 'eng_Latn')
english_dev = english['dev'].select_columns(['sentence']).rename_column('sentence', 'reference')
english_test = english['devtest'].select_columns(['sentence']).rename_column('sentence', 'reference')
combined_dataset_dev = concatenate_datasets([english_dev, polish_dev], axis=1)
combined_dataset_test = concatenate_datasets([english_test, polish_test], axis=1)
combined_dataset = concatenate_datasets([combined_dataset_dev, combined_dataset_test], axis=0)

pl_en_dataset = combined_dataset.rename_column('sentence', 'source')

en_pl_dataset = combined_dataset.rename_column('reference', 'source')
en_pl_dataset = en_pl_dataset.rename_column('sentence', 'reference')

evaluate_models(en_pl_dataset, pl_en_dataset, 'results-flores.txt')
