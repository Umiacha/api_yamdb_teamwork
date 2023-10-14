from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import AdminViewSet, UserViewSet, get_token


users_router_v1 = SimpleRouter()
users_router_v1.register(r'users', AdminViewSet)


urlpatterns = [
    # path('auth/signup/', ...),
    path('auth/token/', get_token),
    path('users/me/', UserViewSet.as_view({'get': 'retrieve',
                                           'patch': 'partial_update'})),
    path('', include(users_router_v1.urls)),
]
