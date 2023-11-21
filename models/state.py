#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, id_generator
from sqlalchemy import ForeignKey, Column, String


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
