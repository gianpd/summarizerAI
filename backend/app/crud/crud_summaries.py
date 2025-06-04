from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from app.models.summary import Summary
from app.schemas.summary_schema import SummaryCreate, SummaryUpdate


class CRUDSummary:
    async def create(self, db: AsyncSession, *, obj_in: SummaryCreate) -> Summary:
        db_obj = Summary(
            url=str(obj_in.url),
            summary=obj_in.summary or "",
            key_top=obj_in.key_top or "",
            keywords=obj_in.keywords or ""
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, id: int) -> Optional[Summary]:
        result = await db.execute(select(Summary).where(Summary.id == id))
        return result.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[Summary]:
        result = await db.execute(select(Summary).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_by_url(self, db: AsyncSession, *, url: str) -> Optional[Summary]:
        result = await db.execute(select(Summary).where(Summary.url == url))
        return result.scalar_one_or_none()

    async def search_by_keyword(self, db: AsyncSession, *, keyword: str) -> List[Summary]:
        result = await db.execute(
            select(Summary).where(Summary.keywords.contains(keyword))
        )
        return result.scalars().all()

    async def update(self, db: AsyncSession, *, db_obj: Summary, obj_in: SummaryUpdate) -> Summary:
        update_data = obj_in.model_dump(exclude_unset=True)
        if "url" in update_data:
            update_data["url"] = str(update_data["url"])
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> Optional[Summary]:
        db_obj = await self.get(db, id=id)
        if db_obj:
            await db.execute(delete(Summary).where(Summary.id == id))
            await db.commit()
        return db_obj


crud_summary = CRUDSummary()