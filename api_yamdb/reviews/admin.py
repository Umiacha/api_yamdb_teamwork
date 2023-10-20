from django.contrib import admin

from .models import Title, Category, Review, Genre, Comment, GenreTitle


class GenreTitleInline(admin.StackedInline):
    model = GenreTitle
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "rating",
        "description",
        "category",
    )
    search_fields = ("name",)
    filter_horizontal = ("genre",)
    list_filter = (
        "year",
        "category",
        "genre",
    )
    inlines = (GenreTitleInline,)
    exclude = ("rating",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "text",
        "author",
        "score",
        "pub_date",
    )
    search_fields = ("title",)
    list_filter = ("author",)
    inlines = (CommentInline,)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("review", "text", "author", "pub_date")
    search_fields = ("review",)
    list_filter = ("author",)


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.empty_value_display = "Отсутствует"
