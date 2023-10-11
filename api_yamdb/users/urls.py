from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import AdminViewSet, UserViewSet


users_router_v1 = SimpleRouter()
users_router_v1.register('users', AdminViewSet)


urlpatterns = [
    path('auth/signup/', ...),  # регистрируем уже лежащего в БД пользователя
    path('auth/token/', ...),  # даем зарегистрированному пользователю jwt-токен
    path('users/me', UserViewSet.as_view()),
    path('', include(users_router_v1.urls)),
]
