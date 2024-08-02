# Basic django import
from django.urls import path
from .views import (
    PostListView, #Lists all of the posts
    PostDetailView, #Observes the post in more detail, and provides the option to update/delete
    PostCreateView, #Class view to create a post
    PostUpdateView, #Updates the post
    PostDeleteView, #Deltes the post
    UserPostListView #Lists the all the posts from a particular user
)
from . import views #imports the views we listed so we can use them

urlpatterns = [
    # url for the list view; all we do is list the posts, and redirect to blog home
    path('', PostListView.as_view(), name='blog-home'),
    # url for any posts by a particular user...redirect to user/username with the user-posts name
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    # url for a particular posts details..redirect to post/post int with the post-detail name
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # url for any new posts...hard coded url with the post-create name
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    # url for the update with post/int for the post/update with the post-update name
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # url for the delete with post/int for the post/delete with the post-delete name
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # url for the about page..this isn't a class view
    path('about/', views.about, name='blog-about'),
]


# <app>/<model>_<viewtype>.html
# blog/post_list.html
