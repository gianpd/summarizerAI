from typing import Text
from newspaper import Article
from transformers import pipeline

from app.models.tortoise import TextSummary

async def generate_summary(summary_id: int, url: str) -> None:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    article = Article(url)
    article.download()
    article.parse()
    print(article.text)
    summary = summarizer(article.text, max_length=120, min_length=30, do_sample=False)
    summary = summary[0]['summary_text']
    print(summary)
    await TextSummary.filter(id=summary_id).update(summary=summary)