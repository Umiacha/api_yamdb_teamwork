from django.contrib.auth import get_user_model
import jwt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import NotFound

from .serializers import UserSerializer


User = get_user_model()


@api_view(['POST'])
def get_token(request):
    username = request.data.get('username', None)
    confirmation_code = request.data.get('confirmation_code', None)
    if not username:
        return Response(data={"username": "Отсутствует поле или оно некорректно!"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise NotFound('Пользователь не найден!')
    # Пока почта не настроена, confirmation_code всегда должен быть 1!
    if not confirmation_code or confirmation_code != 1:
        return Response(data={"confirmation_code": "Отсутствует поле или оно некорректно!"}, status=status.HTTP_400_BAD_REQUEST)
    user_token = jwt.encode(
        payload={'uid': user.id},  # Тут 100% будет "exp" со значением из настроек, но... Что еще?
        key='secret',  # думаю, надо будет это как-то поменять!
        algorithm='HS256'
    )
    return Response(data={'token': user_token}, status=status.HTTP_200_OK)


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
