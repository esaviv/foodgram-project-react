import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_username(username):
    if username.lower() in settings.PROHIBITED_USERNAMES:
        raise ValidationError(
            'Недопустимое имя пользователя.'
        )
    if not bool(re.match(settings.VALID_CHARACTERS, username)):
        raise ValidationError(
            'Некорректные символы в имени пользователя.'
        )
    return username
