import sys
import json
import requests

from typing import Text

from newspaper import Article
# from transformers import pipeline
from app.models.tortoise import TextSummary
from app.models.pydantic import SummaryPayloadSchema
from app.config import get_settings
from app.summarizer_pipeline import get_nest_sentences, load_tokenizer

Config = get_settings()

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
    await TextSummary.filter(id=summary_id).update(summary=total_summary)
