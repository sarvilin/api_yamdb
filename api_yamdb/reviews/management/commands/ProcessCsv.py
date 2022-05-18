import csv
import os.path

from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import (
    User, Category, Title, Review,
    Comments, Genre, GenreTitle
)

TABLES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title',
    Review: 'review.csv',
    Comments: 'comments.csv',
}


class Command(BaseCommand):
    """Экспорт из csv файлов в нашу базу данных."""

    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, 'static', 'data',
                               'users.csv'), 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if row[0] == 'id':
                    continue
                User.objects.create(id=int(row[0]),
                                    username=row[1],
                                    email=row[2],
                                    role=row[3])

        with open(os.path.join(settings.BASE_DIR, 'static', 'data',
                               'category.csv'), 'r', encoding="utf-8") as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if row[0] == 'id':
                    continue
                Category.objects.create(name=row[1], slug=row[2])

        with open(os.path.join(settings.BASE_DIR, 'static', 'data',
                               'titles.csv'), 'r', encoding="utf-8") as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if row[0] == 'id':
                    continue
                Title.objects.create(
                    name=row[1],
                    year=row[2],
                    category=Category.objects.get(pk=int(row[3]))
                )

        with open(os.path.join(settings.BASE_DIR, 'static', 'data',
                               'review.csv'), 'r', encoding="utf-8") as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if row[0] == 'id':
                    continue
                Review.objects.create(
                    title_id=int(row[1]),
                    text=row[2],
                    author=User.objects.get(pk=int(row[3])),
                    score=row[4], pub_date=row[5]
                )

        with open(os.path.join(settings.BASE_DIR, 'static', 'data',
                               'comments.csv'), 'r', encoding="utf-8") as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if row[0] == 'id':
                    continue
                Comments.objects.create(
                    review_id=int(row[1]),
                    text=row[2],
                    author=User.objects.get(pk=int(row[3])),
                    pub_date=[4]
                )

        with open(os.path.join(settings.BASE_DIR, 'static', 'data',
                               'genre.csv'), 'r', encoding="utf-8") as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if row[0] == 'id':
                    continue
                Genre.objects.create(name=row[1], slug=row[2])

        with open(os.path.join(settings.BASE_DIR, 'static', 'data',
                               'genre_title.csv'), 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if row[0] == 'id':
                    continue
                GenreTitle.objects.create(title_id=int(row[1]),
                                          genre_id=int(row[2]))
