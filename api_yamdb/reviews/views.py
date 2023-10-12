import csv

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import (
    Title, Category, Genre, GenreTitle,
    Review, Comment, User
)


def upload_csv(request):
    "Функция для импорта CSV в базу данных"
    data = {}
    if "GET" == request.method:
        return render(request, "reviews/upload.html", data)
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Файл не является CSV')
            return HttpResponseRedirect(reverse("reviews:upload_csv"))
        if csv_file.multiple_chunks():
            messages.error(
                request, "Загруженый файл слишком большой (%.2f MB). " % (
                    csv_file.size/(1000*1000),
                )
            )
            return HttpResponseRedirect(reverse("reviews:upload_csv"))
        file_data = csv_file.read().decode("utf-8")
        csv_reader = csv.reader(file_data.splitlines(), quoting=csv.QUOTE_ALL)
        next(csv_reader)
        for row in csv_reader:
            if csv_file.name == 'titles.csv':
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
                    messages.error(request, "Невозможно загрузить файл. "+repr(e))
                    pass
            if csv_file.name == 'category.csv':
                try:
                    object = Category(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    )
                    object.save()
                except Exception as e:
                    messages.error(request, "Невозможно загрузить файл. "+repr(e))
                    pass
            if csv_file.name == 'genre.csv':
                try:
                    object = Genre(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    )
                    object.save()
                except Exception as e:
                    messages.error(request, "Невозможно загрузить файл. "+repr(e))
                    pass
            if csv_file.name == 'genre_title.csv':
                try:
                    object = GenreTitle(
                        id=row[0],
                        title_id=row[1],
                        genre_id=row[2],
                    )
                    object.save()
                except Exception as e:
                    messages.error(request, "Невозможно загрузить файл. "+repr(e))
                    pass
            if csv_file.name == 'review.csv':
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
                    messages.error(request, "Невозможно загрузить файл. "+repr(e))
                    pass
            if csv_file.name == 'user.csv':
                try:
                    object = User(
                        id=row[0],
                        title_id=row[1],
                        text=row[2],
                        author=author,
                        score=row[4],
                        pub_date=row[5],
                    )
                    object.save()
                except Exception as e:
                    messages.error(request, "Невозможно загрузить файл. "+repr(e))
                    pass
    except Exception as e:
        messages.error(request, "Невозможно загрузить файл. "+repr(e))
    return HttpResponseRedirect(reverse("reviews:upload_csv"))
