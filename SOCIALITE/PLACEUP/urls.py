from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('signup/', orgsignup, name='orgsignup'),
    path('signin/', orgsignin, name='orgsignin'),
    path('logout/', orglogout, name='orglogout'),


    path('company-profile/', orgprofile, name='orgprofile'),
    path('works/', jobs, name='jobs'),






]
