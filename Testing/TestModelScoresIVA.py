from datasets import load_dataset
from testing import evaluate_models

raw_dataset = load_dataset('cartesinus/iva_mt_wslot', split='test').flatten()
raw_dataset = raw_dataset.select_columns(['translation_utt.en', 'translation_utt.pl'])

en_pl_dataset = raw_dataset.rename_column('translation_utt.en', 'source')
en_pl_dataset = en_pl_dataset.rename_column('translation_utt.pl', 'reference')

pl_en_dataset = raw_dataset.rename_column('translation_utt.pl', 'source')
pl_en_dataset = pl_en_dataset.rename_column('translation_utt.en', 'reference')

evaluate_models(en_pl_dataset, pl_en_dataset, 'results-iva.txt')
