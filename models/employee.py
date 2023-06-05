#!/usr/bin/python3
"""
Employee module
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
import models
import sqlalchemy


class Employee(BaseModel, Base):
    """The employee class, state_id and name"""
    __tablename__ = "employees"
    name = Column(String(128), nullable=False)
    department_id = Column(String(60), ForeignKey('departments.id'), nullable=False)
