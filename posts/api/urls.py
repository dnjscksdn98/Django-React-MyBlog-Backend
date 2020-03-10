from django.urls import path

from .views import (
    PostsView, PostView, CommentView, PostCreateView, CategoryView, MyPostsView, PostUpdateView, PostDeleteView
)

urlpatterns = [
    path('posts/', PostsView.as_view(), name='posts'),
    path('posts/<pk>/', PostView.as_view(), name='post-detail'),
    path('add-comment/', CommentView.as_view(), name='add-comment'),
    path('post-create/', PostCreateView.as_view(), name='post-create'),
    path('retrieve-categories/', CategoryView.as_view(),
         name='retrieve-categories'),
    path('my-posts/', MyPostsView.as_view(), name='my-posts'),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete')
]
