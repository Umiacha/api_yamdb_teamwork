from django.contrib import admin

from .models import (
    Title, Category, Review,
    Genre, Comment
)


class TitleAdmin(admin.ModelAdmin):
    exclude = ('rating',)


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Comment)
