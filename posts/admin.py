from django.contrib import admin

from .models import Post, Author, Category, Comment, PostView, UserProfile, Like

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostView)
admin.site.register(UserProfile)
admin.site.register(Like)
