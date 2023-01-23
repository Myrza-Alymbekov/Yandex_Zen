from django.shortcuts import render
from rest_framework import viewsets, generics

from .models import Author, User
from .serializers import AuthorRegisterSerializer
from .permissions import OwnerOrReadOnlyPermission


class AuthorRegisterAPIView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorRegisterSerializer


class AuthorRetrieveUpdateDestroy(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorRegisterSerializer
    lookup_field = 'user__username'
    permission_classes = [OwnerOrReadOnlyPermission, ]


