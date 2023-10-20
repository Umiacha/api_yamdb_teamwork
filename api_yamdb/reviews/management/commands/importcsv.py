import csv
import os
from django.core.management.base import BaseCommand, CommandError
from reviews.models import (
    Title,
    Category,
    Genre,
    GenreTitle,
    User,
    Review,
    Comment,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def create_title(self, row):
        category = Category.objects.get(id=row[3])
        return Title(id=row[0], name=row[1], year=row[2], category=category)

    def create_category(self, row):
        return Category(id=row[0], name=row[1], slug=row[2])

    def create_genre(self, row):
        return Genre(id=row[0], name=row[1], slug=row[2])

    def create_genre_title(self, row):
        genre = Genre.objects.get(id=row[0])
        title = Title.objects.get(id=row[1])
        return GenreTitle(genre=genre, title=title)

    def create_user(self, row):
        return User(id=row[0], email=row[1], password=row[2])

    def create_review(self, row):
        user = User.objects.get(id=row[1])
        title = Title.objects.get(id=row[2])
        return Review(
            id=row[0], user=user, title=title, text=row[3], score=row[4]
        )

    def create_comment(self, row):
        user = User.objects.get(id=row[1])
        review = Review.objects.get(id=row[2])
        return Comment(id=row[0], user=user, review=review, text=row[3])

    def import_data(self, reader, object_creator):
        for row in reader:
            try:
                obj = object_creator(row)
                obj.save()
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR("Невозможно импортировать. " + repr(e))
                )
                continue

    def handle(self, *args, **options):
        filename_to_creator_function = {
            "titles.csv": self.create_title,
            "category.csv": self.create_category,
            "genre.csv": self.create_genre,
            "genre_title.csv": self.create_genre_title,
            "users.csv": self.create_user,
            "review.csv": self.create_review,
            "comments.csv": self.create_comment,
        }

        csv_file = options["csv_file"]

        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)

                try:
                    filename = os.path.basename(csv_file)
                    object_creator = filename_to_creator_function[filename]
                except KeyError:
                    raise CommandError(f'Не найден файл "{filename}"')

                self.import_data(reader, object_creator)
        except Exception as e:
            raise CommandError(f"Невозможно открыть файл: {str(e)}")

        self.stdout.write(self.style.SUCCESS("Дата успешно импортирована"))
