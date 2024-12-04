from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import ProductModel, OrderItem

router = APIRouter()

# Lấy tất cả thông tin liên quan đến sản phẩm theo product_id
@router.get("/", response_description="List all products", response_model=List[ProductModel])
async def list_products(request: Request):
    products = await request.app.database["product"].find(limit=100).to_list(length=100)
    if products:
        return products
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unavailable products")
