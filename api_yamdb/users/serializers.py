from rest_framework import serializers

from api_yamdb.constants import MAX_USERNAME_ROLE_CODE_LENGTH, MAX_EMAIL_LENGTH
from reviews.models import User
from .validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)


class UserCrateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=MAX_USERNAME_ROLE_CODE_LENGTH,
        required=True
    )
    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        required=True
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, value):
        return validate_username(value)
