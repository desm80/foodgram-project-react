from django.conf import settings
from django.contrib.auth import get_user_model, update_session_auth_hash
from djoser import utils
from djoser.compat import get_user_email
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, \
    ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import MyUserSerializer, CustomUserCreateSerializer

User = get_user_model()


class MyUserViewSet(CreateModelMixin, RetrieveModelMixin,
                  ListModelMixin, GenericViewSet):
# class MyUserViewSet(UserViewSet):
    """Описание логики работы АПИ для эндпоинта users."""

    queryset = User.objects.all()
    # serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        elif self.action == "set_password":
            return SetPasswordSerializer
        else:
            return MyUserSerializer

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

    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
