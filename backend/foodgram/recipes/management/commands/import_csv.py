import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

DATABASES_DICT = {
    Ingredient: 'ingredients.csv',
}

DATA_DIR = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Loads the data from csv files located in static/data folder'

    def handle(self, *args, **options):
        for model, csv_file in DATABASES_DICT.items():
            with open(
                os.path.join(DATA_DIR, csv_file), 'r',
                encoding='utf-8',
            ) as file:
                reader = csv.reader(file)
                next(reader)
                for data in reader:
                    model.objects.get_or_create(
                        name=data[0], measurement_unit=data[1]
                    )
        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))
