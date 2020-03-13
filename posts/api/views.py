from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
)
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse

from posts.models import Post, PostView, Comment, Author, Category
from .serializers import PostSerializer, CategorySerializer, PostViewSerializer

from functools import wraps
import jwt


def get_token_auth_header(request):
    # Obtains the Access Token from the Authorization Header

    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]
    return token


def requires_scope(required_scope):
    # Determines if the required scope is present in the Access Token Args:
    # required_scope (str): The scope required to access the resource

    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, verify=False)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse(
                {'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response
        return decorated
    return require_scope


class PostsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer

    def get_object(self):
        try:
            post = Post.objects.get(id=self.kwargs.get('pk'))
            if self.request.user.is_authenticated:
                PostView.objects.get_or_create(
                    user=self.request.user, post=post)
            return post

        except ObjectDoesNotExist:
            raise Http404('This post does not exist.')


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

        selected_categories = request.data.get('selectedCategories')
        if len(selected_categories) < 1:
            return Response({'message': 'You must select at least one category.'}, status=HTTP_404_NOT_FOUND)

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

            for category in selected_categories:
                selected_category = Category.objects.get(title=category)
                created_post.category.add(selected_category)
            created_post.save()

            return Response({'message': 'Successfully created a new post.', 'id': created_post.id}, status=HTTP_201_CREATED)

        else:
            return Response({'message': 'You must login first.'}, status=HTTP_401_UNAUTHORIZED)


class CategoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class MyPostsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(author__user=self.request.user)


class PostUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def put(self, request, *args, **kwargs):
        form = request.data.get('formData', None)
        if form is None:
            return Response({'message': 'Invalid data received.'}, status=HTTP_404_NOT_FOUND)

        updated_post_id = request.data.get('updateId', None)
        if updated_post_id is None:
            return Response({'message': 'Invalid data received.'}, status=HTTP_404_NOT_FOUND)

        selected_categories = request.data.get('selectedCategories')
        if len(selected_categories) < 1:
            return Response({'message': 'You must select at least one category.'}, status=HTTP_404_NOT_FOUND)

        if request.user.is_authenticated:
            updated_post = Post.objects.get(id=updated_post_id)
            updated_post.title = form['title']
            updated_post.overview = form['overview']
            updated_post.content = form['content']
            updated_post.save()

            # update categories
            selected_categories_list = []
            for category in selected_categories:
                selected_categories_list.append(
                    Category.objects.get(title=category))
            updated_post.category.set(selected_categories_list)

            return Response({'message': 'Successfully updated your new post.', 'id': updated_post.id}, status=HTTP_201_CREATED)

        else:
            return Response({'message': 'You must login first.'}, status=HTTP_401_UNAUTHORIZED)


class PostDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()


class ReadingListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostViewSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return PostView.objects.filter(user=self.request.user)

        return PostView.objects.none()
