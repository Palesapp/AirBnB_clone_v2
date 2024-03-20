#!/usr/bin/python3
""" Module for testing file storage"""
import os
import unittest
from models import storage
from models.base_model import BaseModel


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
class TestFileStorage(unittest.TestCase):
    """
    Test cases for FileStorage class
    """

    def setUp(self):
        """
        Remove storage file at start of tests
        """
        del_list = []
        for key in storage.all().keys():
            del_list.append(key)
        for key in del_list:
            del storage.all()[key]

    def tearDown(self):
        """
        Remove storage file at end of tests
        """
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_obj_list_empty(self):
        """
        Tests that __objects is empty at start of tests
        """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """
        Tests that new objects are properly added to __objects
        """
        new = BaseModel()  # noqa
        new.save()
        for obj in storage.all().values():
            temp = obj
        self.assertTrue(temp is obj)

    def test_all(self):
        """
        Tests that all() returns __objects
        """
        new = BaseModel()  # noqa
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """
        Tests that a new instance of BaseModel is created
        """
        new = BaseModel()  # noqa
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """
        Tests that all() returns an empty dictionary if __objects is empty
        """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)  # noqa
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """
        Tests that save() properly saves objects to file.json
        """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """
        Tests that reload() properly loads objects from file.json
        """
        new = BaseModel()
        new.save()
        storage.reload()
        loaded = None
        for obj in storage.all().values():
            loaded = obj
        self.assertNotEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """
        Tests that reload() properly loads an empty file.json
        """
        with open('file.json', 'w') as f:  # noqa
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """
        Tests that reload() properly loads from a nonexistent file.json
        """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """
        Tests that save() properly saves BaseModel objects to file.json
        """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """
        Tests that __file_path is a string
        """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """
        Tests that __objects is a dictionary
        """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """
        Tests that the key for each object in __objects is in
        <class name>.<id> format
        """
        new = BaseModel()
        _id = new.to_dict()['id']
        temp = ''
        new.save()
        for key, value in storage.all().items():
            if value is new:
                temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """
        Tests that a new instance of FileStorage is created
        """
        from models.engine.file_storage import FileStorage
        self.assertEqual(type(storage), FileStorage)
