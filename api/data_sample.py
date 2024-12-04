from models import ProductModel, Address, UserModel
from pymongo import MongoClient
from fastapi import FastAPI
from dotenv import dotenv_values

# Fake user product

app = FastAPI()

config = dotenv_values(".env")
app.mongo_client = MongoClient(config["ATLAS_URI"])
app.database = app.mongo_client[config["DB_NAME"]]

async def create_product(db):
    product = ProductModel(
        name="Oishi",
        description="Oishi bung no vi cay",
        price=12.0,
        stock=100
    )
    product = product.dict(by_alias=True)
    db["product"].insert_one(product)
    
    product = ProductModel(
        name="Keo sua Milkita",
        description="Keo sua Milkita duoc lam tu sua",
        price=25.0,
        stock=70
    )
    product = product.dict(by_alias=True)
    db["product"].insert_one(product)



async def create_user(db):
    address = Address(street="Main street", city="Example city")
    user = UserModel(
        name="John Weekend",
        password="securepassword123",
        phone="1234567890",
        address=address
    )

    user = user.dict(by_alias=True)
    db["user"].insert_one(user)



@app.on_event("startup")
async def startup_event():
    await create_product(app.database)
    await create_user(app.database)


# MongoDB shutdown
@app.on_event("shutdown")
def shutdown_event():
    app.mongo_client.close()