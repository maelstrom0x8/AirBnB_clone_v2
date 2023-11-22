#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base, id_generator
from sqlalchemy import ForeignKey, Column, String


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)
