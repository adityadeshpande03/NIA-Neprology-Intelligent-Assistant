import os
from pymongo import MongoClient
from typing import Optional
from src.config import settings
from dotenv import load_dotenv

load_dotenv()


class MongoDBTool:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        if settings.DATABASE is None:
            raise ValueError("settings.DATABASE must not be None")
        self.db = self.client[settings.DATABASE]
        if settings.COLLECTION is None:
            raise ValueError("settings.COLLECTION must not be None")
        self.collection = self.db[settings.COLLECTION]

    def find(self, query: Optional[dict] = None, projection: Optional[dict] = None):
        """
        Retrieve documents from the collection.
        :param query: MongoDB query dictionary.
        :param projection: Fields to include or exclude.
        :return: List of documents.
        """
        if query is None:
            query = {}
        if projection is None:
            projection = {}
        return list(self.collection.find(query, projection))


# Example usage:
# tool = MongoDBTool("mongodb://localhost:27017/", "test_db", "test_collection")
# results = tool.find({"name": "John"})
