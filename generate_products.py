from pymongo import MongoClient
from faker import Faker
import random

# Initialize Faker for generating fake data
fake = Faker()

# MongoDB connection
client = MongoClient('mongodb://localhost:27026/')  # Replace with your MongoDB connection string
db = client['ecommerce']  # Database name
collection = db['products']  # Collection name

# Function to generate fake product data
def generate_fake_product():
    return {
        "product_id": fake.uuid4(),
        "name": fake.word() + " " + fake.word(),
        "description": fake.sentence(),
        "category": random.choice(["Computers", "Accessories", "Home Appliances", "Mobile Phones", "Electronics"]),
        "price": round(random.uniform(50, 2000), 2),
        "stock": random.randint(10, 500),
        "details": {
            "weight": f"{round(random.uniform(0.5, 5.0), 2)}kg",
            "dimensions": f"{random.randint(10, 50)} x {random.randint(10, 50)} x {random.randint(1, 20)} inches",
            "manufacturer": fake.company(),
            "warranty": f"{random.randint(1, 3)} years" if random.choice([True, False]) else f"{random.randint(6, 12)} months"
        }
    }

# Insert many fake products into the collection
def insert_fake_products(n=100):
    fake_products = [generate_fake_product() for _ in range(n)]
    result = collection.insert_many(fake_products)
    print(f"{len(result.inserted_ids)} fake products inserted")

# Run the insertion
if __name__ == "__main__":
    insert_fake_products(5)  # You can change the number of fake products here
