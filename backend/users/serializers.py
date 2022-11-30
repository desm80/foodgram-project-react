from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer, SetPasswordSerializer

from users.models import Follow

User = get_user_model()


class MyUserSerializer(UserSerializer):
    """Сериализатор для эндпоита users."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',  'first_name', 'last_name',
            'is_subscribed',
        )
        # lookup_field = 'username'

    def get_is_subscribed(self, obj):
        """Подписан ли пользователь на автора."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=self.context['request'].user,
                                     author=obj).exists()


class MyUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания модели User."""
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
