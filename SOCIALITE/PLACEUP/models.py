from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CompanyProfile(models.Model):
    ''' MOdel for Company Profile '''
    company_type = models.CharField(max_length = 30)
    company_specialization = models.CharField(max_length = 30)
    phone = models.CharField(max_length = 20)
    company_logo = models.ImageField(upload_to = "company_logo")
    about_company = models.TextField(max_length=300)
    company_site = models.CharField(max_length = 50)
    username = models.OneToOneField(User, on_delete=models.CASCADE)
