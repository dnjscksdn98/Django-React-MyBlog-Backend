from django.urls import path

from .views import PostsView, PostView, CommentView

urlpatterns = [
    path('posts/', PostsView.as_view(), name='posts'),
    path('posts/<pk>/', PostView.as_view(), name='post-detail'),
    path('add-comment/', CommentView.as_view(), name='add-comment')
]
