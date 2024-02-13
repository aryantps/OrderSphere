from typing import Any
from fastapi import HTTPException

class AppException(HTTPException):
    def __init__(self, status_code: int, detail: Any = None):
        super().__init__(status_code=status_code, detail=detail)
