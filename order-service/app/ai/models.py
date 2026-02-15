from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class OrderAIMetadata(Base):
    __tablename__ = "order_ai_metadata"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    summary_text = Column(Text, nullable=True)
    notification_draft = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
