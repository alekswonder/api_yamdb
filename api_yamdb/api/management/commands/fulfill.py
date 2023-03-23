import csv

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from titles.models import (Title, GenreTitle, Review, Comment,
                           Genre, User, Category)


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
                    f_name = file_name[:len(f_name) - 1].capitalize()
                if f_name.find('_') != -1:
                    f_name = file_name.replace('_',
                                               ' ').title().replace(' ', '')
                data = [
                    i for i in csv.DictReader(
                        data_file,
                        delimiter=',',
                        quotechar='"'
                    )
                ]
                try:
                    if f_name == Title.__name__:
                        for kwargs in data:
                            eval(f_name).objects.create(
                                id=kwargs['id'],
                                name=kwargs['name'],
                                year=kwargs['year'],
                                category=Category.objects.get(
                                    pk=kwargs['category_id'])
                            )
                    elif f_name == GenreTitle.__name__:
                        for kwargs in data:
                            eval(f_name).objects.create(
                                id=kwargs['id'],
                                genre=Genre.objects.get(pk=kwargs['genre_id']),
                                title=Title.objects.get(pk=kwargs['title_id']),
                            )
                    elif f_name == Review.__name__:
                        for kwargs in data:
                            eval(f_name).objects.create(
                                id=kwargs['id'],
                                title=Title.objects.get(pk=kwargs['title_id']),
                                text=kwargs['text'],
                                author=User.objects.get(pk=kwargs['author']),
                                score=kwargs['score'],
                                pub_date=kwargs['pub_date']
                            )
                    elif f_name == Comment.__name__:
                        for kwargs in data:
                            eval(f_name).objects.create(
                                id=kwargs['id'],
                                review=Review.objects.get(
                                    pk=kwargs['review_id']
                                ),
                                text=kwargs['text'],
                                author=User.objects.get(pk=kwargs['author']),
                                pub_date=kwargs['pub_date']
                            )
                    else:
                        bulk_list = [eval(f_name)(**kwargs) for kwargs in data]
                        eval(f_name).objects.bulk_create(bulk_list)
                except ObjectDoesNotExist:
                    print(f'{f_name} with id:{kwargs["id"]} has problems with'
                          f' its foreign key')
                except IntegrityError:
                    print(f'{f_name} with id:{kwargs["id"]} already exists')
