from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter

from .serializers import UserSerializer


User = get_user_model()


class AdminViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)


class UserViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer

    def get_object(self):
        # return self.request.user  # отключаю пока что, тк нет токенов.
        return User.objects.first()
