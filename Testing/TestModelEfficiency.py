import time
from transformers import pipeline
from testing import get_model_params


def time_model(model_name, tokenizer_to_use, source_lang=None, additional_model_data=None):
    second_lang = 'pl' if source_lang == 'en' else 'en'
    if additional_model_data is not None:
        pipeline_to_use = pipeline('translation', tokenizer=tokenizer_to_use, model=model_name, src_lang=source_lang,
                                   tgt_lang=second_lang)
    else:
        pipeline_to_use = pipeline('translation', tokenizer=tokenizer_to_use, model=model_name)

    # time the model for 10 characters, 100 characters, and 300 characters
    times = ''
    for c in [10, 100, 300]:
        # take an average of 10 runs
        runs = []
        for j in range(10):
            text = 'a' * c
            start = time.time()
            pipeline_to_use(text)
            end = time.time()
            runs.append(end - start)
        times += f'{sum(runs) / len(runs):.2f}, '

    print(f'{model_name}: {times}')
    with open('results-efficiency.txt', 'a') as file:
        file.write(f'{model_name}: {times}\n')


params = get_model_params()

for param in params:
    time_model(param['model_name'], param['tokenizer_to_use'], param['source_lang'], param['additional_model_data'])
