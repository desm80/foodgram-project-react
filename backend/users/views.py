from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, \
    ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer, CustomUserCreateSerializer

User = get_user_model()


class UserViewSet(CreateModelMixin, RetrieveModelMixin,
                  ListModelMixin, GenericViewSet):
    """Описание логики работы АПИ для эндпоинта users."""

    queryset = User.objects.all()
    # serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        else:
            return UserSerializer

    @action(methods=['get'],
            permission_classes=[IsAuthenticated],
            detail=False)
    def me(self, request, *args, **kwargs):
        """Описание логики работы АПИ для эндпоинта users/me."""

        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            if user.is_user and request.data.get('role') != 'User':
                return Response(serializer.data)
            serializer.save()
        return Response(serializer.data)
