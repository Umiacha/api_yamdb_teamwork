import jwt

from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header
)
from rest_framework.exceptions import AuthenticationFailed


User = get_user_model()


class JWTAuthentification(BaseAuthentication):
    AUTH_HEADER_PREFIX = 'Bearer'

    def authenticate(self, request):
        request.user = None
        auth_header = get_authorization_header(request).split()

        if not auth_header or len(auth_header) == 1 or len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix != self.AUTH_HEADER_PREFIX:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                'Время жизни токена истекло. Обновите токен!'
            )
        except Exception:
            raise AuthenticationFailed(
                'Отказ в доступе: невозможно декодировать токен!'
            )

        try:
            user = User.objects.get(pk=payload['uid'])
        except User.DoesNotExist:
            raise AuthenticationFailed(
                'Пользователь, соответствующий токену не найден!'
            )

        if not user.is_active:
            raise AuthenticationFailed(
                'Данный пользователь деактивирован!'
            )

        return (user, token)
