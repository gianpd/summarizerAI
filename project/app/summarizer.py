import sys
import json
import requests

from typing import Text
from newspaper import Article
# from transformers import pipeline
from app.models.tortoise import TextSummary
from app.models.pydantic import SummaryPayloadSchema
from app.config import get_settings


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
    article = download_text(url)
    data = get_hf_inference_data_input(article.text)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    summary = json.loads(response.content.decode("utf-8"))
    summary = summary[0]['summary_text']
    logger.info(f'Summary: {summary}')
    await TextSummary.filter(id=summary_id).update(summary=summary)



# async def generate_summary(summary_id: int, url: str) -> None:
#     summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#     max_length = 160
#     # newspaper download article
#     article = Article(url)
#     article.download()
#     article.parse()
#     # check length
#     text = article.text
#     length = len(text)
#     logging.info(f'Summarizing text with lenght: {length}')
#     if length > 2800:
#         text = article.text[:2800]
#         max_length = 360
#     logging.info(f'Summarizing text to one with max_length: {max_length}')
#     summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
#     summary = summary[0]['summary_text']
#     await TextSummary.filter(id=summary_id).update(summary=summary)