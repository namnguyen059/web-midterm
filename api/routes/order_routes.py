from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from datetime import datetime
from models import OrderModel, OrderItem, OrdersOfUser
router = APIRouter()

@router.get("/{uid}", response_description="List orders of a user", response_model=List[OrdersOfUser])
async def list_orders(request: Request, uid: str):
    orders_of_user = await request.app.database["order"].find({"user_id": uid}).limit(100).to_list(100)
    if not orders_of_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {uid} has not been purchased yet")
    
    result = []
    for order_of_user in orders_of_user:
        instance = OrdersOfUser(orders=order_of_user["orders"], create_at=order_of_user["created_at"])
        result.append(instance.dict(by_alias=True))
        
    return result
    
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
    
    ordermodel = OrderModel(user_id=uid, orders=orders, created_at=str(datetime.now()).strip().split(" ")[1][:8])
    
    # Insert new order into the "order" collection
    result = await request.app.database["order"].insert_one(ordermodel.dict(by_alias=True))
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