from datasets import load_dataset
from testing import evaluate_models

raw_dataset = load_dataset('opus_euconst', 'en-pl', split='train').flatten()

en_pl_dataset = raw_dataset.rename_column('translation.en', 'source')
en_pl_dataset = en_pl_dataset.rename_column('translation.pl', 'reference')

pl_en_dataset = raw_dataset.rename_column('translation.pl', 'source')
pl_en_dataset = pl_en_dataset.rename_column('translation.en', 'reference')

evaluate_models(en_pl_dataset, pl_en_dataset, 'results-euconst.txt')
