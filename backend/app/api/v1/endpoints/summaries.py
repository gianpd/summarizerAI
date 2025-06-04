import logging
from typing import List
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, BackgroundTasks, HTTPException, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.crud.crud_summaries import crud_summary
from app.schemas.summary_schema import (
    Summary,
    SummaryCreate,
    SummaryUpdate,
    SummaryFromTextCreate,
    SummaryFromTextResponse
)
from app.core.summarizer import generate_summary_from_text, generate_summary_from_url, generate_keywords

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/text", response_model=SummaryFromTextResponse, status_code=201)
async def create_summary_from_text(
    payload: SummaryFromTextCreate
) -> SummaryFromTextResponse:
    """Generate summary from plain text without storing in database"""
    try:
        total_summary = generate_summary_from_text(payload.text)
        response = {"text": payload.text, "summary": total_summary}
        logger.info(f"Returning response for text summary")
        return response
    except Exception as e:
        logger.error(f"Error creating summary from text: {e}")
        raise HTTPException(status_code=500, detail="Error generating summary")


async def background_generate_summary(summary_id: int, url: str, db: AsyncSession):
    """Background task to generate summary and update database"""
    try:
        summary_text = generate_summary_from_url(url)
        keywords = generate_keywords(summary_text)
        key_top = keywords[0] if keywords else ""
        keywords_str = ", ".join(keywords[1:]) if len(keywords) > 1 else ""
        
        # Get the summary object and update it
        summary_obj = await crud_summary.get(db, id=summary_id)
        if summary_obj:
            update_data = SummaryUpdate(
                url=summary_obj.url,
                summary=summary_text,
                key_top=key_top,
                keywords=keywords_str
            )
            await crud_summary.update(db, db_obj=summary_obj, obj_in=update_data)
            logger.info(f"Updated summary {summary_id} with generated content")
    except Exception as e:
        logger.error(f"Error in background summary generation for {summary_id}: {e}")


@router.post("/", response_model=Summary, status_code=201)
async def create_summary(
    payload: SummaryCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> Summary:
    """Create a new summary from URL"""
    logger.info('Creating new summary ...')
    
    # Check if URL already exists
    existing_summary = await crud_summary.get_by_url(db, url=str(payload.url))
    if existing_summary:
        created_at = existing_summary.created_at
        now = datetime.now(timezone.utc)
        delta = now - created_at
        logger.info(f"created at: {created_at}\n now: {now}\n delta: {delta.total_seconds()}")
        
        # If summary is less than 1 hour old, return existing
        if delta.total_seconds() < 3600.0:
            logger.info(f'Summary already present in DB')
            return existing_summary
    
    # Create new summary entry
    summary = await crud_summary.create(db, obj_in=payload)
    logger.info(f'New summary id {summary.id} created')
    
    # Start background task to generate summary
    logger.info('Starting AI summary inference ...')
    background_tasks.add_task(background_generate_summary, summary.id, str(payload.url), db)
    
    return summary


@router.get("/keyword/{keyword}/", response_model=List[Summary])
async def read_summaries_by_keyword(
    keyword: str,
    db: AsyncSession = Depends(get_db)
) -> List[Summary]:
    """Get summaries by keyword"""
    logger.info(f'Searching for summaries with keyword {keyword}')
    summaries = await crud_summary.search_by_keyword(db, keyword=keyword)
    if not summaries:
        raise HTTPException(status_code=404, detail=f"No summaries found with keyword {keyword}")
    logger.info(f'Found {len(summaries)} summaries')
    return summaries


@router.get("/{summary_id}/", response_model=Summary)
async def read_summary(
    summary_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
) -> Summary:
    """Get summary by ID"""
    logger.info(f'Trying to get summary {summary_id}')
    summary = await crud_summary.get(db, id=summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    logger.info(f'Returning summary {summary_id}')
    return summary


@router.get("/", response_model=List[Summary])
async def read_all_summaries(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> List[Summary]:
    """Get all summaries with pagination"""
    summaries = await crud_summary.get_multi(db, skip=skip, limit=limit)
    return summaries


@router.delete("/{summary_id}/", response_model=Summary)
async def delete_summary(
    summary_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
) -> Summary:
    """Delete summary by ID"""
    summary = await crud_summary.get(db, id=summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    
    deleted_summary = await crud_summary.remove(db, id=summary_id)
    return deleted_summary


@router.put("/{summary_id}/", response_model=Summary)
async def update_summary(
    payload: SummaryUpdate,
    summary_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
) -> Summary:
    """Update summary by ID"""
    summary = await crud_summary.get(db, id=summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail='Summary not found')
    
    updated_summary = await crud_summary.update(db, db_obj=summary, obj_in=payload)
    return updated_summary