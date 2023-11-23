#!/usr/bin/python3
""" """
import os

import models
from models.state import State
from tests.test_models.test_base_model import test_basemodel, TestDBPersistence, is_valid_uuid4


class test_state(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)


class TestStatePersistence(TestDBPersistence):

    def test_env_is_db(self):
        assert os.getenv('HBNB_TYPE_STORAGE') == 'db'
        assert len(models.storage.all(State)) == 0

    def test_state_creation(self):
        s1 = State()
        s1.name = 'Kansas'
        s2 = State()
        s2.name = 'Ohio'
        s1.save()
        s2.save()

        self.assertTrue(is_valid_uuid4(s1.id))
        self.assertTrue(is_valid_uuid4(s2.id))

    def test_duplicates_with_unique_ids(self):
        s1 = State()
        s1.name = 'Nevada'
        s2 = State()
        s2.name = 'Nevada'

        s1.save()
        s2.save()

        self.assertNotEqual(s1.id, s2.id)

    def test_nonnull_name_raises_exception(self):
        s1 = State()

        self.assertRaises(AttributeError, s1.save)
