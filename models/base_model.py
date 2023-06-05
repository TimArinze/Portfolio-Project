#!/usr/bin/python3
"""
base module for all class
"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import models
import pytz

Base = declarative_base()
west_africa_tz = pytz.timezone('Africa/Lagos')
time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """A base class for all"""
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.now(west_africa_tz))
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now(west_africa_tz))

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.now(west_africa_tz)
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.now(west_africa_tz)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now(west_africa_tz)
            self.updated_at = datetime.now(west_africa_tz)

    def __str__(self):
        """Returns a string representation of the instance"""
        return '[{:s}] ({:s}) {:s}'.format(self.__class__.__name__,
                                           self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now(west_africa_tz)

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if "_sa_instance_state" in dictionary:
            del dictionary["_sa_instance_state"]
        return dictionary

    def delete(self):
        """Deletes the current instance from the storage"""
        models.storage.delete(self)
