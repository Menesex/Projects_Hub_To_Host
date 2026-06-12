from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from . import crud, schemas

router = APIRouter(prefix="/api/employees", tags=["Employees Manager"])


@router.get("/", response_model=List[schemas.EmployeeResponse])
def read_employees(
    status: str = "all",
    search: str = "",
    search_type: str = "nombre",
    db: Session = Depends(get_db),
):
    return crud.get_employees(db, status=status, search=search, search_type=search_type)


@router.post("/", response_model=schemas.EmployeeResponse, status_code=201)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db=db, employee=employee)


@router.put("/{employee_id}", response_model=schemas.EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_update: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
):
    db_employee = crud.update_employee(db, employee_id, employee_update)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return db_employee


@router.patch("/{employee_id}/retire", response_model=schemas.EmployeeResponse)
def retire_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.retire_employee(db, employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return db_employee


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    if not crud.delete_employee(db, employee_id):
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return {"message": "Empleado eliminado exitosamente"}
