#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os

from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

storage_t = os.getenv('HBNB_TYPE_STORAGE')

if storage_t == 'db':
    storage = DBStorage()
    storage.reload()
else:
    storage = FileStorage()
    storage.reload()
