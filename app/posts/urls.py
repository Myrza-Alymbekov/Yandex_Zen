from django.urls import path, include

from . import views


urlpatterns = [
    path('posts/', views.PostViewSet.as_view()),
    path('posts/<int:pk>/', views.PostRetrieveUpdateDestroy.as_view()),
    path('posts/<int:post_id>/comment/', views.CommentListCreateAPIView.as_view()),
    path('posts/<int:post_id>/comment/<int:pk>/', views.CommentRetrieveUpdateDestroy.as_view()),
    path('posts/<int:post_id>/status/<int:pk>/', views.StatusRetrieveUpdateDestroyAPIView.as_view()),
    path('posts/<int:post_id>/status/', views.StatusListCreateAPIView.as_view()),
]

