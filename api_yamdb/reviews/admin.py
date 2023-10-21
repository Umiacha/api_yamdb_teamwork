from django.contrib import admin

from .models import Title, Category, Review, Genre, Comment, GenreTitle


class GenreTitleInline(admin.StackedInline):
    model = GenreTitle
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Title)
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name",)


@admin.register(Review)
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


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("review", "text", "author", "pub_date")
    search_fields = ("review",)
    list_filter = ("author",)


admin.site.empty_value_display = "Отсутствует"
