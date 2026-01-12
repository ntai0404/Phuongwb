from pydantic import BaseModel
from typing import Optional

class CrawlerTriggerRequest(BaseModel):
    source_id: Optional[int] = None  # If None, crawl all sources

class CrawlerScheduleUpdate(BaseModel):
    cron_schedule: str
    is_enabled: bool = True

class CrawlerConfigResponse(BaseModel):
    id: int
    cron_schedule: str
    is_enabled: bool
    
    class Config:
        from_attributes = True
