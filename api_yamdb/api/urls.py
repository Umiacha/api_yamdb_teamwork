from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
    GenreViewSet,
    CategoryViewSet,
)

router = SimpleRouter()
router.register(r"titles", TitleViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>[0-9]+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"categories", CategoryViewSet, basename="categories")


urlpatterns = [
    path("v1/", include("users.urls")),
    path("v1/", include(router.urls)),
]
