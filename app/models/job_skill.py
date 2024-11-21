from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.models.base import Base

class JobSkill(Base):
    __tablename__ = 'job_skill'

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skill.id'), nullable=False)