from sqlalchemy import Column, Integer, String, Date
from core.database import Base

class Employee(Base):
    __tablename__ = 'hrd_employees'
    id = Column(Integer, primary_key=True, index=True)
    nip = Column(String, unique=True, index=True)
    nama = Column(String)
    jabatan = Column(String)
    tgl_masuk = Column(Date)