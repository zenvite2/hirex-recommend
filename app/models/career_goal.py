from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class CareerGoal(Base):
    """
    CareerGoal model representing an employee's career preferences
    """
    __tablename__ = 'career_goal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    industry_id = Column(Integer)
    min_salary = Column(Integer)
    max_salary = Column(Integer)
    position_id = Column(Integer)
    job_type_id = Column(Integer)

    def __repr__(self):
        return (f"<CareerGoal(id={self.id}, industry_id={self.industry_id}, "
                f"position_id={self.position_id}, job_type_id={self.job_type_id}, "
                f"min_salary={self.min_salary}, max_salary={self.max_salary})>")
