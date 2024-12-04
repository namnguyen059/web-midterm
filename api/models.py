import uuid
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

## USER MODEL REGION
##########################################################################

# Address in User model
class Address(BaseModel):
    street: str = Field(...)
    city: str = Field(...)
    zip: Optional[int] = Field(12000)

# User model
class UserModel(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: str = Field(...)
    password: str = Field(...)
    phone: str = Field(...)
    address: Address = Field(...)

    class Config:
        populated_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Don Quixote",
                "password": "securepassword123",
                "phone": "0123456789",
                "address": {
                    "street": "123 Main Street",
                    "city": "Hometown"
                }
            }
        }

##########################################################################







## ORDER MODEL REGION
##########################################################################
# OrderItem
class OrderItem(BaseModel):
    product_id: str = Field(...)
    quantity: int = Field(...)
    total_price: Optional[float] = Field(None)
    class Config:
        json_schema_extra: {
            "orders": [
                {
                    "product_id": "kbnjn321v31sd",
                    "quantity": 1
                }
            ]
        }

# OrdersOfUser = OrderItem + created_at. In order to get orders of a user   
class OrdersOfUser(BaseModel):
    orders: list[OrderItem] = Field(...)
    create_at: str = Field(...)
    
# Order model
class OrderModel(BaseModel):
    order_id: str = Field(default_factory= lambda: str(uuid.uuid4()), alias="_id")
    user_id: str = Field(...)
    orders: list[OrderItem] = Field(...)
    created_at: str = Field(default=str(datetime.now()).strip().split(" ")[1][:8])
    
    class Config:
        populated_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "15131",
                "user_id": "Uid001",
                "orders": [
                {
                    "product_id": "4763e2d4-51ac-43a2-95a0-696a51745564",
                    "quantity": 5
                },
                {
                    "product_id": "d6253004-d913-4bd3-911e-cea8e959424b",
                    "quantity": 9
                }
                ]
            }
        }
##########################################################################




## PRODUCT MODEL REGION
##########################################################################

class ProductDetail(BaseModel):
    weight: Optional[float] = Field(None)
    dimensions: Optional[float] = Field(None)
    manufacturer: Optional[str] = Field(None)
    warrantly: Optional[int] = Field(None)

class ProductModel(BaseModel):
    product_id: str = Field(default_factory=lambda :str(uuid.uuid4()), alias="_id")
    name: str = Field(...)
    description: Optional[str] = Field("No description")
    category: Optional[str] = Field("Undefined category")
    price: float = Field(...)
    stock: int = Field(...)
    details: Optional[ProductDetail] = Field(None)

    class Config:
        populated_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "Pid1",
                "name": "Don Quixote",
                "price": "13.1",
                "stock": 10
            }
        }
##########################################################################
