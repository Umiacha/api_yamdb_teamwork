from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import TitleViewSet

router = SimpleRouter()
router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls))
]
