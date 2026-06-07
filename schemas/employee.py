from pydantic import BaseModel
from datetime import date

class EmployeeBase(BaseModel):
    nip: str
    nama: str
    jabatan: str
    tgl_masuk: date

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    class Config:
        from_attributes = True