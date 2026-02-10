"""
QdrantStore abstraction: minimal wrapper around qdrant-client.
If qdrant-client is not available at runtime, gracefully disable vector functionality.
"""

from typing import List, Optional, Dict, Any

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import PointStruct, VectorParams
    _QDRANT_AVAILABLE = True
except Exception:
    QdrantClient = None  # type: ignore
    _QDRANT_AVAILABLE = False

class QdrantStore:
    def __init__(self, url: str, api_key: Optional[str] = None, collection_name: str = "mem0_vectors"):
        if not _QDRANT_AVAILABLE:
            raise RuntimeError("qdrant-client not available")
        # parse url, default scheme handled by client
        kwargs = {}
        # very small wrapper; user may pass http(s) url
        if url.startswith("http://") or url.startswith("https://"):
            # QdrantClient can accept host & prefer_grpc flag; but easiest is passing url as host param
            host = url
            kwargs["url"] = host
        else:
            kwargs["url"] = url
        if api_key:
            kwargs["api_key"] = api_key

        self.client = QdrantClient(**kwargs)
        self.collection_name = collection_name
        # ensure collection exists (simple)
        try:
            if not self.client.get_collection(self.collection_name):
                # create with default params (embedding dim will be set on upsert if unknown)
                pass
        except Exception:
            # try create simple collection (if not exists)
            try:
                self.client.recreate_collection(self.collection_name, vector_size=1536, distance="Cosine")
            except Exception:
                # ignore; collection may already exist or remote config is different
                pass

    def upsert_vector(self, item_id: int, vector: List[float], payload: Optional[Dict[str, Any]] = None):
        pts = [PointStruct(id=item_id, vector=vector, payload=payload or {})]
        self.client.upsert(self.collection_name, pts)

    def search_vector(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        res = self.client.search(collection_name=self.collection_name, query_vector=query_vector, limit=limit)
        # return list of {id, score, payload}
        out = []
        for hit in res:
            out.append({
                "id": int(hit.id), 
                "score": float(hit.score),
                "payload": hit.payload if hasattr(hit, 'payload') else {}
            })
        return out

    def delete_vector(self, item_id: int):
        try:
            self.client.delete(self.collection_name, ids=[item_id])
        except Exception:
            pass
