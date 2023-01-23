from django.shortcuts import render
from rest_framework import viewsets, generics

from .models import Author, User
from .serializers import AuthorRegisterSerializer
from .permissions import OwnerOrReadOnlyPermission


class AuthorRegisterAPIView(generics.CreateAPIView):
    """
        API для регистрации пользователей
    """
    queryset = Author.objects.all()
    serializer_class = AuthorRegisterSerializer


class AuthorRetrieveUpdateDestroy(viewsets.ModelViewSet):
    """
        API для детального просмотра, изменения и удаления пользователей
    """
    queryset = Author.objects.all()
    serializer_class = AuthorRegisterSerializer
    lookup_field = 'user__username'
    permission_classes = [OwnerOrReadOnlyPermission, ]


