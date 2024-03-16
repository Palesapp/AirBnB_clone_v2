#!/usr/bin/python3
"""
Test Module - Contains all unittests for the BaseModel class
"""
from datetime import datetime
import json
import os
import unittest
from models.base_model import BaseModel, Base


class TestBasemodel(unittest.TestCase):
    """
    Test Class - Contains all unittests for the BaseModel class
    """

    def __init__(self, *args, **kwargs):
        """Initializes the test class."""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """
        Performs some operations before the tests are run but now it's empty
        """
        pass

    def tearDown(self):
        """
        Performs some operations after the tests are run.
        """
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_init(self):
        """
        Tests the initialization of the BaseModel class.
        """
        self.assertIsInstance(self.value(), BaseModel)
        if self.value is not BaseModel:
            self.assertIsInstance(self.value(), Base)
        else:
            self.assertNotIsInstance(self.value(), Base)

    def test_default(self):
        """
        Tests the default values of the BaseModel class.
        """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """
        Tests the kwargs initialization of the BaseModel class.
        """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """
        Tests the kwargs initialization of the BaseModel class with an int.
        """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)  # noqa

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_save(self):
        """
        Tests the save function of the BaseModel class with FileStorage.
        """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """
        Tests the __str__ function of the BaseModel class str representation.
        """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """
        Tests the to_dict function of the model class dictionary
        representation
        """
        i = self.value()
        d = i.to_dict()
        self.assertEqual(type(d), dict)
        self.assertEqual(d['__class__'], self.name)
        self.assertEqual(d['created_at'], i.created_at.isoformat())
        self.assertEqual(d['updated_at'], i.updated_at.isoformat())

        mdl = self.value()
        mdl.firstname = 'Celestine'
        mdl.lastname = 'Akpanoko'
        self.assertIn('firstname', mdl.to_dict())
        self.assertIn('lastname', mdl.to_dict())
        self.assertIn('firstname', self.value(firstname='Celestine').to_dict())
        self.assertIn('lastname', self.value(lastname='Akpanoko').to_dict())

        self.assertIsInstance(self.value().to_dict()['created_at'], str)
        self.assertIsInstance(self.value().to_dict()['updated_at'], str)

        datetime_now = datetime.today()
        mdl = self.value()
        mdl.id = '012345'
        mdl.created_at = mdl.updated_at = datetime_now
        to_dict = {
            'id': '012345',
            '__class__': mdl.__class__.__name__,
            'created_at': datetime_now.isoformat(),
            'updated_at': datetime_now.isoformat()
        }
        self.assertDictEqual(mdl.to_dict(), to_dict)

    def test_kwargs_none(self):
        """Tests kwargs that is empty."""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)  # noqa

    def test_kwargs_one(self):
        """Tests kwargs with one key-value pair."""
        n = {'Name': 'test'}
        new = self.value(**n)
        self.assertTrue(hasattr(new, 'Name'))

    def test_id(self):
        """Tests the type of id."""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """Tests the type of created_at."""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

    def test_updated_at(self):
        """Tests the type of updated_at."""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_delete(self):
        """Tests the delete function of the BaseModel class."""
        from models import storage
        i = self.value()
        i.save()
        self.assertTrue(i in storage.all().values())
        i.delete()
        self.assertFalse(i in storage.all().values())
