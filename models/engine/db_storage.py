#!/usr/bin/env python3

import os

from typing import Any, Union
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import DatabaseError
from models.base_model import BaseModel, Base
from models.user import User
from models.city import *
from models.state import *

Entity = Union[Base, BaseModel]


class DataSource:
    __engine = None
    __session = None
    __connection_url = ''
    __user = os.getenv('HBNB_MYSQL_USER')
    __password = os.getenv('HBNB_MYSQL_PWD')
    __host = os.getenv('HBNB_MYSQL_HOST')
    __database = os.getenv('HBNB_MYSQL_DB')
    __dialect = 'mysql'
    __driver = 'mysqldb'
    __env = os.getenv('HBNB_ENV')

    def __init__(self) -> None:
        self.__connection_url = f"{self.__dialect}+{self.__driver}://{self.__user}:{self.__password}@{self.__host}/{self.__database}"
        self.__engine = create_engine(
            self.__connection_url, pool_pre_ping=True)


    @property
    def engine(self):
        return self.__engine

    @property
    def session(self):
        return self.__session

    def get_connection_details(self):
        return self.__connection_url


class DBStorage:
    __engine = None
    __session = None

    entity_map: dict[str, Entity] = {
        'State': State, 'City': City, 'User': User
    }

    def __init__(self) -> None:
        env = os.getenv('HBNB_ENV')
        self.datasource = DataSource()
        self.__engine = self.datasource.engine

        if env == 'test':
            Base.meta.drop_all(self.__engine)

    @property
    def engine(self):
        return self.__engine

    @property
    def session(self):
        return self.__session

    def new(self, obj):
        _class = self.entity_map.get(obj.__class__.__name__)
        if not _class:
            print("** class doesn't exist **")
            return None
        self.session.add(obj)

    def reload(self):
        if self.engine is not None:
            Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()


    def all(self, cls=None):
        _class = self.entity_map.get(cls)
        result = []
        if cls is not None:
            result.extend(self.session.query(_class).all())
            return {f"{entry.__class__.__name__}.{entry.id}": entry for entry in result}
        else:
            for item in self.entity_map.values():
                result.extend(self.session.query(item).all())

        return {f"{entry.__class__.__name__}.{entry.id}": entry for entry in result}

    def save(self):
        self.session.commit()
