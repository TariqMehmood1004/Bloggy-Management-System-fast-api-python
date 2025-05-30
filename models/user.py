from sqlalchemy import Column, String, Boolean
from ..database.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import DateTime, func
from ..utils.hash import verify_password

uuid4 = uuid.uuid4

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    def verify_password(self, plain_password: str) -> bool:
        return verify_password(plain_password, self.password)

    def __repr__(self):
        return f"User(id={self.id}, is_admin={self.is_admin}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, password={self.password})"

    def __str__(self):
        return f"User(id={self.id}, is_admin={self.is_admin}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, password={self.password})"

    def to_dict(self):
        return {
            "id": str(self.id),
            "is_admin": self.is_admin,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }