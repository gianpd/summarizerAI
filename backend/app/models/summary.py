from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base


class Summary(Base):
    __tablename__ = "summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    key_top = Column(Text, default="")
    keywords = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())