#!/usr/bin/python3
""" Review module for the HBNB project """
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel


class Review(BaseModel, Base):
    """A class representing reviews"""
    __tablename__ = 'reviews'

    text = Column(String(1024), nullable=False)

    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    place = relationship('Place', backref='reviews')

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='reviews')
