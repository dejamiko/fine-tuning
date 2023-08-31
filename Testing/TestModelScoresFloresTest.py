from datasets import load_dataset, concatenate_datasets
from testing import evaluate_models

polish = load_dataset('facebook/flores', 'pol_Latn')
polish_test = polish['devtest'].select_columns(['sentence'])
english = load_dataset('facebook/flores', 'eng_Latn')
english_test = english['devtest'].select_columns(['sentence']).rename_column('sentence', 'reference')
combined_dataset_test = concatenate_datasets([english_test, polish_test], axis=1)

pl_en_dataset_test = combined_dataset_test.rename_column('sentence', 'source')

en_pl_dataset_test = combined_dataset_test.rename_column('reference', 'source')
en_pl_dataset_test = en_pl_dataset_test.rename_column('sentence', 'reference')

evaluate_models(en_pl_dataset_test, pl_en_dataset_test, 'results-flores-test.txt')
