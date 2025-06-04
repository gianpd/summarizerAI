import sys
import json
import time
import logging
from typing import List, Dict
from functools import lru_cache
from collections import Counter, namedtuple
from operator import attrgetter

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import nltk
from newspaper import Article
from transformers import pipeline, AutoTokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from app.core.config import settings

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
except:
    pass

# Setup logging
logging.basicConfig(stream=sys.stdout, format='%(asctime)-15s %(message)s',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger("Summarizer")

# Constants
LANGUAGE = "english"
CANDIDATE_LABELS = [
    'literature', 'history', 'cinema',
    'cooking', 'dancing', 'holidays', 
    'finance', 'technology', 'science',
    'politics', 'economy', 'society'
]
KEYWORD_TH = 0.55

# Initialize summarizer components
stemmer = Stemmer(LANGUAGE)
summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)

# Load spacy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("Spacy model 'en_core_web_sm' not found. Please install it with: python -m spacy download en_core_web_sm")
    nlp = None

SentenceInfo = namedtuple("SentenceInfo", ("sentence", "order", "rates",))


@lru_cache
def load_tokenizer(tokenizer_model: str = 'facebook/bart-large-mnli'):
    return AutoTokenizer.from_pretrained(tokenizer_model)


def download_text(url: str) -> Article:
    """Download and parse article from URL"""
    article = Article(url)
    article.download()
    article.parse()
    return article


def get_significant_words_list(doc) -> List[str]:
    """Get a list of important words (PROPN; ADJ; NOUN; VERB) excluding stop words and punctuation"""
    words = []
    stopwords = list(STOP_WORDS)
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in doc:
        if (token.text in stopwords or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            words.append(token.text)
    return words


def get_frequency_words(words: List[str]) -> Counter:
    """Get a counter with the frequency of each word normalized to one"""
    freq_word = Counter(words)
    if not freq_word:
        return freq_word
    max_freq = freq_word.most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word] = (freq_word[word] / max_freq)
    return freq_word


def get_sent_strength(doc, freq_word: Counter) -> Dict:
    """Get sentence importance scores based on word frequencies"""
    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent] += freq_word[word.text]
                else:
                    sent_strength[sent] = freq_word[word.text]
    return sent_strength


def get_extractive_summary(sent_strength: Dict, n_sents: int = 5):
    """Extract top sentences based on importance scores"""
    infos = (SentenceInfo(s, o, sent_strength.get(s)) 
        for o, s in enumerate(sent_strength.keys()))

    infos = sorted(infos, key=attrgetter("rates"), reverse=True)[:n_sents]
    infos = sorted(infos, key=attrgetter("order"))
    logger.info(f"Extracted {len(infos)} sentences ...")
    return tuple(i.sentence.text for i in infos)


def extractive_summary_pipeline(doc: str, n_sents: int = 5) -> str:
    """Generate extractive summary using spacy pipeline"""
    if not nlp:
        return extractive_summary_lsa(doc, n_sents)
    
    doc = nlp(doc)
    logger.info(f"Starting to compute summary from {len(list(doc.sents))} sentences ...")
    words = get_significant_words_list(doc)
    freq_word = get_frequency_words(words)
    sent_strength = get_sent_strength(doc, freq_word)

    summaries = get_extractive_summary(sent_strength, n_sents=n_sents)
    if not summaries:
        return extractive_summary_lsa(doc.text, n_sents)
    
    start_sentence = list(doc.sents)[0].text
    total_summary = ' '.join(summaries)
    if start_sentence in summaries:
        return total_summary
    return start_sentence + ' ' + total_summary


def extractive_summary_lsa(text: str, n_sents: int = 5) -> str:
    """Generate extractive summary using LSA algorithm"""
    try:
        parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
        extractive_summary = ' '.join([sentence._text for sentence in summarizer(parser.document, n_sents)])
        return extractive_summary
    except Exception as e:
        logger.error(f"Error in LSA summarization: {e}")
        # Fallback to simple truncation
        sentences = text.split('.')[:n_sents]
        return '. '.join(sentences) + '.'


def get_nest_sentences(document: str, tokenizer: AutoTokenizer, token_max_length: int = 1024) -> List[str]:
    """Split document into chunks with maximum token length"""
    if not nlp:
        # Simple sentence splitting fallback
        sentences = document.split('.')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            test_chunk = current_chunk + sentence + "."
            tokens = tokenizer(test_chunk, truncation=False, padding=False)['input_ids']
            
            if len(tokens) <= token_max_length:
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence + "."
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    sents = []
    length = 0
    doc = nlp(document)
    s = ''
    for sentence in doc.sents:
        tokens_in_sentence = tokenizer(str(sentence), truncation=False, padding=False)['input_ids']
        length += len(tokens_in_sentence)
        if length <= token_max_length:
            s += sentence.text
        else:
            sents.append(s)
            s = sentence.text
            length = len(tokens_in_sentence)
    
    # Append last string
    if s:
        sents.append(s)
    
    logger.info(f'Returning {len(sents)} number of chunk strings')
    return sents


def generate_summary_from_text(text: str) -> str:
    """Generate summary from plain text"""
    start = time.time()
    logger.info(f"Generating summary from text of length: {len(text)}")
    
    try:
        total_summary = extractive_summary_lsa(text, n_sents=5)
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        # Fallback to simple truncation
        sentences = text.split('.')[:3]
        total_summary = '. '.join(sentences) + '.'
    
    logger.info(f"*** ELAPSED CREATE SUMMARY FROM TEXT: {time.time() - start} s")
    return total_summary


def generate_summary_from_url(url: str) -> str:
    """Generate summary from URL"""
    start = time.time()
    try:
        article = download_text(url)
        logger.info(f'Retrieved url text of length: {len(article.text)}')
        total_summary = extractive_summary_pipeline(article.text)
        logger.info(f"*** ELAPSED CREATE SUMMARY FROM URL: {time.time() - start} s")
        return total_summary
    except Exception as e:
        logger.error(f"Error generating summary from URL {url}: {e}")
        raise


def generate_keywords(summary: str) -> List[str]:
    """Generate keywords from summary using zero-shot classification"""
    try:
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        preds = classifier(summary, CANDIDATE_LABELS, multi_label=True)
        labels, scores = preds['labels'], preds['scores']
        logger.info(f'Keywords labels predicted: {labels}')
        top5 = labels[:5]
        top = [x for i, x in enumerate(top5) if scores[i] > KEYWORD_TH]
        logger.info(f'Top keywords with score greater than {KEYWORD_TH}: {top}')
        return top
    except Exception as e:
        logger.error(f"Error generating keywords: {e}")
        return []