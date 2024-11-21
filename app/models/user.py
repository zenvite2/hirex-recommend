from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(Base):
    """
    User model representing system users
    """
    __tablename__ = 'user'
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    email = Column(String(255), unique=True)
    role_id = Column(Integer, ForeignKey('role.id'))
    
    avatar = Column(String(255))
    full_name = Column(String(255))
    phone_number = Column(String(255))

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"