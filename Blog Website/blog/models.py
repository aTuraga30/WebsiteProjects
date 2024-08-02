# standard django import
from django.db import models
# imports the timezone so we can custom set what time a post was created
from django.utils import timezone
# imports the user model
from django.contrib.auth.models import User
# don't know what this does
from django.urls import reverse

# creates a Post class, which we use a ton


class Post(models.Model):
    # sets a title of the post to a character field with a length of 100
    title = models.CharField(max_length=100)
    # sets the content field as a text field with no set limit
    content = models.TextField()
    # sets the date posted and is a date time field which sets the timezone
    date_posted = models.DateTimeField(default=timezone.now)
    # sets the author with a "Foreign Key"? with the User model and if on_delete, then it'll
    # either delete the user and the posts or just the user, i cant remeber
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # we're supposed to do a dunder function
    def __str__(self):
        return self.title

    # don't know what this does
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
