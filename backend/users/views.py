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

from .serializers import MyUserSerializer, MyUserCreateSerializer

User = get_user_model()


class MyUserViewSet(UserViewSet):
    http_method_names = ['get', 'post']
