from datasets import load_dataset
from testing import evaluate_models

en_pl_dataset = load_dataset('gsarti/wmt_vat', 'wmt20_en_pl', split='test')
pl_en_dataset = load_dataset('gsarti/wmt_vat', 'wmt20_pl_en', split='test')

evaluate_models(en_pl_dataset, pl_en_dataset, 'results-wmt.txt')
