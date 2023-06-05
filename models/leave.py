#!/usr/bin/python3
"""Leave module"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
import models


class Leave(BaseModel, Base):
    """Leave class to store leave"""
    __tablename__ = 'leave_requests'
    text = Column(String(1024), nullable=False)
    employee_id = Column(String(60), ForeignKey('employees.id'),
                         nullable=False)
    department_id = Column(String(60), ForeignKey('departments.id'),
                           nullable=False)
    approval = Column(Boolean, nullable=False, default=False)
