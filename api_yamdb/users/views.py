from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import AdminSerializer, UserSerializer


User = get_user_model()


def get_expiration_time():
    return int(
        (datetime.now() + timedelta(
            **settings.JWT_ACCESS_LIFETIME
        )).timestamp()
    )


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def get_token(request):
#     username = request.data.get('username', None)
#     confirmation_code = request.data.get('confirmation_code', None)
#     if not username:
#         return Response(
#             data={"username": "Отсутствует поле или оно некорректно!"},
#             status=status.HTTP_400_BAD_REQUEST
#         )
#     try:
#         user = User.objects.get(username=username)
#     except User.DoesNotExist:
#         raise NotFound('Пользователь не найден!')

#     # Пока почта не настроена, confirmation_code всегда должен быть 1!
#     if not confirmation_code or confirmation_code != '1':
#         return Response(
#             data={
#                 "confirmation_code": "Отсутствует поле или оно некорректно!"
#             },
#             status=status.HTTP_400_BAD_REQUEST
#         )
#     user_token = jwt.encode(
#         payload={
#             'exp': get_expiration_time(),
#             'uid': user.id,
#         },
#         key=settings.SECRET_KEY,
#         algorithm='HS256'
#     )
#     return Response(data={'token': user_token}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    username = request.data.get('username', None)
    code = request.data.get('confirmation_code', None)
    if not username:
        return Response(data={'username': 'Поле некорректно или отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
    if not code or code != '1':  # EmailBackend скоро будет...
        return Response(data={'confirmation_code': 'Поле некорректно или отсутствует!'}, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=username)
    return Response(data={'token': str(AccessToken.for_user(user))}, status=status.HTTP_200_OK)


class AdminViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)


class UserViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
