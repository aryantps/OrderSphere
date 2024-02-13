from typing import Optional
from fastapi import Query, Request
from pydantic import BaseModel, Field


class PaginatedRequest:
    page: int = 1
    limit: int = 10
    min_price: Optional[float]
    max_price: Optional[float]

    def __init__(
        self,
        r: Request,
        page: int = Query(1, description='Page', gt=0),
        limit: int = Query(10, description='Limit', gt=0),
        min_price: Optional[float] = Query(None, description='Minimum price', gt=0),
        max_price: Optional[float] = Query(None, description='Maximum price', gt=0),
    ):
        self.page = page
        self.limit = limit 
        self.min_price = min_price
        self.max_price = max_price


class SearchOrderRequest(BaseModel):
    productId: Optional[str] = Field(None, description="Product ID to filter orders")
    city: Optional[str] = Field(None, description="City to filter orders")
    zipCode: Optional[str] = Field(None, description="ZIP code to filter orders")

    class Config:
        schema_extra = {
            "example": {
                "productId": "product_id_1",
                "city": "Example City",
                "zipCode": "12345"
            }
        }