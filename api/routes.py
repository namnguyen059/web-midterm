from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import UserModel, ProductModel, OrderModel, OrderItem

router = APIRouter()

# Lấy tất cả thông tin liên quan đến sản phẩm theo product_id
@router.get("/products", response_description="List all products", response_model=List[ProductModel])
async def list_products(request: Request):
    products = await request.app.database["product"].find(limit=100).to_list(length=100)
    if products:
        return products
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unavailable products")

@router.get("/orders/{user_id}", response_description="Get all orders for a user", response_model=List[OrderModel])
async def get_orders_by_user(user_id: str, request: Request):
    # Find all orders where user_id matches
    user_orders = await request.app.database["order"].find({"user_id": user_id}).to_list(length=100)
    
    if user_orders:
        return user_orders
    
    # Raise 404 if no orders are found for the given user_id
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No orders found for user_id {user_id}")

@router.post("/", response_description="Create a new order", status_code=status.HTTP_201_CREATED, response_model=OrderModel)
async def create_order(request: Request, uid: str = Body(...), orders : List[OrderItem] = Body(...)):
    
    # Compute total_price
    orders = jsonable_encoder(orders)
    for order in orders:
        pid = order["product_id"]
        quantity = order["quantity"]
    
        # refer product_id of orders to product's info in ProductModel
        product_respectively = await request.app.database["product"].find_one({"_id": pid})
        if not product_respectively:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No product found with product_id {pid}")

        price = product_respectively["price"]
    
        # Insert 'total_price' into document
        order["total_price"] = quantity * price
    
    ordermodel = OrderModel(user_id=uid, orders=orders)
    
    # Insert new order into the "order" collection
    result = await request.app.database["order"].insert_one(ordermodel.model_dump(by_alias=True))
    if not result.inserted_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insert into database failed")
    # Fetch the created order back from the database
    new_order = await request.app.database["order"].find_one({"_id": result.inserted_id})
    
    return new_order

    
    
@router.delete("/{id}", response_description="Cancel order by order_id")
async def delete_order(id: str, request: Request):
    delete_result = await request.app.database["order"].delete_one({"_id": id})
    if delete_result.deleted_count != 0:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with ID {id} has not been created yet")



@router.put("/", response_description="Change order's information by product_id", response_model=OrderModel)
async def update_order(request: Request, oid: str = Body(...), orders: List[OrderItem] = Body(...)):
    # Find the specific order by product_id 
    order_to_update = await request.app.database["order"].find_one({"_id": oid})

    if not order_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No order found with order_id {oid}")

    od_items = jsonable_encoder(orders)

    # total_price of each orderitem in orders: List[OrderItem]
    for od_item in od_items:
        pid = od_item["product_id"]
        product_respectively = await request.app.database["product"].find_one({
            "_id": pid
        })
        if not product_respectively:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No product found with product_id {pid}")

        price = product_respectively["price"]
        
        od_item["total_price"] = od_item["quantity"] * price
        
        # if need to modify 'created_at' with respect to updated time
        # od_item["created_at"] = datetime.... remains the same as in models
    
    # Update the order in the database
    result = await request.app.database["order"].update_one(
        {
            "_id": oid
        }, 
        {
            "$set": {
                "orders": od_items
            }
        }
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update failed")

    # Fetch the updated order
    updated_order = await request.app.database["order"].find_one({"_id": oid})
    
    return updated_order


    
    