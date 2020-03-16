from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from ckeditor.fields import RichTextField

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @property
    def reading_list(self):
        return PostView.objects.filter(user=self.user)

    @property
    def my_posts(self):
        return Post.objects.filter(author__user=self.user)


class Author(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    profile_image = models.ImageField()

    def __str__(self):
        return self.user.username


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)

    # reply

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    thumbnail = models.ImageField(blank=True, null=True)
    category = models.ManyToManyField('Category')
    featured = models.BooleanField(default=False)
    content = RichTextField()
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    # likes

    def __str__(self):
        return self.title

    @property
    def comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()
