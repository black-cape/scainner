import os
from datetime import datetime, timedelta, timezone

from pymongo import MongoClient

MONGO_HOSTNAME = os.getenv("MONGO_DB_HOSTNAME")
MONGO_PORT = os.getenv("MONGO_DB_PORT")
MONGO_PORT = MONGO_PORT if MONGO_PORT else 27017
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_DB_NAME = MONGO_DB_NAME if MONGO_DB_NAME else "scainner-db"

client_singleton: MongoClient | None = None


def is_mongo_configured():
    """Check if MongoDB is configured (hostname is set)."""
    return MONGO_HOSTNAME


def init_client():
    global client_singleton
    if not is_mongo_configured():
        return
    client_singleton = MongoClient(f"mongodb://{MONGO_HOSTNAME}:{MONGO_PORT}/")


def get_client():
    if not client_singleton:
        init_client()
    return client_singleton


def close_client():
    if client_singleton:
        client_singleton.close()


def get_transcriptions_collection():
    """Get the transcriptions collection. Returns None if MongoDB is not configured."""
    client = get_client()
    if client is None:
        return None
    db = client["transcriber_db"]
    if "transcriptions" not in db.list_collection_names():
        collection = db.create_collection("transcriptions")
        collection.create_index("timestamp")
        return collection
    return db["transcriptions"]


def clear_audio_older_than_30_days():
    """Clear audio files older than 30 days. Does nothing if MongoDB is not configured."""
    collection = get_transcriptions_collection()
    if collection is None:
        return
    thirty_days_ago = datetime.now(tz=timezone.utc) - timedelta(days=30)
    result = collection.update_many(
        {"timestamp": {"$lt": thirty_days_ago}, "audio": {"$ne": None}},
        {"$set": {"audio": None}},
    )
    print(f"Cleared {result.modified_count} audio files older than 30 days")
