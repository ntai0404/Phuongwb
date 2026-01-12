from pydantic import BaseModel
from typing import List, Any, Optional

class RawSQLRequest(BaseModel):
    query: str
    
class RawSQLResponse(BaseModel):
    success: bool
    rows_affected: Optional[int] = None
    data: Optional[List[dict]] = None
    error: Optional[str] = None
