from django.contrib import admin

from reviews.models import Title, Category, Review, Genre, Comment, GenreTitle


class TitleAdmin(admin.ModelAdmin):
    exclude = ("rating",)


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Comment)
