import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_username(username):
    if username.lower() in settings.PROHIBITED_USERNAMES:
        raise ValidationError(
            'Недопустимое имя пользователя.'
        )
    invalid_chars = re.sub(settings.VALID_CHARS, '', username)
    if invalid_chars != '':
        raise ValidationError(
            f'Некорректные символы в имени пользователя:'
            f' {", ".join(set(invalid_chars))}'
        )
    return username
