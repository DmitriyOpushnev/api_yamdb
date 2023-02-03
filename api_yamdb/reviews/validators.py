from django.core.exceptions import ValidationError


def validate_correct_username(data):
    if data == 'me':
        raise ValidationError(
            f'Никнэйм пользователя не должен быть {data}'
        )
