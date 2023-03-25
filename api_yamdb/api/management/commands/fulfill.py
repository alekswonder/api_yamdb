import csv

from django.core.management.base import BaseCommand

from ._utils import change_id_to_command
from titles.models import Category, Genre, Title, GenreTitle
from reviews.models import Review, Comment
from users.models import User

"""Инициализация классов моделей для flake8"""
imported_models = (Category, Genre, Title, GenreTitle, Review, Comment, User)


class Command(BaseCommand):
    help = ('Enter file name that contains data which you want to fill the'
            'table. Make sure that file name you input represents concrete '
            'table name in database and has not its extension (csv).')

    def add_arguments(self, parser):
        parser.add_argument('file_names', nargs='+', type=str)

    def handle(self, *args, **options):
        for file_name in options['file_names']:
            with open(f'static/data/{file_name}.csv', 'r',
                      encoding='utf-8') as data_file:
                f_name = file_name.capitalize()
                if f_name.endswith('s'):
                    f_name = f_name[:len(f_name) - 1]
                if f_name.find('_') != -1:
                    f_name = f_name.replace('_',
                                            ' ').title().replace(' ', '')

                data = [i for i in csv.DictReader(data_file,
                                                  delimiter=',',
                                                  quotechar='"')]

                data = list(map(lambda x: change_id_to_command(x), data))
                bulk_list = [eval(f_name)(**kwargs) for kwargs in data]
                eval(f_name).objects.bulk_create(bulk_list)
