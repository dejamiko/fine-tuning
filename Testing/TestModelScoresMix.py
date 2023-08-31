from datasets import load_dataset, concatenate_datasets, Dataset
from testing import evaluate_models

kde4 = load_dataset('kde4', lang1='en', lang2='pl', split='train').select(range(100))
kde4 = kde4.flatten().select_columns(['translation.en', 'translation.pl'])
para_crawl = load_dataset('para_crawl', 'enpl', split='train').select(range(1300))
para_crawl = para_crawl.flatten().select_columns(['translation.en', 'translation.pl'])
opus100 = load_dataset('opus100', 'en-pl', split='test').select(range(1300))
opus100 = opus100.flatten().select_columns(['translation.en', 'translation.pl'])
ccmatrix = Dataset.from_list(list(load_dataset('yhavinga/ccmatrix', 'en-pl', split='train', streaming=True).take(1300)))
ccmatrix = ccmatrix.flatten().select_columns(['translation.en', 'translation.pl'])

raw_dataset = concatenate_datasets([kde4, para_crawl, opus100, ccmatrix])

en_pl_dataset = raw_dataset.rename_column('translation.en', 'source')
en_pl_dataset = en_pl_dataset.rename_column('translation.pl', 'reference')

pl_en_dataset = raw_dataset.rename_column('translation.pl', 'source')
pl_en_dataset = pl_en_dataset.rename_column('translation.en', 'reference')

evaluate_models(en_pl_dataset, pl_en_dataset, 'results-mix.txt')
