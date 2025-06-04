# crud API
from typing import List, Text, Union
from app.models.pydantic import SummaryPayloadSchema, SummaryUpdatePayloadSchema
from app.models.tortoise import TextSummary
from tortoise.query_utils import Prefetch


async def post(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(url=payload.url, summary="")
    await summary.save()
    return summary.id


async def get(id: int) -> Union[dict, None]:
    summary = await TextSummary.filter(id=id).first().values()
    if summary:
        return summary
    return None

async def search_key(key: str) -> Union[dict, None]:
    summary = await TextSummary.filter(keyTop=key).all().values()
    if summary:
        return summary
    return None

async def search_by_url(url: str) -> Union[dict, None]:
    summary = await TextSummary.filter(url=url).first().values()
    if summary:
        return summary
    return None


async def get_all() -> List:
    summaries = await TextSummary.all().values()
    return summaries


async def delete(id: int) -> int:
    summary = await TextSummary.filter(id=id).first().delete()
    return summary 


async def put(id: int, payload: SummaryUpdatePayloadSchema) -> Union[dict, None]:
    summary = await TextSummary.filter(id=id).update(url=payload.url, summary=payload.summary)
    if summary:
        updated_summary = await TextSummary.filter(id=id).first().values()
        return updated_summary
    return None

