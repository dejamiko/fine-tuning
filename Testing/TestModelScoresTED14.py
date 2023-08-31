from datasets import load_dataset
from testing import evaluate_models

raw_dataset = load_dataset('ted_talks_iwslt', language_pair=('en', 'pl'), year='2014', split='test').flatten()

en_pl_dataset = raw_dataset.rename_column('translation.en', 'source')
en_pl_dataset = en_pl_dataset.rename_column('translation.pl', 'reference')

pl_en_dataset = raw_dataset.rename_column('translation.pl', 'source')
pl_en_dataset = pl_en_dataset.rename_column('translation.en', 'reference')

evaluate_models(en_pl_dataset, pl_en_dataset, 'results-ted-14.txt')
