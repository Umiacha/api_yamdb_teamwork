from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import TitleViewSet, ReviewViewSet, CommentViewSet

router = SimpleRouter()
router.register(r"titles", TitleViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>[0-9]+)/rewiews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>[0-9]+)/rewiews/(?P<review_id>[0-9]+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include("users.urls")),
]
