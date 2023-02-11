from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_correct_username(data):
    if data.lower() == 'me':
        raise ValidationError(
            f'Никнэйм пользователя не должен быть {data}'
        )


def validate_year(data):
    if data >= timezone.now().year:
        raise ValidationError(
            'Год выпуска произведения не может быть больше текущего.'
        )


validate_username = UnicodeUsernameValidator()
