from django.core.exceptions import ValidationError


def validate_digits_not_in_string(value):
    """
    Custom validator which validates
    only alphabetic characters in the given string value
    """
    if not isinstance(value, str):
        return
    for char in value:
        if char.isnumeric():
            raise ValidationError(
                message="This field should contain only letters"
            )
