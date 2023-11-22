#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, id_generator
from sqlalchemy import ForeignKey, Column, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', cascade='all, delete', backref='states')
    else:
        def cities(self):
            """city relationship for file storage"""
            import models
            result = models.storage.all(models.City)
            return [y for _, y in result.items() if self.id == y.id]
