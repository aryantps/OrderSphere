from typing import List
from pydantic import BaseModel


class ItemSchema(BaseModel):
    productId: str
    boughtQuantity: float
    totalAmount: float

class UserAddressSchema(BaseModel):
    city: str
    country: str
    zipCode: str

class OrderSchema(BaseModel):
    items: List[ItemSchema]
    userAddress: UserAddressSchema

    class Config:
        schema_extra = {
            "example": {
                "items": [
                    {"productId": "product_id_1", "boughtQuantity": 2, "totalAmount": 25.5},
                    {"productId": "product_id_2", "boughtQuantity": 1, "totalAmount": 12.0},
                ],
                "userAddress": {
                    "city": "Example City",
                    "country": "Example Country",
                    "zipCode": "12345"
                }
            }
        }
