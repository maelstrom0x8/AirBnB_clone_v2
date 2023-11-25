#!/usr/bin/python3
import unittest

from models import storage
from models.base_model import Base


class TestDBStorage(unittest.TestCase):

    def test_db_mode_is_initialized(self):
        self.assertTrue(storage.session is not None)
        self.assertTrue(storage.engine is not None)

    def test_metadata_schema_is_populated(self):
        metadata = Base.metadata

        self.assertTrue(metadata.tables is not None)
