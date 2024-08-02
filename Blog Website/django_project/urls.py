"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# standard django import
from django.contrib import admin
# importing auth views? Dont know what this does
from django.contrib.auth import views as auth_views
# standard django import
from django.urls import path, include
# imports views from the user app
from users import views as user_views
# imports django settings
from django.conf import settings
# imports static files
from django.conf.urls.static import static

urlpatterns = [
    # path to the admin page
    path('admin/', admin.site.urls),
    # path to the register page , user_views register is the path to the user views
    path('register/', user_views.register, name='register'),
    # path to the profile page, user_views shows the path
    path('profile/', user_views.profile, name='profile'),
    # path to the login page, auth_views is the login view; its seperate because its included in
    # the standard django library
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # path to the logout page, auth_views.LogoutView is a view for the logout page
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # path to the urls for the blog site
    path('', include('blog.urls')),
]

# if the page is in debug mode do this, or something like this...I dont know exactly
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
