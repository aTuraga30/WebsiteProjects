#standard django import
from django.contrib import admin
#imports the Post model
from .models import Post

#the admin site will register the Post model
admin.site.register(Post)
