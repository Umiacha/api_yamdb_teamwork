from django.contrib import admin

from reviews.models import Title, Category


class TitleAdmin(admin.ModelAdmin):
    exclude = ('rating',)


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
