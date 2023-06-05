#!/usr/bin/python3
"""
storage module
"""
from os import getenv, environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.employee import Employee
from models.department import Department
from models.leave import Leave


class Storage:
    """Storage class"""
    __engine = None
    __session = None


    def __init__(self):
        """Instantiation"""
        user = environ.get("MYSQL_USER")
        passwd = environ.get("MYSQL_PWD")
        host = environ.get("MYSQL_HOST")
        database = environ.get("MYSQL_DB")
        env = environ.get("ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                                      user, passwd, host, database),
                                      pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database"""

        obj_classes = {'Employee': Employee, 'Department': Department}

        dictionary = {}
        if cls is None:
            for obj_class in obj_classes.value():
                obj_list = self.__session.query(obj_class)
                for obj in obj_list:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    dictionary[key] = obj
                    del obj.__dict__['_sa_instance_state']
                return dictionary
        else:
            obj_list = self.__session.query(cls)
            for obj in obj_list:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                dictionary[key] = obj
            return dictionary

    def new(self, obj):
        """Adds object to a current database"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from current database session obj"""
        if obj is not None:
            self.__session.delete(obj)
        else:
            pass

    def reload(self):
        """ Reload """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """call close method on the private session attribute"""
        self.__session.close()
