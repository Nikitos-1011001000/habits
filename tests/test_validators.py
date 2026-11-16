from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from habbits_tracker.validators import validate_duration, validate_periodicity


class ValidatorTests(SimpleTestCase):
    def test_duration_max_value(self):
        with self.assertRaises(ValidationError):
            validate_duration(121)

    def test_duration_valid_value(self):
        validate_duration(120)

    def test_periodicity_min_value(self):
        with self.assertRaises(ValidationError):
            validate_periodicity(0)

    def test_periodicity_max_value(self):
        with self.assertRaises(ValidationError):
            validate_periodicity(8)

    def test_periodicity_valid_value(self):
        validate_periodicity(7)
