from titles.models import Category, Title, Genre
from reviews.models import Review
from users.models import User

"""Инициализация классов моделей для flake8"""
imported_models = (Category, Genre, Title, Review, User)


def get_object_from_model(key, value):
    return eval(key.rstrip('_id').title()
                ).objects.get(pk=value)


def change_id_to_command(dictionary):
    raw_to_model_field = {
        'author': 'user_id',
        'category': 'category_id'
    }
    to_instance = ('author',)
    for k, v in dictionary.items():
        if k.endswith('_id') or k in raw_to_model_field.keys():
            if k in to_instance:
                tmp_k = raw_to_model_field[k]
                dictionary[k] = get_object_from_model(tmp_k, v)
            else:
                tmp_k = k
                dictionary[k] = get_object_from_model(
                    tmp_k, v).id
    return dictionary
