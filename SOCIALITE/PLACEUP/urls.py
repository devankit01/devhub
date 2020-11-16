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
    path('update-profile/', update_orgprofile, name='update_orgprofile'),

    path('works/', jobs, name='jobs'),
    path('job-details/<id>/', job_detail, name='job_detail'),
    path('intern-details/', intern_detail, name='intern_detail'),

    path('my-works/',JobHire, name='JobHire'),
    path('add-work',job_add, name='job_add'),
    path('work-view/<id>/',work_view, name='work_view'),


    path('apply_job/<id>/',apply_job, name="apply_job"),
    path('my-applications/',myapplications, name="myapplications"),


    path('select-resume/<id1>/<work>/',select_resume, name="select_resume"),









]
