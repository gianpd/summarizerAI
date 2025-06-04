import sys
import json

import time

from newspaper import Article
from transformers import pipeline
from app.models.tortoise import TextSummary
from app.config import get_settings
from app.summarizer_pipeline import get_nest_sentences, load_tokenizer, extractive_summary_pipeline, extractive_summary_lsa

Config = get_settings()
CANDIDATE_LABELS = Config.CANDIDATE_LABELS
KEYWORD_TH = Config.keyword_th

import logging
logging.basicConfig(stream=sys.stdout, format='%(asctime)-15s %(message)s',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger("Summarizer")

from huggingface_hub.inference_api import InferenceApi

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn" 
inference = InferenceApi(repo_id="facebook/bart-large-cnn", token=Config.hf_token)


# headers = {"Authorization": f"Bearer {Config.hf_token}"}
# API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

def download_text(url: str):
    article = Article(url)
    article.download()
    article.parse()
    return article

def get_hf_inference_data_input(article_text):
    payload = {'inputs': article_text, 'parameters': {'do_sample': True}}
    data = json.dumps(payload)
    return data

def retrive_summary(text: str):
    """Get a string and generate its summary by calling the HF API"""
    summaries = []
    text_chunks = get_nest_sentences(text, load_tokenizer())
    for i, str_chunk in enumerate(text_chunks):
        # data = get_hf_inference_data_input(str_chunk)
        # response = requests.request("POST", API_URL, headers=headers, data=data)
        # try:
        #     summary = json.loads(response.content.decode("utf-8"))
        # except json.JSONDecodeError as e:
        #     logger.error(e)
        #     continue
        # summary = summary[0]['summary_text']

        summary = inference(str_chunk)[0]['summary_text']
        logger.info(f'summary {i}: {summary}')
        summaries.append(summary)
    return ''.join(summaries)

def generate_summary_from_text(text: str):
    start = time.time()
    logger.info(f"Generating summary from text: {text}")
    # total_summary = retrive_summary(text)
    # total_summary = extractive_summary_pipeline(text, n_sents=5)
    total_summary = extractive_summary_lsa(text, n_sents=5)
    logger.info(f"*** ELAPSED CREATE SUMMARY FROM TEXT: {time.time() - start} s")
    return total_summary


async def generate_summary(summary_id: int, url: str):
    start = time.time()
    article = download_text(url)
    logger.info(f'Retrived url text: {article.text}')
    # total_summary = retrive_summary(article.text)
    total_summary = extractive_summary_pipeline(article.text)
    logger.info(f"*** ELAPSED CREATE SUMMARY POST: {time.time() - start} s")
    logger.info(f'Total summary: {total_summary}')
    # get top predicted keywords if any
    # top = generate_keys(total_summary)
    # keytop = top[0] if top else ''
    # keys = top[1:] if len(top) > 1 else ''
    # logger.info(f'Retrived top {keytop} and keys {keys}')
    # await TextSummary.filter(id=summary_id).update(summary=total_summary, keyTop=keytop, keywords=keys)
    await TextSummary.filter(id=summary_id).update(summary=total_summary)

def generate_keys(summary: str):
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    preds = classifier(summary, CANDIDATE_LABELS, multi_label=True)
    labels, scores = preds['labels'], preds['scores']
    logger.info(f'Keywords labels predicted: {labels}')
    top5 = labels[:5]
    top = [x for i, x in enumerate(top5) if scores[i] > KEYWORD_TH]
    logger.info(f'Top keywords with score greather than {KEYWORD_TH}: {top}')
    return top if len(top) else ''

