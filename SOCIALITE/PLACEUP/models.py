from django.db import models
from django.contrib.auth.models import User
from Django_Socialite.models import Profile
from ckeditor.fields import RichTextField

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


class Work(models.Model):
    TYPE = (('INERNSHIP','INERNSHIP'),('JOB','JOB'))
    EMP = (('Part Time Job','Part Time Job'),('Full Time Job','Full Time Job'))
    Type = models.CharField(max_length=20)
    emp_type = models.CharField(max_length=50)
    work_name = models.CharField(max_length=100)
    company = models.ForeignKey(CompanyProfile, on_delete = models.CASCADE)
    about = RichTextField()
    min_requirement = RichTextField()
    location = models.CharField(max_length=100) # Work from Home , Remote or Delhi, India
    experience_or_time = models.CharField(max_length=10) # Expererience in Job and INtern time in Internship
    tech_stack = models.CharField(max_length=100)
    posted = models.DateField(auto_now_add = True)
    number_of_vacancy = models.CharField(max_length=3)
    status = models.BooleanField(default = True)
    salary_or_stipend = models.CharField(max_length=20)
    applicants = models.ManyToManyField(Profile)
    resume_selected = models.ManyToManyField(Profile, related_name = 'resume_selected')
    hired = models.ManyToManyField(Profile, related_name = 'hired')



