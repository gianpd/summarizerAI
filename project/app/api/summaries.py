import sys
import logging
logging.basicConfig(stream=sys.stdout, format='%(asctime)-15s %(message)s',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger("summaries")

from typing import List

from datetime import datetime, timezone

import time


from fastapi import APIRouter, BackgroundTasks, HTTPException, Path

from app.api import crud
from app.models.tortoise import SummarySchema
from app.summarizer import generate_summary, generate_summary_from_text
from app.models.tortoise import TextSummary

from app.models.pydantic import (  # isort:skip
    SummaryPayloadFromText,
    SummaryFromTextResponseSchema,
    SummaryPayloadSchema,
    SummaryResponseSchema,
    SummaryUpdatePayloadSchema,
)

router = APIRouter()

@router.post("/text", response_model=SummaryFromTextResponseSchema, status_code=201)
async def create_summary_from_text(
    payload: SummaryPayloadFromText) -> SummaryFromTextResponseSchema:

    total_summary = generate_summary_from_text(payload.text)
    response = {"text": payload.text, "summary": total_summary}
    logger.info(f"Returning response: {response}")
    return response



@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(
    payload: SummaryPayloadSchema, background_tasks: BackgroundTasks) -> SummaryResponseSchema:
    logger.info('Creating new summary ...')
    # if payload url is already present do not execute post
    summary_exist = await crud.search_by_url(payload.url)
    if summary_exist:
        created_at = summary_exist['created_at']
        now = datetime.now(timezone.utc)
        delta = now - created_at
        logger.info(f"created at: {created_at}\n now: {now}\n delta: {delta.seconds}")
        if delta.seconds > 3600.0:
            logger.info(f"Too much time from last news summary ...")
        else:
            response = {'url': payload.url, 'id': int(summary_exist['id'])}
            logger.info(f'Summary already present on the DB ---> {response}')
            return response

    summary_id = await crud.post(payload)
    logger.info(f'New summary id {summary_id} created')
    response_object = {"id": summary_id, "url": payload.url}
    logger.info('Calling AI summary inference ...')
    logger.debug(f'Summary id / summary url: {response_object}')
    background_tasks.add_task(generate_summary, summary_id, payload.url)
    return {'url': payload.url, 'id': summary_id}


@router.get("/keyword/{key}/", response_model=List[SummarySchema])
async def read_summary_by_key(key: str) -> List[SummarySchema]:
    logger.info(f'Searching for summary with keyword {key}')
    summary = await crud.search_key(key)
    if not summary:
        raise HTTPException(status_code=404, detail=f"Summary not found with keyword {key}")
    logger.info(f'returning response: {summary}')
    return summary


@router.get("/{id}/", response_model=SummarySchema)
async def read_summary(id: int = Path(..., gt=0)) -> SummarySchema:
    logger.info(f'Trying to get the summary {id}')
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    logger.info(f'returning response: {summary}')
    return summary


@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries() -> List[SummarySchema]:
    return await crud.get_all()


@router.delete("/{id}/", response_model=SummaryResponseSchema)
async def delete_summary(id: int = Path(..., gt=0)) -> SummaryResponseSchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    await crud.delete(id)
    return summary


@router.put("/{id}/", response_model=SummarySchema)
async def update_summary(payload: SummaryUpdatePayloadSchema, id: int = Path(..., gt=0)) -> SummarySchema:
    summary = await crud.put(id, payload)
    if not summary:
        raise HTTPException(status_code=404, detail='Summary not found')
    return summary


