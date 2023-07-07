import re

from django.core.exceptions import ValidationError

from foodgram.settings import PROHIBITED_USERNAMES, VALID_CHARACTERS


def validate_username(username):
    if username.lower() in PROHIBITED_USERNAMES:
        raise ValidationError(
            'Недопустимое имя пользователя.'
        )
    if not bool(re.match(VALID_CHARACTERS, username)):
        raise ValidationError(
            'Некорректные символы в имени пользователя.'
        )
    return username
