# services/hrd_service.py
from sqlalchemy.orm import Session
from models import employee as models
from schemas import employee as schemas

def get_employees(db: Session):
    return db.query(models.Employee).all()

def get_employee(db: Session, emp_id: int):
    return db.query(models.Employee).filter(models.Employee.id == emp_id).first()

def get_employee_by_nip(db: Session, nip: str):
    return db.query(models.Employee).filter(models.Employee.nip == nip).first()

def create_employee(db: Session, emp: schemas.EmployeeCreate):
    # Cek NIP udah ada atau belum
    if get_employee_by_nip(db, emp.nip):
        return None  # Balikin None kalo duplikat
    
    db_emp = models.Employee(**emp.model_dump())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

def update_employee(db: Session, emp_id: int, emp: schemas.EmployeeCreate):
    db_emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not db_emp:
        return None
        
    # Bonus: validasi NIP duplikat pas update
    existing = get_employee_by_nip(db, emp.nip)
    if existing and existing.id != emp_id:
        return "nip_duplicate"
        
    for key, value in emp.model_dump().items():
        setattr(db_emp, key, value)
    db.commit()
    db.refresh(db_emp)
    return db_emp

def delete_employee(db: Session, emp_id: int):
    db_emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if db_emp:
        db.delete(db_emp)
        db.commit()
    return db_emp