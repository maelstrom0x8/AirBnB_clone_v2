#!/usr/bin/python3
""" State Module for HBNB project """
import os

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref

from models.base_model import BaseModel, Base
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', cascade='all, delete-orphan',
                              backref=backref('states'))
    else:
        def cities(self):
            """city relationship for file storage"""
            import models
            result = models.storage.all(City)
            return [y for _, y in result.items() if self.id == y.id]

    def save(self):
        if self.name is None:
            raise AttributeError("Attribute 'name' cannot be none")
        super().save()
