from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ('Enter file name that contains data which you want to fill the'
            'table. Make sure that file name you input represents concrete '
            'table name in database.')

    def add_arguments(self, parser):
        parser.add_argument('file_names', nargs='+', type=str)

    def handle(self, *args, **options):
        for file_name in options['file_names']:
            with open(f'static/data/{file_name}', 'r') as data_file:
                f_name = file_name.rstrip('.csv').capitalize()
                if f_name.endswith('s'):
                    f_name = file_name[:len(f_name) - 1]
                elif f_name.find('_') != -1:
                    f_name = file_name.replace('_',
                                               ' ').title().replace(' ', '')
                fields = [i for i in data_file.readline().rstrip('\n'
                                                                 ).split(',')]
                values = [j.split(',') for j in
                          [i.rstrip('\n') for i in data_file.readlines()]]
                model_name = eval(f_name)
                bulk_list = [model_name(dict(zip(fields, val)))
                             for val in values]
                model_name.objects.bulk_create(bulk_list)
