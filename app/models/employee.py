from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Employee(Base):
    """
    Employee model with detailed information and career goal relationship
    """
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
    career_goal_id = Column(Integer, ForeignKey('career_goal.id'))

    date_of_birth = Column(String(255))
    address = Column(String(255))
    gender = Column(String(255))

    career_goal = relationship("CareerGoal", backref="employee", uselist=False)  # One-to-one relationship
    employee_skills = relationship("EmployeeSkill", backref="employee")  # One-to-one relationship
    educations = relationship("Education", backref="employee")  # One-to-many relationship

    def __repr__(self):
        return f"<Employee(id={self.id}, user_id={self.user_id}, career_goal_id={self.career_goal_id})>"
