# django import for render, and a 404 response
from django.shortcuts import render, get_object_or_404
# django import for a mixin that makes sure a user is logged in before accesing other pages
# UserPassesTest mixin makes sure that if a person wants to edit/delete a post, they are the author
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# imports the user model
from django.contrib.auth.models import User
# imports all of the various class views
from django.views.generic import (
    ListView, #lists the posts
    DetailView, #details the post
    CreateView, #creates the post
    UpdateView, #updates the post
    DeleteView #deletes the post
)
# imports the post model
from .models import Post

# dont actually need this, but its a way to list all of the posts using a function


def home(request):
    context = {
        'posts': Post.objects.all() #stores all of the posts in a variable called context
    }
    # returns the home.html template with all of the posts
    return render(request, 'blog/home.html', context)

# class view that lists all of the posts


class PostListView(ListView):
    # instead of calling all of the posts objects, we set the model to post
    model = Post
    # sets the template name instead of the default class template name
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    # similar to the model change
    context_object_name = 'posts'
    # orders all of the posts by reverse date posted
    ordering = ['-date_posted']
    # puts 5 blogs per page
    paginate_by = 5


# class view thats lists all of a particular posts from a specific user
class UserPostListView(ListView):
    # sets the model to Post instead of object
    model = Post
    # sets the template name instead of using a default
    # <app>/<model>_<viewtype>.html
    template_name = 'blog/user_posts.html'
    # similar to the model above idk
    context_object_name = 'posts'
    # paginates the page by 5 per page
    paginate_by = 5

    # no clue what this does
    def get_queryset(self):
        # filters the user by username
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # returns the posts by newest posts first
        return Post.objects.filter(author=user).order_by('-date_posted')

# class view for the detail post


class PostDetailView(DetailView):
    # sets the model to post instead of object
    model = Post

# class view for the create post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
