from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from reviews.models import Title, Comment, Review, Genre, Category
from .serializers import (
    TitleSerializer,
    CommentSerializer,
    ReviewSerializer,
    GenreSerializer,
    CategorySerializer,
)
from users.permissions import AdminOrReadOnly, OwnerOrStaffOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "category",
        "genre",
        "name",
        "year",
    )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ["name"]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (OwnerOrStaffOrReadOnly,)
    http_method_names = ["get", "post", "patch", "delete", "head"]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrStaffOrReadOnly,)
    http_method_names = ["get", "post", "patch", "delete", "head"]

    def get_review(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return get_object_or_404(
            Review, pk=self.kwargs.get("review_id"), title=title
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
