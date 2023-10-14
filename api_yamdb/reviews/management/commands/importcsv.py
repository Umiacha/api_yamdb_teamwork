import csv
import os

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import (
    Title, Category, Genre,
    GenreTitle, Review, Comment, User
)

class Command(BaseCommand):
    help = 'Import data from a CSV file into the Title model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        filename = os.path.basename(csv_file)

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if filename == 'titles.csv':
                    category_id = row[3]
                    category = get_object_or_404(Category, id=category_id)
                    try:
                        object = Title(
                            id=row[0],
                            name=row[1],
                            year=row[2],
                            category=category
                        )
                        object.save()
                    except Exception as e:
                        print("Unable to upload file. "+repr(e))
                if filename == 'category.csv':
                    try:
                        object = Category(
                            id=row[0],
                            name=row[1],
                            slug=row[2],
                        )
                        object.save()
                    except Exception as e:
                        print("Unable to upload file. "+repr(e))
                if filename == 'genre.csv':
                    try:
                        object = Genre(
                            id=row[0],
                            name=row[1],
                            slug=row[2],
                        )
                        object.save()
                    except Exception as e:
                        print("Unable to upload file. "+repr(e))
                if filename == 'genre_title.csv':
                    try:
                        object = GenreTitle(
                            id=row[0],
                            title_id=row[1],
                            genre_id=row[2],
                        )
                        object.save()
                    except Exception as e:
                        print("Unable to upload file. "+repr(e))
                if filename == 'users.csv':
                    try:
                        object = User(
                            id=row[0],
                            username=row[1],
                            email=row[2],
                            role=row[3],
                            bio=row[4],
                            first_name=row[5],
                            last_name=[6]
                        )
                        object.save()
                    except Exception as e:
                        print("Unable to upload file. "+repr(e))
                if filename == 'review.csv':
                    user_id = row[3]
                    author = get_object_or_404(User, id=user_id)
                    try:
                        object = Review(
                            id=row[0],
                            title_id=row[1],
                            text=row[2],
                            author=author,
                            score=row[4],
                            pub_date=row[5],
                        )
                        object.save()
                    except Exception as e:
                        print("Unable to upload file. "+repr(e))
                if filename == 'comments.csv':
                    user_id = row[3]
                    author = get_object_or_404(User, id=user_id)
                    review_id = row[1]
                    review = get_object_or_404(Review, id=review_id)
                    try:
                        object = Comment(
                            id=row[0],
                            review=review,
                            text=row[2],
                            author=author,
                            pub_date=row[4],
                        )
                        object.save()
                    except Exception as e:
                        print("Unable to upload file. "+repr(e))
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
