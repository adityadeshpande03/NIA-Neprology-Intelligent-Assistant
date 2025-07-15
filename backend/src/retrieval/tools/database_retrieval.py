import os
from pymongo import MongoClient
from src.config import settings
from dotenv import load_dotenv

load_dotenv()

class MongoDBTool:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client[settings.DATABASE]
        self.collection = self.db[settings.COLLECTION]

    def find(self, query: dict = None, projection: dict = None):
        """
        Retrieve documents from the collection.
        :param query: MongoDB query dictionary.
        :param projection: Fields to include or exclude.
        :return: List of documents.
        """
        if query is None:
            query = {}
        return list(self.collection.find(query, projection))

# Example usage:
# tool = MongoDBTool("mongodb://localhost:27017/", "test_db", "test_collection")
# results = tool.find({"name": "John"})