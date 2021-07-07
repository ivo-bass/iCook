from django.core.exceptions import ValidationError


def validate_digits_not_in_string(value):
    for char in value:
        if char.isnumeric():
            raise ValidationError(
                message="This field should contain only letters"
            )
