from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
)
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from posts.models import Post, Comment, Author, Category
from .serializers import PostSerializer, CategorySerializer


class PostsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class CommentView(APIView):
    def post(self, request, *args, **kwargs):
        comment = request.data.get('comment', None)
        post_id = request.data.get('blogId', None)

        if comment is None:
            return Response({'message': 'Invalid comment received.'}, status=HTTP_404_NOT_FOUND)

        if post_id is None:
            return Response({'message': 'This blog does not exist.'}, status=HTTP_404_NOT_FOUND)

        try:
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist:
            raise Http404('This blog does not exist.')

        if request.user.is_authenticated:
            new_comment = Comment(
                user=request.user,
                content=comment,
                post=post
            )
            new_comment.save()

            post.comments.add(new_comment)
            post.save()

            return Response({'message': 'Successfully submitted a comment.'}, status=HTTP_201_CREATED)

        else:
            return Response({'message': 'You must login first.'}, status=HTTP_401_UNAUTHORIZED)


class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        form = request.data.get('formData', None)
        if form is None:
            return Response({'message': 'Invalid data received.'}, status=HTTP_404_NOT_FOUND)

        if request.user.is_authenticated:
            current_author, created = Author.objects.get_or_create(
                user=request.user)

            created_post = Post(
                title=form['title'],
                overview=form['overview'],
                author=current_author,
                thumbnail=form['thumbnail'],
                content=form['content']
            )
            created_post.save()
            created_post.category.add(form['category'])
            created_post.save()
            return Response({'message': 'Successfully created a new post.', 'id': created_post.id}, status=HTTP_201_CREATED)

        else:
            return Response({'message': 'You must login first.'}, status=HTTP_401_UNAUTHORIZED)


class CategoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
