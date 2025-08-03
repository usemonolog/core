from sqlalchemy import Column, Integer, String, UUID, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import JSONB


class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    knowledge_foundation = Column(String, nullable=False)
    guideline = Column(JSONB, nullable=False)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    submissions = relationship("Submission", back_populates="scenario")
