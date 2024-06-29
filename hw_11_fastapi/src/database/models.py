from sqlalchemy import Column, Integer, String, Boolean, func, Table
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(30))
    phone_number = Column(String(12), nullable=False)
    birth_date = Column(Date)