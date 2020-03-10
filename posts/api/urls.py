from django.urls import path

from .views import (
    PostsView, PostDetailView, CommentView, PostCreateView, CategoryView,
    MyPostsView, PostUpdateView, PostDeleteView, ReadingListView
)

urlpatterns = [
    path('posts/', PostsView.as_view(), name='posts'),
    path('posts/<pk>/', PostDetailView.as_view(), name='post-detail'),
    path('add-comment/', CommentView.as_view(), name='add-comment'),
    path('post-create/', PostCreateView.as_view(), name='post-create'),
    path('retrieve-categories/', CategoryView.as_view(),
         name='retrieve-categories'),
    path('my-posts/', MyPostsView.as_view(), name='my-posts'),
    path('my-reading-list/', ReadingListView.as_view(), name='my-reading-list'),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete')
]
