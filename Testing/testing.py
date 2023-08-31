import evaluate
from transformers import pipeline


def evaluate_models(dataset_en_pl, dataset_pl_en, filename):
    model_params = get_model_params()
    for param in model_params:
        evaluate_model(param['model_name'], param['tokenizer_to_use'], filename, dataset_pl_en, dataset_en_pl,
                       param['source_lang'], param['additional_model_data'])


def evaluate_model(model_name, tokenizer_to_use, filename, pl_en_dataset, en_pl_dataset, source_lang=None,
                   additional_model_data=None):
    second_lang = 'pl' if source_lang == 'en' else 'en'
    if source_lang == 'pl':
        dataset = pl_en_dataset
    else:
        dataset = en_pl_dataset
    if additional_model_data is not None:
        pipeline_to_use = pipeline('translation', tokenizer=tokenizer_to_use, model=model_name, src_lang=source_lang,
                                   tgt_lang=second_lang)
    else:
        pipeline_to_use = pipeline('translation', tokenizer=tokenizer_to_use, model=model_name)

    task_evaluator = evaluate.evaluator('translation')

    with open(filename, 'a') as file:
        file.write('Evaluating model: ' + model_name + '\n')
    print('Evaluating model: ' + model_name)

    results = get_results(task_evaluator, pipeline_to_use, dataset)

    with open(filename, 'a') as file:
        file.write('Results ' + str(results['score']) + '\n')
    print('Results ' + str(results['score']))


def get_results(task_evaluator_to_use, pipeline_to_use, dataset_to_use):
    results = task_evaluator_to_use.compute(
        model_or_pipeline=pipeline_to_use,
        data=dataset_to_use,
        input_column='source',
        label_column='reference',
        metric='sacrebleu'
    )

    return results


def get_model_params():
    return [
        {'model_name': 'gsarti/opus-mt-tc-en-pl', 'tokenizer_to_use': 'gsarti/opus-mt-tc-en-pl', 'source_lang': 'en',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/gsarti-opus-mt-tc-en-pl-kde4-finetune',
         'tokenizer_to_use': 'gsarti/opus-mt-tc-en-pl',
         'source_lang': 'en', 'additional_model_data': None},
        {'model_name': 'MikolajDeja/gsarti-opus-mt-tc-en-pl-opus100-finetune',
         'tokenizer_to_use': 'gsarti/opus-mt-tc-en-pl',
         'source_lang': 'en', 'additional_model_data': None},
        {'model_name': 'MikolajDeja/gsarti-opus-mt-tc-en-pl-3-para_crawl-finetune',
         'tokenizer_to_use': 'gsarti/opus-mt-tc-en-pl', 'source_lang': 'en', 'additional_model_data': None},
        {'model_name': 'MikolajDeja/gsarti-opus-mt-tc-en-pl-para_crawl-finetune',
         'tokenizer_to_use': 'gsarti/opus-mt-tc-en-pl', 'source_lang': 'en', 'additional_model_data': None},
        {'model_name': 'MikolajDeja/gsarti-opus-mt-tc-en-pl-yhavinga-ccmatrix-finetune',
         'tokenizer_to_use': 'gsarti/opus-mt-tc-en-pl', 'source_lang': 'en', 'additional_model_data': None},

        {'model_name': 'Helsinki-NLP/opus-mt-pl-en', 'tokenizer_to_use': 'Helsinki-NLP/opus-mt-pl-en',
         'source_lang': 'pl',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/Helsinki-NLP-opus-mt-pl-en-kde4-finetune',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-pl-en', 'source_lang': 'pl',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/Helsinki-NLP-opus-mt-pl-en-opus100-finetune',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-pl-en', 'source_lang': 'pl',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/Helsinki-NLP-opus-mt-pl-en-3-para_crawl-finetune',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-pl-en', 'source_lang': 'pl',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/Helsinki-NLP-opus-mt-pl-en-para_crawl-finetune',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-pl-en', 'source_lang': 'pl',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/Helsinki-NLP-opus-mt-pl-en-yhavinga-ccmatrix-finetune',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-pl-en', 'source_lang': 'pl',
         'additional_model_data': None},

        {'model_name': 'Helsinki-NLP/opus-mt-en-mul',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-en-mul', 'source_lang': 'en',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/Helsinki-NLP-opus-mt-en-mul-kde4-finetune',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-en-mul', 'source_lang': 'en',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/Helsinki-NLP-opus-mt-en-mul-opus100-finetune',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-en-mul', 'source_lang': 'en',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/Helsinki-NLP-opus-mt-en-mul-3-para_crawl-finetune',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-en-mul', 'source_lang': 'en',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/Helsinki-NLP-opus-mt-en-mul-para_crawl-finetune',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-en-mul', 'source_lang': 'en',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/Helsinki-NLP-opus-mt-en-mul-yhavinga-ccmatrix-finetune',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-en-mul', 'source_lang': 'en',
         'additional_model_data': None},

        {'model_name': 'Helsinki-NLP/opus-mt-mul-en',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-mul-en', 'source_lang': 'pl',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/Helsinki-NLP-opus-mt-mul-en-kde4-finetune',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-mul-en', 'source_lang': 'pl',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/Helsinki-NLP-opus-mt-mul-en-opus100-finetune',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-mul-en', 'source_lang': 'pl',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/Helsinki-NLP-opus-mt-mul-en-3-para_crawl-finetune',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-mul-en', 'source_lang': 'pl',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/Helsinki-NLP-opus-mt-mul-en-para_crawl-finetune',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-mul-en', 'source_lang': 'pl',
         'additional_model_data': None},
        {'model_name': 'MikolajDeja/Helsinki-NLP-opus-mt-mul-en-yhavinga-ccmatrix-finetune',
         'tokenizer_to_use': 'Helsinki-NLP/opus-mt-mul-en', 'source_lang': 'pl',
         'additional_model_data': None},

        {'model_name': 'alirezamsh/small100', 'tokenizer_to_use': 'alirezamsh/small100', 'source_lang': 'pl',
         'additional_model_data': 'pl'},
        {'model_name': 'MikolajDeja/alirezamsh-small100-pl-en-kde4-finetune', 'tokenizer_to_use': 'alirezamsh/small100',
         'source_lang': 'pl', 'additional_model_data': 'pl'},
        {'model_name': 'MikolajDeja/alirezamsh-small100-pl-en-opus100-finetune',
         'tokenizer_to_use': 'alirezamsh/small100', 'source_lang': 'pl', 'additional_model_data': 'pl'},
        {'model_name': 'MikolajDeja/alirezamsh-small100-pl-en-3-para_crawl-finetune',
         'tokenizer_to_use': 'alirezamsh/small100', 'source_lang': 'pl', 'additional_model_data': 'pl'},
        {'model_name': 'MikolajDeja/alirezamsh-small100-pl-en-para_crawl-finetune',
         'tokenizer_to_use': 'alirezamsh/small100', 'source_lang': 'pl', 'additional_model_data': 'pl'},
        {'model_name': 'MikolajDeja/alirezamsh-small100-pl-en-yhavinga-ccmatrix-finetune',
         'tokenizer_to_use': 'alirezamsh/small100', 'source_lang': 'pl', 'additional_model_data': 'pl'},

        {'model_name': 'alirezamsh/small100', 'tokenizer_to_use': 'alirezamsh/small100', 'source_lang': 'en',
         'additional_model_data': 'en'},
        {'model_name': 'MikolajDeja/alirezamsh-small100-en-pl-kde4-finetune', 'tokenizer_to_use': 'alirezamsh/small100',
         'source_lang': 'en', 'additional_model_data': 'en'},
        {'model_name': 'MikolajDeja/alirezamsh-small100-en-pl-opus100-finetune',
         'tokenizer_to_use': 'alirezamsh/small100', 'source_lang': 'en', 'additional_model_data': 'en'},
        {'model_name': 'MikolajDeja/alirezamsh-small100-en-pl-3-para_crawl-finetune',
         'tokenizer_to_use': 'alirezamsh/small100', 'source_lang': 'en', 'additional_model_data': 'en'},
        {'model_name': 'MikolajDeja/alirezamsh-small100-en-pl-para_crawl-finetune',
         'tokenizer_to_use': 'alirezamsh/small100', 'source_lang': 'en', 'additional_model_data': 'en'},
        {'model_name': 'MikolajDeja/alirezamsh-small100-en-pl-yhavinga-ccmatrix-finetune',
         'tokenizer_to_use': 'alirezamsh/small100', 'source_lang': 'en', 'additional_model_data': 'en'},

        {'model_name': 'facebook/nllb-200-distilled-600M', 'tokenizer_to_use': 'facebook/nllb-200-distilled-600M',
         'source_lang': 'pl', 'additional_model_data': 'pl'},
        {'model_name': 'MikolajDeja/facebook-nllb-200-distilled-600M-pl-en-opus-finetune',
         'tokenizer_to_use': 'facebook/nllb-200-distilled-600M', 'source_lang': 'pl', 'additional_model_data': 'pl'},
        {'model_name': 'MikolajDeja/facebook-nllb-200-distilled-600M-pl-en-3-para_crawl-finetune',
         'tokenizer_to_use': 'facebook/nllb-200-distilled-600M', 'source_lang': 'pl', 'additional_model_data': 'pl'},
        {'model_name': 'MikolajDeja/facebook-nllb-200-distilled-600M-pl-en-yhavinga-ccmatrix-finetune',
         'tokenizer_to_use': 'facebook/nllb-200-distilled-600M', 'source_lang': 'pl', 'additional_model_data': 'pl'},

        {'model_name': 'facebook/nllb-200-distilled-600M', 'tokenizer_to_use': 'facebook/nllb-200-distilled-600M',
         'source_lang': 'en', 'additional_model_data': 'en'},
        {'model_name': 'MikolajDeja/facebook-nllb-200-distilled-600M-en-pl-opus-finetune',
         'tokenizer_to_use': 'facebook/nllb-200-distilled-600M', 'source_lang': 'en', 'additional_model_data': 'en'},
        {'model_name': 'MikolajDeja/facebook-nllb-200-distilled-600M-en-pl-3-para_crawl-finetune',
         'tokenizer_to_use': 'facebook/nllb-200-distilled-600M', 'source_lang': 'en', 'additional_model_data': 'en'},
        {'model_name': 'MikolajDeja/facebook-nllb-200-distilled-600M-en-pl-yhavinga-ccmatrix-finetune',
         'tokenizer_to_use': 'facebook/nllb-200-distilled-600M', 'source_lang': 'en', 'additional_model_data': 'en'},
    ]
