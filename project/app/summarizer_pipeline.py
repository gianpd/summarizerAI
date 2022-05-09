import os
import sys

import spacy
from transformers import AutoTokenizer

nlp = spacy.load('en_core_web_sm')

import logging
logging.basicConfig(stream=sys.stdout, format='%(asctime)-15s %(message)s',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger("Summarizer")

def load_tokenizer(tokenizer_model: str = 'facebook/bart-large-mnli'):
    return AutoTokenizer.from_pretrained(tokenizer_model)


def get_nest_sentences(document: str, tokenizer: AutoTokenizer, token_max_length = 1024):
    """
    Starting from a large document, a list of sequential string is computed, such that each string has
    a number of tokens equal to token_max_length.

    ---Params
    - document: the long text (str)
    - tokenizer: the pre-trained tokenizer to be used.
    - token_max_length: the maximum number of token has required by the NLP model (int)
    """
    sents = []
    length = 0
    doc = nlp(document)
    s = ''
    for sentence in doc.sents:
        tokens_in_sentence = tokenizer(str(sentence), truncation=False, padding=False)[0]
        length += len(tokens_in_sentence) # how many tokens the current sentence have summed to the previous
        if length <= token_max_length:
            s += sentence.text
        else:
            sents.append(s)
            s = sentence.text
            length = 0
    # append last string with less # of tokens than token_max_length
    sents.append(s)
    logger.info(f'Returning {len(sents)} number of chunk strings')
    return sents