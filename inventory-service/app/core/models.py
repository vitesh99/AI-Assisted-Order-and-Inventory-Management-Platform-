from sqlalchemy import Column, String, JSON, DateTime
from app.db.base import Base
from datetime import datetime

class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    key = Column(String, primary_key=True, index=True)
    response_body = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
