from transformers import pipeline

from testing import get_model_params

sentence_en_to_pl = '''Hello, it's me
I was wondering if after all these years you'd like to meet
To go over everything
They say that time's supposed to heal ya, but I ain't done much healing
Hello, can you hear me?
I'm in California dreaming about who we used to be
When we were younger and free
I've forgotten how it felt before the world fell at our feet
There's such a difference between us
And a million miles
Hello from the other side
I must've called a thousand times
To tell you I'm sorry for everything that I've done
But when I call, you never seem to be home'''.split('\n')

sentence_pl_to_en = '''Ktoś pogasił wszystkie światła
Świat się ugiął od zamieci
I pomimo wielkich chęci
Nie mam dobrych wieści
Chciałoby się uciec
Nie przed wszystkim się da
Idzie zima
Wiem, że nigdy nie jest łatwa
Niesie ciemny dzień przy sobie
Nieruchome myśli w głowie
Żywe są o Tobie
Byle śpiewać było o czym
Serce było wciąż gorące
Znowu krótsze będą noce
Zobaczymy słońce
Chciałoby się uciec
Nie przed wszystkim się da
Chciałoby się uciec
Nie przed wszystkim się da
Idzie zima
Idzie zima'''.split('\n')


def translate(sentence, model_name, tokenizer_to_use, source_lang=None, target_lang=None):
    translator = pipeline('translation', model=model_name, tokenizer=tokenizer_to_use)
    print(model_name)
    if source_lang is not None:
        results = translator(sentence, src_lang=source_lang, tgt_lang=target_lang)
    else:
        results = translator(sentence)
    for index, result in enumerate(results):
        print(result['translation_text'], ' -> ', sentence[index])
        file.write(f"{result['translation_text']} -> {sentence[index]}")


params = get_model_params()

# open file
with open('results-translation.txt', 'w') as file:
    for param in params:
        translate(param['model_name'], param['tokenizer_to_use'], param['source_lang'],
                  param['additional_model_data'])
