import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    MONGODB_URI = os.getenv("MONGODB_URI")
    DATABASE = os.getenv("DATABASE")
    COLLECTION = os.getenv("COLLECTION")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

settings = Settings()