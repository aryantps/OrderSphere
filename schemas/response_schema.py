
from typing import Any
from typing import Optional
from pydantic import BaseModel


class ResponseModel:
    def __init__(self, data: Any, message: str, status_code : int = 200):
        self.status_code = status_code
        self.data = [data]
        self.message = message


class PaginatedResponse(BaseModel):
    page: int
    limit: int
    nextOffset: Optional[int]
    prevOffset: Optional[int]
    total: int
    data: list[dict]