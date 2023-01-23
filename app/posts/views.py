from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

import telebot
from rest_framework.response import Response

from accounts.models import Author
from .models import Post, Comment, Status
from .permissions import IsStaffOrOwnerPermission, StatusOrReadOnlyPermission
from .serializers import PostSerializer, CommentSerializer, StatusSerializer

bot = telebot.TeleBot('5607209879:AAEkLq6k2EPEdLzwE4J14mj1REdEIXqjg3Q', parse_mode=None)


class PostPagePagination(PageNumberPagination):
    page_size = 3


def send_telegram_message(chat_id_list, message):
    for chat_id in chat_id_list:
        bot.send_message(chat_id, message)


class PostViewSet(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsStaffOrOwnerPermission, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['text', ]
    search_fields = ['text', ]
    ordering_fields = ['text', ]
    pagination_class = PostPagePagination

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user.author)
            try:
                author = Author.objects.get(user=self.request.user)
                bot.send_message(author.telegram_chat_id, f' Пост был создан!')
            except:
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsStaffOrOwnerPermission, ]


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsStaffOrOwnerPermission, ]
    pagination_class = PostPagePagination

    def get_queryset(self):
        return super().get_queryset().filter(post_id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            post_id=self.kwargs.get('post_id')
        )


class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsStaffOrOwnerPermission, ]

    def get_queryset(self):
        return super().get_queryset().filter(post_id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            post_id=self.kwargs.get('post_id')
        )


class StatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [StatusOrReadOnlyPermission, ]

    def get_queryset(self):
        return super().get_queryset().filter(post_id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            post_id=self.kwargs.get('post_id')
        )


class StatusRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [StatusOrReadOnlyPermission, ]

    def get_queryset(self):
        return super().get_queryset().filter(post_id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            post_id=self.kwargs.get('post_id')
        )
