import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:

    def __init__(self):
        self.uri = os.getenv("MONGODB_URI")
        self.database = os.getenv("DATABASE")
        self.collection = os.getenv("COLLECTION")

    def database_connection(self, patients):
        client = MongoClient(self.uri)
        db = client[self.database]
        collection = db[self.collection]
        collection.insert_many(patients)
        return "Database connection established and data inserted."

if __name__ == "__main__":
    with open(input("Enter the path to the patients JSON file: "), "r") as file:
        patients = json.load(file)
    db_config = DatabaseConfig()
    result = db_config.database_connection(patients)
    print(result)