from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from .config import QDRANT_HOST, QDRANT_PORT, COLLECTION_NAME
import psycopg2

def init_qdrant():
    try:
        q = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        collections = [c.name for c in q.get_collections().collections]
        if COLLECTION_NAME not in collections:
            q.create_collection(
                COLLECTION_NAME,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )
        return True
    except Exception:
        return False

def init_postgres(url: str):
    try:
        conn = psycopg2.connect(url)
        conn.close()
        return True
    except Exception:
        return False
 