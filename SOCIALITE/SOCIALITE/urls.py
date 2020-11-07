"""SOCIALITE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Django_Socialite.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup', signup , name = 'signup'),
    path('accounts/signin', signin , name = 'signin'),
    path('user/dashboard', dashboard , name = 'dashboard'),
    path('user/profile', profile , name = 'profile'),
    path('update_profile', update_profile , name = 'update_profile'),

    # Skills urls =>
    path('user/skills', skills , name = 'skills'),
    path('add_skill', add_skill , name = 'add_skill'),
    path('edit_skill/<id>', edit_skill , name = 'edit_skill'),
    path('delete_skill/<key>', delete_skill , name = 'delete_skill'),

    # Certifications urls =>
    path('user/certifications', certifications , name = 'certifications'),
    path('add_certification', add_certification , name = 'add_certification'),
    path('edit_certification/<id>', edit_certification , name = 'edit_certification'),
    path('delete_certification/<id>', delete_certification , name = 'delete_certification'),


    # POST urls =>
    path('user/posts' , posts , name = 'posts'),
    path('add_post', add_post , name = 'add_post'),
    path('edit_post/<id>', edit_post , name = 'edit_post'),
    path('delete_post/<id>', delete_post , name = 'delete_post'),

    path('myresume/', myresume , name = 'myresume'),
    # path('add_resume/', add_resume , name = 'add_resume'),




    # User-Profile
    path('user_profile/<id>', user_profile , name = 'user_profile'),

    # Like
    path('like_dislike_post', like_dislike_post ,name = 'like_dislike_post'),

    # Comment
    path('comment/<id>' , comment_post , name = 'comment_post' ),
    path('delete_comment/<id>' , delete_comment , name = 'delete_comment' ),

    path('user/follow/<id>' , follow , name = 'follow'),

  



    path('logout', logout , name = 'logout'),




]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)