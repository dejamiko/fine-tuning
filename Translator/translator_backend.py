from transformers import pipeline

print("Loading models...")
translator_en_pl = pipeline('translation', tokenizer="alirezamsh/small100",
                            model="MikolajDeja/alirezamsh-small100-en-pl-para_crawl-finetune",
                            src_lang="en", tgt_lang="pl")

translator_pl_en = pipeline("translation", model="MikolajDeja/Helsinki-NLP-opus-mt-pl-en-para_crawl-finetune",
                            tokenizer="Helsinki-NLP/opus-mt-pl-en")

print("Models loaded.")


def translateEnglishToPolish(english_sentence):
    return translator_en_pl(english_sentence.split("\n"))


def translatePolishToEnglish(polish_sentence):
    return translator_pl_en(polish_sentence.split("\n"))
