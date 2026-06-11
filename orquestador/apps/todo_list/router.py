from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from .models import Task
from . import crud, schemas

router = APIRouter(prefix="/api/tasks", tags=["To-Do List"])


@router.get("/", response_model=List[schemas.TaskRead])
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)


@router.post("/", response_model=schemas.TaskRead)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)


@router.patch("/{task_id}", response_model=schemas.TaskRead)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_id, task_update)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    if not crud.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@router.post("/{task_id}/steps", response_model=schemas.StepRead)
def create_step(task_id: int, step: schemas.StepCreate, db: Session = Depends(get_db)):
    if not db.query(Task).filter(Task.id == task_id).first():
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.create_step(db=db, step=step, task_id=task_id)


@router.get("/{task_id}/steps", response_model=List[schemas.StepRead])
def read_steps(task_id: int, db: Session = Depends(get_db)):
    if not db.query(Task).filter(Task.id == task_id).first():
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.get_steps_by_task(db=db, task_id=task_id)


@router.patch("/steps/{step_id}", response_model=schemas.StepRead)
def update_step(step_id: int, is_completed: bool, db: Session = Depends(get_db)):
    db_step = crud.update_step(db, step_id, is_completed)
    if not db_step:
        raise HTTPException(status_code=404, detail="Step not found")
    return db_step


@router.delete("/steps/{step_id}")
def delete_step(step_id: int, db: Session = Depends(get_db)):
    if not crud.delete_step(db, step_id):
        raise HTTPException(status_code=404, detail="Step not found")
    return {"message": "Step deleted successfully"}
