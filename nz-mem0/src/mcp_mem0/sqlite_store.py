"""
SQLiteStore - lightweight SQL abstraction over SQLAlchemy for nz-mem0.
Provides:
 - add(text, metadata) -> id
 - get(id) -> dict
 - get_many(ids) -> list[dict]
 - search_text(query, limit) -> list[dict]
 - get_last(limit) -> list[dict]
 - delete(id)
 - export_all()
"""

import json
import datetime
from typing import Optional, List, Dict, Any

from sqlalchemy import (
    Table, Column, Integer, String, Text, MetaData, DateTime
)
from sqlalchemy import select, insert, delete
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

metadata = MetaData()

mem_items = Table(
    "mem_items",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("text", Text, nullable=False),
    Column("metadata", Text, nullable=True),
    Column("created_at", DateTime, default=datetime.datetime.utcnow),
)


class SQLiteStore:
    def __init__(self, engine: Engine):
        self.engine = engine
        # create tables if not exists
        metadata.create_all(self.engine)

    def add(self, text: str, metadata_obj: Optional[Dict[str, Any]] = None) -> int:
        conn = self.engine.connect()
        try:
            payload = {
                "text": text,
                "metadata": json.dumps(metadata_obj or {}),
                "created_at": datetime.datetime.utcnow(),
            }
            res = conn.execute(insert(mem_items).values(**payload))
            conn.commit()
            return int(res.inserted_primary_key[0])
        finally:
            conn.close()

    def get(self, item_id: int) -> Optional[Dict[str, Any]]:
        conn = self.engine.connect()
        try:
            r = conn.execute(select(mem_items).where(mem_items.c.id == item_id)).first()
            if not r:
                return None
            return {
                "id": r.id,
                "text": r.text,
                "metadata": json.loads(r.metadata or "{}"),
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
        finally:
            conn.close()

    def get_many(self, ids: List[int]) -> List[Dict[str, Any]]:
        if not ids:
            return []
        conn = self.engine.connect()
        try:
            rows = conn.execute(select(mem_items).where(mem_items.c.id.in_(ids))).fetchall()
            out = []
            for r in rows:
                out.append({
                    "id": r.id,
                    "text": r.text,
                    "metadata": json.loads(r.metadata or "{}"),
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                })
            return out
        finally:
            conn.close()

    def search_text(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        # naive SQL LIKE-based search (fallback)
        conn = self.engine.connect()
        try:
            q = f"%{query}%"
            rows = conn.execute(
                select(mem_items).where(mem_items.c.text.ilike(q)).limit(limit)
            ).fetchall()
            out = []
            for r in rows:
                out.append({
                    "id": r.id,
                    "text": r.text,
                    "metadata": json.loads(r.metadata or "{}"),
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                })
            return out
        finally:
            conn.close()

    def get_last(self, limit: int = 50) -> List[Dict[str, Any]]:
        conn = self.engine.connect()
        try:
            rows = conn.execute(select(mem_items).order_by(mem_items.c.id.desc()).limit(limit)).fetchall()
            out = []
            for r in rows:
                out.append({
                    "id": r.id,
                    "text": r.text,
                    "metadata": json.loads(r.metadata or "{}"),
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                })
            return out
        finally:
            conn.close()

    def delete(self, item_id: int) -> None:
        conn = self.engine.connect()
        try:
            conn.execute(delete(mem_items).where(mem_items.c.id == item_id))
            conn.commit()
        finally:
            conn.close()

    def export_all(self) -> List[Dict[str, Any]]:
        conn = self.engine.connect()
        try:
            rows = conn.execute(select(mem_items)).fetchall()
            return [
                {
                    "id": r.id,
                    "text": r.text,
                    "metadata": json.loads(r.metadata or "{}"),
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                }
                for r in rows
            ]
        finally:
            conn.close()
