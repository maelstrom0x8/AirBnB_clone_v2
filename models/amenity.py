#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel


class Amenity(BaseModel, Base):
    """A class representing amenities"""
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)

    # Many-to-Many relationship with Place
    place_amenities = relationship('Place',
                                   secondary='place_amenity',
                                   back_populates='amenities')
