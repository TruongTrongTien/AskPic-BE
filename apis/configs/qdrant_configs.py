from qdrant_client import QdrantClient
from qdrant_client.http import models

import os
from dotenv import load_dotenv

load_dotenv()

qdrant_client = QdrantClient(
    url = os.getenv("ASKPIC_QDRANT_URL"), 
    api_key = os.getenv("ASKPIC_QDRANT_API_KEY"),
)
print("Vector Database connected")

# Check if collection AskPic_Documents exists
if qdrant_client.collection_exists("AskPic_Documents") == False:
    qdrant_client.create_collection(
        collection_name="AskPic_Documents",
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
    )
