from sqlalchemy import Column, Integer, String
from app.models.base import Base

class EducationLevel(Base):
    """
    EducationLevel model representing different levels of education (e.g., Bachelor's, Master's, etc.)
    """
    __tablename__ = 'education_level'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    def __repr__(self):
        return f"<EducationLevel(id={self.id}, name='{self.name}')>"
