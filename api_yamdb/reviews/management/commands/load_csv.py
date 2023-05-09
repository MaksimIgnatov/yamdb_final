import csv
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()

MODELS_TO_CSV = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    User: 'users.csv'
}


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for model, csv_file in MODELS_TO_CSV.items():
            with open(
                os.path.join(settings.BASE_DIR, f'static/data/{csv_file}'),
                'r',
                encoding='utf-8'
            ) as file:
                reader = csv.DictReader(file, delimiter=',')
                model.objects.bulk_create(
                    model(**data) for data in reader
                )
