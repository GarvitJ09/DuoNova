import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # MongoDB (Atlas/cloud)
    MONGODB_URL = os.getenv("MONGODB_URL")  # e.g. "mongodb+srv://user:pass@cluster.mongodb.net"
    DATABASE_NAME = os.getenv("DATABASE_NAME", "ats_checker")

    # AWS S3
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

    # Other global settings
    DEBUG = os.getenv("DEBUG", "False") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    # Add more as needed...

settings = Settings()