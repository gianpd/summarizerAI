from ast import keyword
import sys
import json
import requests

from typing import Text

from newspaper import Article
from transformers import pipeline
from app.api import crud
from app.models.tortoise import TextSummary
from app.models.pydantic import SummaryPayloadSchema
from app.config import get_settings
from app.summarizer_pipeline import get_nest_sentences, load_tokenizer

Config = get_settings()
CANDIDATE_LABELS = Config.CANDIDATE_LABELS

import logging
logging.basicConfig(stream=sys.stdout, format='%(asctime)-15s %(message)s',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger("Summarizer")


headers = {"Authorization": f"Bearer {Config.hf_token}"}
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

def download_text(url: str):
    article = Article(url)
    article.download()
    article.parse()
    return article

def get_hf_inference_data_input(article_text):
    payload = {'inputs': article_text, 'parameters': {'do_sample': False}}
    data = json.dumps(payload)
    return data

async def generate_summary(summary_id: int, url: str):
    summaries = []
    article = download_text(url)
    logger.info(f'Retrived url text: {article.text}')
    # get text chunks where each chunk has 1024 tokens
    text_chunks = get_nest_sentences(article.text, load_tokenizer())
    for i, str_chunk in enumerate(text_chunks):
        data = get_hf_inference_data_input(str_chunk)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        try:
            summary = json.loads(response.content.decode("utf-8"))
        except json.JSONDecodeError as e:
            logger.error(e)
            continue
        summary = summary[0]['summary_text']
        logger.info(f'summary {i}: {summary}')
        summaries.append(summary)
    total_summary = ''.join(summaries)
    logger.info(f'Total summary: {total_summary}')
    # get top predicted keywords if any
    top = generate_keys(total_summary)
    keytop = top[0] if top else ''
    keys = top[1:] if len(top) > 1 else ''
    logger.info(f'Retrived top {keytop} and keys {keys}')
    await TextSummary.filter(id=summary_id).update(summary=total_summary, keyTop=keytop, keywords=keys)

def generate_keys(summary: str):
    th = .55
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    preds = classifier(summary, CANDIDATE_LABELS, multi_label=True)
    labels, scores = preds['labels'], preds['scores']
    logger.info(f'Keywords labels predicted: {labels}')
    top5 = labels[:5]
    top = [x for i, x in enumerate(top5) if scores[i] > th]
    logger.info(f'Top keywords with score greather than {th}: {top}')
    return top if len(top) else ''

