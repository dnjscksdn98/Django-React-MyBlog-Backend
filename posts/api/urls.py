from django.urls import path

from .views import (
    PostsView, PostDetailView, CommentView, CategoryView, UserIdView, UserProfileView
)

urlpatterns = [
    path('posts/', PostsView.as_view(), name='posts'),
    path('posts/<pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<pk>/comments/', CommentView.as_view(), name='create-comment'),
    path('categories/', CategoryView.as_view(), name='get-categories'),
    path('users/id/', UserIdView.as_view(), name='get-user-id'),
    path('users/<pk>/profile/', UserProfileView.as_view(), name='user-profile'),
]
