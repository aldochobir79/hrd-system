from sqlalchemy.orm import Session
from models import employee as models
from schemas import employee as schemas

def get_employees(db: Session):
    return db.query(models.Employee).all()

def create_employee(db: Session, emp: schemas.EmployeeCreate):
    db_emp = models.Employee(**emp.model_dump())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp