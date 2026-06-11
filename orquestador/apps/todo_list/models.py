from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from database import Base


class Step(Base):
    __tablename__ = "todo_steps"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)
    task_id = Column(Integer, ForeignKey("todo_tasks.id"))

    task = relationship("Task", back_populates="steps")


class Task(Base):
    __tablename__ = "todo_tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, default="guest_user")
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    is_important = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    category = Column(String, default="Tasks")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Direct class reference — no string lookup, no registry ambiguity
    steps = relationship(Step, back_populates="task", cascade="all, delete-orphan")
