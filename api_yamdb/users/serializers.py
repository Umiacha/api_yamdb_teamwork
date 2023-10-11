from django.contrib.auth import get_user_model
from rest_framework import serializers


USERS_ROLES = ['user', 'moderator', 'admin',]

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)
