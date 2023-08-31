from datasets import load_dataset
from testing import evaluate_models

raw_dataset = load_dataset('Helsinki-NLP/tatoeba_mt', 'eng-pol', split='test').select(range(4000))

pl_en_dataset = raw_dataset.rename_column('sourceString', 'reference')
pl_en_dataset = pl_en_dataset.rename_column('targetString', 'source')

en_pl_dataset = raw_dataset.rename_column('targetString', 'reference')
en_pl_dataset = en_pl_dataset.rename_column('sourceString', 'source')

evaluate_models(en_pl_dataset, pl_en_dataset, 'results-tatoeba.txt')
