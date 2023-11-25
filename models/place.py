#!/usr/bin/python3
""" Place Module for HBNB project """

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel


# place_amenity = Table('place_amenity', Base.metadata,
#                       Column('place_id', String(60),
#                              ForeignKey('places.id'),
#                              primary_key=True,
#                              nullable=False),
#                       Column('amenity_id', String(60),
#                              ForeignKey('amenities.id'),
#                              primary_key=True,
#                              nullable=False)
#                       )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer(), default=0, nullable=False)
    number_bathrooms = Column(Integer(), default=0, nullable=False)
    max_guest = Column(Integer(), default=0, nullable=False)
    price_by_night = Column(Integer(), default=0, nullable=False)
    latitude = Column(Float(), nullable=True)
    longitude = Column(Float(), nullable=True)

    user = relationship('User', back_populates='places')
    cities = relationship('City', back_populates='places')
    reviews = relationship('Review', back_populates='place')

    #
    # if "db" == os.getenv("HBNB_TYPE_STORAGE"):
    #     reviews = relationship("Review", cascade='all, delete, delete-orphan',
    #                            backref="place")
    #
    #     amenities = relationship("Amenity", secondary=place_amenity,
    #                              viewonly=False,
    #                              back_populates="place_amenities")
    # else:
    #     @property
    #     def reviews(self):
    #         """ Returns list of reviews. Id """
    #         var = models.storage.all()
    #         lista = []
    #         result = []
    #         for key in var:
    #             review = key.replace('.', ' ')
    #             review = shlex.split(review)
    #             if review[0] == 'Review':
    #                 lista.append(var[key])
    #         for elem in lista:
    #             if self.id == elem.place_id:
    #                 result.append(elem)
    #         return result
    #
    #     @property
    #     def amenities(self):
    #         """ Returns list of amenity ids """
    #         return self.amenity_ids
    #
    #     @amenities.setter
    #     def amenities(self, obj=None):
    #         """ Appends amenity ids to the attribute """
    #         if not (not (type(obj) is Amenity) or not (obj.id not in self.amenity_ids)):
    #             self.amenity_ids.append(obj.id)
