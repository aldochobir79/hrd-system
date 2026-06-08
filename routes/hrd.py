from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db, engine, Base
from schemas import employee as schemas
from services import hrd_service
from fastapi import APIRouter, Depends, HTTPException

Base.metadata.create_all(bind=engine)
router = APIRouter(prefix='/hrd', tags=['HRD'])

@router.get('/employees', response_model=list[schemas.Employee])
def list_employees(db: Session = Depends(get_db)):
    return hrd_service.get_employees(db)

@router.post('/employees', response_model=schemas.Employee)
def add_employee(emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_emp = hrd_service.create_employee(db, emp)
    if db_emp is None:
        raise HTTPException(
            status_code=400, 
            detail=f"NIP {emp.nip} sudah terdaftar. Gunakan NIP lain."
        )
    return db_emp

@router.get('/employees/{emp_id}', response_model=schemas.Employee)
def get_employee_detail(emp_id: int, db: Session = Depends(get_db)):
    db_emp = hrd_service.get_employee(db, emp_id)
    if db_emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_emp

@router.put('/employees/{emp_id}', response_model=schemas.Employee)
def update_employee_data(emp_id: int, emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_emp = hrd_service.update_employee(db, emp_id, emp)
    if db_emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    if db_emp == "nip_duplicate":
        raise HTTPException(status_code=400, detail=f"NIP {emp.nip} sudah dipakai karyawan lain")
    return db_emp

@router.delete('/employees/{emp_id}')
def delete_employee_data(emp_id: int, db: Session = Depends(get_db)):
    db_emp = hrd_service.delete_employee(db, emp_id)
    if db_emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}