from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Employee(Base):
    __tablename__ = "employees_records"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    access_id = Column(String, nullable=True)
    area = Column(String, nullable=False)
    position = Column(String, nullable=False)
    entry_hour = Column(String, nullable=False)
    active = Column(Boolean, default=True)
