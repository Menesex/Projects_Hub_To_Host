from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class StepBase(BaseModel):
    title: str
    is_completed: bool = False

class StepCreate(StepBase):
    pass

class StepRead(StepBase):
    id: int
    task_id: int
    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_important: bool = False
    category: str = "Tasks"

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    is_completed: bool
    created_at: datetime
    user_id: str
    steps: List[StepRead] = []
    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    is_important: Optional[bool] = None
    due_date: Optional[datetime] = None
    category: Optional[str] = None
