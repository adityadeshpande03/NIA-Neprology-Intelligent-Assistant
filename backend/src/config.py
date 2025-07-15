import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    QDRANT_URL: str = os.getenv("QDRANT_URL")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY")
    MONGODB_URI: str = os.getenv("MONGODB_URI")
    DATABASE: str = os.getenv("DATABASE")
    COLLECTION: str = os.getenv("COLLECTION")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

settings = Settings()