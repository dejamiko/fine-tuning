# Fine-tuning pre-trained models for English-Polish machine translation

## Structure
This repo contains the code and report of my dissertation as developed for my BSc in Computer Science at King's College London. It achieved a First and a Layton Science Research Award.

The Report.pdf file contains the main body of the report. There is also Appendix.pdf with some additional information.

The code is structured as follows:
- Translator - contains the code for a simple web app that uses the fine-tuned models to translate text
- Training - contains the code for fine-tuning the models
- Testing - contains the code for evaluating the models
- Hyper - contains the code for hyperparameter tuning
- HelperScripts - contains scripts for running the code on the cluster 

## Abstract
Machine translation is a problem known to humanity for many centuries. In the past decades, many advancements were made. Starting with rule-based systems, moving to statistical models trained on vast amounts of data, to neural network approaches. The ease and quality of translation has been improving throughout the years.

This project explores the effectiveness of fine-tuning pre-trained models for English-Polish machine translation. With the increasing popularity of the general language models, the quality of translation that can be achieved by fine-tuning publicly available models can be near state-of-the-art. Another big push in the Machine Translation research community is towards multilingual translation models. However, these models are typically trained on large datasets for a number of language pair and domains, making them less effective for the specific task of English-Polish translation. In this project, a number of multilingual and bilingual pre-trained models were fine-tuned on a number of different datasets. The effectiveness of this approach is evaluated using standard machine translation metrics. The results show that this approach is a viable way of improving the quality of translation for some bilingual models. The quality of translation provided by multilingual models can be significantly improved by fine-tuning, to the point where it is comparable with state-of-the-art models.

