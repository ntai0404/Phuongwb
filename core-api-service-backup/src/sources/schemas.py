from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class RSSSourceCreate(BaseModel):
    name: str
    url: str
    category: Optional[str] = None

class RSSSourceUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None

class RSSSourceResponse(BaseModel):
    id: int
    name: str
    url: str
    category: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
