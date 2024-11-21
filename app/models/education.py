from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.models.base import Base

class Education(Base):
    """
    Education model representing an employee's education details
    """
    __tablename__ = 'education'

    id = Column(Integer, primary_key=True, autoincrement=True)
    education_level_id = Column(Integer, ForeignKey('education_level.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    # university_name = Column(String(255), nullable=False)
    # expertise = Column(String(255), nullable=False)
    # start_date = Column(Date, nullable=False)
    # end_date = Column(Date, nullable=False)
    # description = Column(String(255), nullable=True)

    # Relationships
    education_level = relationship("EducationLevel", backref="educations")

    def __repr__(self):
        return (f"<Education(id={self.id}, education_level_id={self.education_level_id}, "
                f"employee_id={self.employee_id}, university_name='{self.university_name}', "
                f"expertise='{self.expertise}', start_date={self.start_date}, "
                f"end_date={self.end_date}, description='{self.description}')>")
