from django.conf import settings
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.shortcuts import get_object_or_404
from djoser import utils
from djoser.compat import get_user_email
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Follow
from .serializers import FollowSerializer

User = get_user_model()


class MyUserViewSet(UserViewSet):
    http_method_names = ['get', 'post']


class FollowViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    # permission_classes = (permissions.IsAuthenticated,)
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('^user__username', '^following__username')

    # def get_queryset(self):
    #     return self.request.user.follower.all()

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.id)
        serializer.save(user=self.request.user, author=author)

