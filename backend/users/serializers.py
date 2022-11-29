from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers


from users.models import Follow

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпоита users."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',  'first_name', 'last_name',
            'is_subscribed',
        )
        # lookup_field = 'username'

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать имя me в качестве имени пользователя.'
            )
        return value

    def get_is_subscribed(self, obj):
        """Подписан ли пользователь на автора."""
        return Follow.objects.filter(user=self.context['request'].user,
                                     author=obj).exists()
