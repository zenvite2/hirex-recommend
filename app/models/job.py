from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Text,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.types import JSON
from app.models.base import Base


class Job(Base):
    """
    Job model
    """
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String(255), nullable=False)  # Job name
    description = Column(Text, nullable=True)  # Job description
    benefit = Column(Text, nullable=True)  # Job benefits
    requirement = Column(Text, nullable=True)  # Candidate requirements
    location = Column(String(255), nullable=True)  # Job location

    min_salary = Column(Integer, nullable=True)
    max_salary = Column(Integer, nullable=True)

    # Job-specific details
    year_experience = Column(Integer, nullable=True)
    city_id = Column(Integer, nullable=True)
    district_id = Column(Integer, nullable=True)
    position_id = Column(Integer, nullable=True)
    job_type_id = Column(Integer, nullable=True)
    contract_type_id = Column(Integer, nullable=True)
    education_level_id = Column(Integer, nullable=True)

    job_skills = relationship("JobSkill", backref="job")  # One-to-many relationship

    def __repr__(self):
        return (f"<Job(id={self.id}, title='{self.title}', status={self.status}, "
                f"min_salary={self.min_salary}, max_salary={self.max_salary})>")
