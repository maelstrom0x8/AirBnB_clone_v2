#!/usr/bin/python3

import contextlib
import os
from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

Entity = Union[Base, BaseModel]


class DataSource:
    __engine = None
    __session: Session = None
    __connection_url = ''
    __user = os.getenv('HBNB_MYSQL_USER')
    __password = os.getenv('HBNB_MYSQL_PWD')
    __host = os.getenv('HBNB_MYSQL_HOST')
    __database = os.getenv('HBNB_MYSQL_DB')
    __dialect = 'mysql'
    __driver = 'mysqldb'
    __env = os.getenv('HBNB_ENV')
    __port: int = int(os.getenv('HBNB_DB_PORT', 3306))

    def __init__(self) -> None:
        cargs = [f"{self.__dialect}+{self.__driver}://",
                 f"{self.__user}:{self.__password}@{self.__host}:",
                 f"{self.__port}/{self.__database}"]

        self.__connection_url = ''.join(cargs)
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

    def reset(self):
        if self.__session is not None:
            with contextlib.closing(self.__engine.connect()) as con:
                trans = con.begin()
                for table in reversed(Base.metadata.sorted_tables):
                    con.execute(table.delete())
                trans.commit()


class DBStorage:
    __engine = None
    __session = None

    entity_map: dict[str, Entity] = {
        'State': State, 'City': City, 'User': User,
        'Place': Place, 'Review': Review
    }

    def __init__(self) -> None:
        env = os.getenv('HBNB_ENV')
        self.datasource = DataSource()
        self.__engine = self.datasource.engine

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    @property
    def engine(self):
        return self.__engine

    @property
    def session(self) -> Session:
        return self.__session

    def new(self, obj):
        self.session.add(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        session_ = scoped_session(session_factory)
        self.__session = session_()

    def all(self, cls=None):
        _class = self.entity_map.get(cls)
        result = []
        if cls is not None:
            result.extend(self.session.query(_class).all())
            if len(result) == 1 and result[0][0] is None:
                return []

            # @formatter:off
            return {f"{entry.__class__.__name__}.{entry.id}": entry
                    for entry in result}
            # @formatter:on
        else:
            for item in self.entity_map.values():
                result.extend(self.session.query(item).all())
        # @formatter:off
        return {f"{entry.__class__.__name__}.{entry.id}": entry
                for entry in result}
        # @formatter:on

    def save(self):
        self.session.commit()
