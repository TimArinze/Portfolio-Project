#!/usr/bin/python3
"""
Department Module
"""
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
import models


class Department(BaseModel, Base):
    """Department Class"""
    __tablename__ = 'departments'
    name = Column(String(128), nullable=False)
