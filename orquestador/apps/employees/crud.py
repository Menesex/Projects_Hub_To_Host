from sqlalchemy.orm import Session
from sqlalchemy import or_
from .models import Employee
from .schemas import EmployeeCreate, EmployeeUpdate


def get_employees(db: Session, status: str = "all", search: str = "", search_type: str = "nombre"):
    query = db.query(Employee)

    if status == "active":
        query = query.filter(Employee.active == True)
    elif status == "inactive":
        query = query.filter(Employee.active == False)

    if search:
        if search_type == "id":
            try:
                search_int = int(search)
                query = query.filter(Employee.id == search_int)
            except ValueError:
                pass
        elif search_type == "access_id":
            query = query.filter(Employee.access_id.ilike(f"%{search}%"))
        else:
            query = query.filter(Employee.name.ilike(f"%{search}%"))

    return query.all()


def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, employee_id: int, employee_update: EmployeeUpdate):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        return None

    for key, value in employee_update.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)

    db.commit()
    db.refresh(db_employee)
    return db_employee


def retire_employee(db: Session, employee_id: int):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        return None

    db_employee.active = False
    db_employee.access_id = None
    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: int) -> bool:
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        return False

    db.delete(db_employee)
    db.commit()
    return True
