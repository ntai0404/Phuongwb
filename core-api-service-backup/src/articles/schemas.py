from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RSSSourceBasic(BaseModel):
    id: int
    name: str
    category: Optional[str]
    
    class Config:
        from_attributes = True

class ArticleResponse(BaseModel):
    id: int
    title: str
    link: str
    content: Optional[str]
    published: Optional[str]
    summary: Optional[str]
    image_url: Optional[str]
    source_id: Optional[int]
    source: Optional[RSSSourceBasic]
    fetched_at: datetime
    
    class Config:
        from_attributes = True

class ArticleListParams(BaseModel):
    source_id: Optional[int] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    page: int = 1
    per_page: int = 20

class SavedArticleResponse(BaseModel):
    id: int
    article: ArticleResponse
    saved_at: datetime
    
    class Config:
        from_attributes = True

class ReadingHistoryResponse(BaseModel):
    id: int
    article: ArticleResponse
    read_at: datetime
    
    class Config:
        from_attributes = True
