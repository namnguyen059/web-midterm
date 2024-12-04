from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from dotenv import dotenv_values
from fastapi.middleware.cors import CORSMiddleware
from routes.order_routes import router as order_router
from routes.product_routes import router as product_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

config = dotenv_values(".env")

# MongoDB connection
app.mongo_client = AsyncIOMotorClient(config["ATLAS_URI"])
app.database = app.mongo_client[config["DB_NAME"]]

# Include order and product routers
app.include_router(order_router, tags=["orders"], prefix="/orders")
app.include_router(product_router, tags=["products"], prefix="/products")
