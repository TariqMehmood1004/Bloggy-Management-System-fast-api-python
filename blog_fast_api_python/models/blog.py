from sqlalchemy import Column, String, Text, ForeignKey
from database.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import DateTime, func


uuid4 = uuid.uuid4

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"Blog(id={self.id}, title={self.title}, body={self.body}, user_id={self.user_id})"
    
    def __str__(self):
        return f"Blog(id={self.id}, title={self.title}, body={self.body}, user_id={self.user_id})"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "body": self.body,
            "user_id": str(self.user_id),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    