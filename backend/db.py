import os
import logging
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

logger = logging.getLogger(__name__)

uri = os.getenv("MONGODB_URI")

client = None
db = None
listings_collection = None
feedback_collection = None

if uri:
    try:
        # serverSelectionTimeoutMS=2000 ensures quick failure if DB is unreachable (e.g. offline/DNS/SSL issues)
        client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=2000)
        db = client["market_risk_detector"]
        listings_collection = db["listings"]
        feedback_collection = db["feedback"]
    except Exception as e:
        logger.warning(f"MongoDB connection failed to initialize: {e}")
        db = None