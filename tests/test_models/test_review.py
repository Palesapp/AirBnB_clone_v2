#!/usr/bin/python3
"""
Defines the unittests for models/review.py
"""
import os
from tests.test_models.test_base_model import TestBasemodel
from models.review import Review


class TestReview(TestBasemodel):
    """
    A unittest for Review class
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the test class for Review
        """
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """
        Tests the type of place_id attribute
        """
        new = self.value()
        self.assertEqual(
            type(new.place_id),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        )

    def test_user_id(self):
        """
        Tests the type of user_id attribute
        """
        new = self.value()
        self.assertEqual(
            type(new.user_id),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        )

    def test_text(self):
        """
        Tests the type of text attribute
        """
        new = self.value()
        self.assertEqual(
            type(new.text),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        )
