import re

from django.core.exceptions import ValidationError


REGEX = re.compile(r'^[\w.@+-]+')
NAME_ERROR = 'Нельзя использовать имя "me"!'
CHARS_ERROR = 'Используйте только цифры, буквы и "@.+-_".'


def validate_username(name):
    "Проверка юзернейма"
    if name == 'me':
        raise ValidationError(NAME_ERROR)
    if not REGEX.fullmatch(name):
        raise ValidationError(CHARS_ERROR)
    if len(name) > 150:
        raise ValidationError(f'Длина name:{name} не должно'
                              f' быть длиннее 254 символа.')
