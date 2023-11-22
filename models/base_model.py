#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime
from models.__init__ import storage
import uuid
from datetime import datetime


def id_generator() -> str:
    _id = uuid.uuid4()
    return str(_id)


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, default=id_generator)
    created_at = Column(DateTime(), default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        orm_name = '_sa_instance_state'
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        if orm_name in self.__dict__:
            del (self.__dict__[orm_name])
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        orm_name = '_sa_instance_state'
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if orm_name in dictionary:
            del (dictionary[orm_name])
        return dictionary

    def delete(self):
        """Deletes an instance from storage"""
        storage.delete(self)
