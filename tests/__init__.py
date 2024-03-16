#!/usr/bin/python3
"""
Tests for the AirBnb clone modules and classes.
"""
import os
from typing import TextIO
from models.engine.file_storage import FileStorage


def clear_stream(stream: TextIO):
    """
    Clears the contents of a given stream if it is seekable.
    """
    if stream.seekable():
        stream.seek(0)
        stream.truncate(0)


def delete_file(file_path: str):
    """
    Removes a file if it exists at the given path.
    """
    if os.path.isfile(file_path):
        os.unlink(file_path)


def reset_store(store: FileStorage, file_path='file.json'):
    """
    Resets the items in the given store and reloads it.
    """
    with open(file_path, mode='w') as file:
        file.write('{}')
    if store is not None:
        store.reload()


def read_text_file(file_name):
    """
    Reads the contents of a given file and returns it as a string.
    """
    lines = []
    if os.path.isfile(file_name):
        with open(file_name, mode='r') as file:
            for line in file.readlines():
                lines.append(line)
    return ''.join(lines)


def write_text_file(file_name, text):
    """
    Writes a text to a given file name.
    """
    with open(file_name, mode='w') as file:
        file.write(text)
