from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl


class SummaryBase(BaseModel):
    url: HttpUrl
    summary: Optional[str] = None
    key_top: Optional[str] = ""
    keywords: Optional[str] = ""


class SummaryCreate(SummaryBase):
    pass


class SummaryUpdate(SummaryBase):
    url: Optional[HttpUrl] = None


class SummaryInDBBase(SummaryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Summary(SummaryInDBBase):
    pass


class SummaryInDB(SummaryInDBBase):
    pass


# Text-only summary schemas
class SummaryFromTextCreate(BaseModel):
    text: str


class SummaryFromTextResponse(BaseModel):
    text: str
    summary: str