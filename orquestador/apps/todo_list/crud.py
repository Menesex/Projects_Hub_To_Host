from sqlalchemy.orm import Session
from .models import Task, Step
from .schemas import TaskCreate, TaskUpdate, StepCreate


def get_tasks(db: Session, user_id: str = "guest_user"):
    return db.query(Task).filter(Task.user_id == user_id).all()


def create_task(db: Session, task: TaskCreate, user_id: str = "guest_user"):
    db_task = Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_update: TaskUpdate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True


def create_step(db: Session, step: StepCreate, task_id: int):
    db_step = Step(**step.dict(), task_id=task_id)
    db.add(db_step)
    db.commit()
    db.refresh(db_step)
    return db_step


def get_steps_by_task(db: Session, task_id: int):
    return db.query(Step).filter(Step.task_id == task_id).all()


def update_step(db: Session, step_id: int, is_completed: bool):
    db_step = db.query(Step).filter(Step.id == step_id).first()
    if not db_step:
        return None
    db_step.is_completed = is_completed
    db.commit()
    db.refresh(db_step)
    return db_step


def delete_step(db: Session, step_id: int) -> bool:
    db_step = db.query(Step).filter(Step.id == step_id).first()
    if not db_step:
        return False
    db.delete(db_step)
    db.commit()
    return True
