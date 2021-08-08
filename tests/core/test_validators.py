from django.core.exceptions import ValidationError
from django.test import TestCase

from LetsCook.core.validators import validate_digits_not_in_string


class ValidateDigitsNotInStringTest(TestCase):
    def test_validator_withNotString_shouldReturn(self):
        result = validate_digits_not_in_string(1)
        self.assertIsNone(result)

    def test_validator_withNoDigitsInString_shouldDoNothing(self):
        result = validate_digits_not_in_string('asd')
        self.assertIsNone(result)

    def test_validator_withDigitsInString_shouldRaise(self):
        with self.assertRaises(ValidationError):
            validate_digits_not_in_string('asd1')
