# models/token.py
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from ..database.database import Base
import uuid
from sqlalchemy import DateTime, func

class Token(Base):
    __tablename__ = "tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    token = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"Token(id={self.id}, user_id={self.user_id}, token={self.token}, created_at={self.created_at})"
    
    def __str__(self):
        return f"Token(id={self.id}, user_id={self.user_id}, token={self.token}, created_at={self.created_at})"
    
    def get_user_on_token(self, db):
        return db.query(User).filter(User.id == self.user_id).first()
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "token": self.token,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }