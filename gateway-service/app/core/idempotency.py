from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.models import IdempotencyKey
from fastapi import Request, HTTPException, status
import json

async def get_idempotency_key(db: AsyncSession, key: str):
    result = await db.execute(select(IdempotencyKey).where(IdempotencyKey.key == key))
    return result.scalars().first()

async def create_idempotency_key(db: AsyncSession, key: str, response_data: dict):
    # Depending on DB, JSON might need dumping
    # SQLite with SQLAlchemy standard type JSON usually handles it, but let's be safe
    db_key = IdempotencyKey(key=key, response_body=response_data)
    db.add(db_key)
    await db.commit()
