from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter


User = get_user_model()


class AdminViewSet(ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)


class UserViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    lookup_field=None  # возможно, определю по-другому, но пользователь никакие аргументы не передает
    
    def get_queryset(self):
        return self.request.user
