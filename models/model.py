from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    password = Column(String, nullable=False)
    address_line_1 = Column(String, nullable=False)
    address_line_2 = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    country_code = Column(String, nullable=False)
    phone = Column(BigInteger, nullable=False)
    refresh_token = relationship("RefreshToken", back_populates="user", uselist=False)

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="refresh_token")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime)
    revoked = Column(Boolean, default=False, nullable=False)

    def is_expired(self):
        return datetime.utcnow() > self.expires_at or self.revoked


