#!/usr/bin/python3
""" """
import models
from models.city import City
from models.state import State
from tests.test_models.test_base_model import test_basemodel, TestDBPersistence


class test_City(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)


class TestCityDBPersistence(TestDBPersistence):

    def test_city_count_is_zero_before_inserts(self):
        assert models.storage.session.query(City).count() == 0

    def test_city_creation(self):
        s1 = State()
        c1 = City()

        s1.name = 'Nigeria'
        c1.name = 'Lagos'
        c1.state_id = s1.id

        s1.save()
        c1.save()

        query = models.storage.session.query(City).where(City.id == c1.id)
        city = query.first()

        self.assertEqual(city.id, c1.id)
        self.assertEqual(city.state_id, s1.id)

    def test_state_deletion_cascades(self):
        s1 = State()
        s1.name = 'Plateau'
        s1.save()

        c1 = City()
        c1.name = 'LangTang'
        c2 = City()
        c2.name = 'Jos'
        c1.state_id = s1.id
        c2.state_id = s1.id

        c1.save()
        c2.save()

        cnt1 = (models.storage.session.query(City)
                .where(City.state_id == s1.id).count())
        models.storage.session.delete(s1)
        cnt2 = (models.storage.session.query(City)
                .where(City.state_id == s1.id).count())

        self.assertEqual(cnt1, 2)
        self.assertEqual(cnt2, 0)
