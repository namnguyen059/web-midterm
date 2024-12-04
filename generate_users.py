from pymongo import MongoClient
from faker import Faker
import random

# Initialize Faker for generating fake data
fake = Faker()

# MongoDB connection
client = MongoClient('mongodb://localhost:27026/')  # Replace with your MongoDB connection string
db = client['ecommerce']  # Database name
users_collection = db['users']  # Users collection
products_collection = db['products']  # Products collection

# Function to generate fake user data
def generate_fake_user(product_ids):
    return {
        "user_id": fake.uuid4(),
        "name": fake.name(),
        "email": fake.email(),
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "zip": fake.zipcode(),
        },
        "orders": [
            {
                "order_id": fake.uuid4(),
                "product_id": random.choice(product_ids),  # Link to an existing product ID
                "quantity": random.randint(1, 10),
                "total_price": round(random.uniform(10, 1000), 2),
            } for _ in range(random.randint(0, 5))  # Random number of orders between 0 and 5
        ],
        "created_at": fake.date_time_this_decade(),
        "is_premium_member": fake.boolean(),
    }

# Insert many fake users into the collection
def insert_fake_data(n=100):
    product_ids = products_collection.distinct("product_id")  # Fetch product IDs from products collection
    fake_users = [generate_fake_user(product_ids) for _ in range(n)]
    result = users_collection.insert_many(fake_users)
    print(f"{len(result.inserted_ids)} fake users inserted")

# Run the insertion
if __name__ == "__main__":
    insert_fake_data(1000000)  # You can change the number of fake users here
