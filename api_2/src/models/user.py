from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.sql import func
from ..database.session import Base
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_hash_password(password):
        return pwd_context.hash(password)

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def check_password(self, password):
        return self.verify_password(self.password, password)
