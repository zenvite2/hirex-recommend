from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.models.base import Base

class EmployeeSkill(Base):
    __tablename__ = 'employee_skill'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skill.id'), nullable=False)