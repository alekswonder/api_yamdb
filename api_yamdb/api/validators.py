import re
from datetime import datetime

from django.core.exceptions import ValidationError

REGEX = re.compile(r'^[\w.@+-]+')
NAME_ERROR = 'Нельзя использовать имя "me"!'
CHARS_ERROR = 'Используйте только цифры, буквы и "@.+-_".'
YEAR_ERROR = 'Проверьте, что год создания произведения: {}, корректен'
SCORE_ERROR = 'Недопустимое значение, {} должен быть от 1 до 10.'


def validate_username(name):
    """Проверка username"""
    if name == 'me':
        raise ValidationError(NAME_ERROR)
    if not REGEX.fullmatch(name):
        raise ValidationError(CHARS_ERROR)


def validate_year(value):
    """Проверка года создание произведения"""
    if datetime.utcnow().year < value:
        raise ValidationError(YEAR_ERROR.format(value))
