from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db, engine, Base
from schemas import employee as schemas
from services import hrd_service

Base.metadata.create_all(bind=engine)
router = APIRouter(prefix='/hrd', tags=['HRD'])

@router.get('/employees', response_model=list[schemas.Employee])
def list_employees(db: Session = Depends(get_db)):
    return hrd_service.get_employees(db)

@router.post('/employees', response_model=schemas.Employee)
def add_employee(emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return hrd_service.create_employee(db, emp)