from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import AuthenticationFailed, ParseError
from rest_framework_simplejwt.tokens import AccessToken

from .models import USERS_ROLES
from .serializers import UserSerializer
from .permissions import IsAdminOrSuperuser


User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def get_token(request):
    username = request.data.get("username", None)
    code = request.data.get("confirmation_code", None)
    if not username:
        return Response(
            data={"username": "Поле некорректно или отсутствует!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user = get_object_or_404(User, username=username)
    print(user)
    if not code or code != user.confirmation_code:
        return Response(
            data={"confirmation_code": "Поле некорректно или отсутствует!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(
        data={"token": str(AccessToken.for_user(user))},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    serializer = UserSerializer(data=request.data)
    try:
        user = User.objects.get(
            username=request.data.get("username", None),
            email=request.data.get("email", None),
        )
    except Exception:
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(**serializer.validated_data)
    user.create_confirmation_code()
    user.email_user(
        subject="Код подтверждения", message=user.confirmation_code
    )
    return Response(
        data={"username": user.username, "email": user.email},
        status=status.HTTP_200_OK,
    )


class AdminViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    filter_backends = (SearchFilter,)
    permission_classes = (IsAdminOrSuperuser,)
    search_fields = ("username",)

    def perform_create(self, serializer):
        if "role" in self.request.data:
            users_roles = [role[1] for role in USERS_ROLES]
            if self.request.data["role"] not in users_roles:
                raise ParseError("Такая роль не предусмотрена!")
            serializer.save(role=self.request.data["role"])
        else:
            serializer.save()

    def perform_update(self, serializer):
        if "role" in self.request.data:
            users_roles = [role[1] for role in USERS_ROLES]
            if self.request.data["role"] not in users_roles:
                raise ParseError("Такая роль не предусмотрена!")
            serializer.save(role=self.request.data["role"])
        else:
            serializer.save()

    def update(self, request, *args, **kwargs):
        if "partial" not in kwargs:
            self.http_method_not_allowed(request, *args, **kwargs)
        return super().update(request, *args, **kwargs)


class UserViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        if user.is_anonymous:
            raise AuthenticationFailed(
                "Доступно только авторизованным пользователям!"
            )
        return user
