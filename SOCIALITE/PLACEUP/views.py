from .models import *
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from SOCIALITE.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

# For html content sending
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.


def index(request):
    return render(request, 'placeup/index.html')


def orgsignup(request):
    if request.method == "POST":
        if request.POST['pass1'] == request.POST['pass2']:
            try:
                email = request.POST['email']
                # email = email[0:-10]
                user = User.objects.filter(email=email)
                if len(user) == 0:
                    raise User.DoesNotExist
                return render(request, 'placeup/accounts/signup.html', {'msg': 'Email already exists 🔑', 'c': 'red'})
            except User.DoesNotExist:
                username = request.POST['email'][0:-10]
                user_obj = User.objects.create_user(first_name=request.POST['cname'], last_name=" ",
                                                    username=username, password=request.POST['pass1'], email=request.POST['email'])
                print(user_obj)
                user_obj.save()
                new_prof = CompanyProfile(username=user_obj, company_type = request.POST['type'], company_specialization = request.POST['typeone'], phone = "", company_logo = "", about_company = "", company_site = "")
                new_prof.save()
                print(new_prof)
                subject = 'Account Activation'
                message = "HI "
                recepient = [email]
                send_mail(subject, message, EMAIL_HOST_USER, recepient, fail_silently = False)
                print('Email ok')
                return redirect('orgsignin')

        else:
            return render(request, 'placeup/accounts/signup.html', {'msg_pass': "Password do not matched ❌"})
    else:
        return render(request, 'placeup/accounts/signup.html')
    return render(request, 'placeup/accounts/signup.html')


# def orgsignin(request):
#     return render(request, 'placeup/accounts/signin.html')

# def orgsignin(request):

#     if request.method == 'POST':
#         try:
#             # Check User in DB
#             uname = request.POST['username']
#             print(uname)
#             uname = uname[0:-10]
#             print(uname)
#             pwd = request.POST['pass1']
#             print(uname, pwd)
#             ud = User.objects.get(username=uname)
#             dd = CompanyProfile.objects.get(username = ud)
#             user_authenticate = auth.authenticate(username=uname, password=pwd)
#             if user_authenticate is not None:
#                 auth.login(request, user_authenticate)
#                 request.session['username'] = uname
#                 print('Successfully Login')
#                 return redirect('orgprofile')

#             else:
#                 print('Login Failed')
#                 return render(request, 'placeup/accounts/signin.html', {"msg": "Invalid Credentials ❌"})
#         except:
#             return render(request, 'placeup/accounts/signin.html')
#     return render(request, 'placeup/accounts/signin.html')


def orglogout(request):
    try:
        del request.session['username']
    except:
        pass
    return redirect('/')


def orgprofile(request):
    obj = User.objects.get(username=request.session['username'])
    user = User.objects.get(username=obj)
    company_profile = CompanyProfile.objects.get(username = user)
    print(company_profile)
    return render(request, 'placeup/profile.html',{'profile':company_profile})


def jobs(request):
    try:
        if request.session['username']:
            data = Work.objects.filter(status = True)
            print(data)
            data = data[::-1]
            return render(request, 'placeup/jobs-intern-plateform.html',{'data':data})
    except:
        return HttpResponse('Error 404')

def job_detail(request,id):
    try:
        if request.session['username']:
            data = Work.objects.get(id=id)
            print(data)
            if data.Type == 'Job':
                print('Job')
                return render(request, 'placeup/job-detail.html',{'data':data})

            elif data.Type == 'Internship':
                print('Internship')
                return render(request, 'placeup/intern-detail.html',{'data':data})

            else:
                return HttpResponse('Error 404')
    except:
        return HttpResponse('Error 404')

def intern_detail(request):
    return render(request, 'placeup/intern-detail.html')

def update_orgprofile(request):
    obj = User.objects.get(username=request.session['username'])
    print(obj)
    user = User.objects.get(username=obj)

    cprofile = CompanyProfile.objects.get(username = user)
    specialization = request.POST['csp']
    phone = request.POST['phone']
    site = request.POST['csite']
    logo = request.FILES.get('clogo')
    about = request.POST['about']
    print(cprofile,specialization,phone,site,logo,about)    
    cprofile.company_specialization = specialization
    cprofile.phone = phone
    if logo:
        cprofile.company_logo = logo
    cprofile.company_site = site
    cprofile.about_company = about
    cprofile.save()
    print(cprofile)
    return redirect('orgprofile')
    

def orgjob(request):
    return render(request,'placeup/org_job_intern.html')

def JobHire(request):
    try:
        if request.session['username']:
            user = User.objects.get(username = request.session['username'])
            company = CompanyProfile.objects.get(username = user)
            works = Work.objects.filter(company = company)
            works = works[::-1]
            print(works)
        return render(request,'placeup/org_job_.html',{'works':works})
    except:
        return HttpResponse('Error 404')

def job_add(request):
    if request.method=="POST":
        Type=request.POST.get('type')
        print(Type)
        about=request.POST.get('about')
        print(about)
        salary=request.POST.get('salary')
        print(salary)
        location=request.POST.get('location')
        print(location)
        employee=request.POST.get('Employement_type')
        print(employee)
        experience=request.POST.get('Experience')
        print(experience)
        tech_need=request.POST.get('tech_need')
        print(tech_need)
        status=request.POST.get('status')
        print(status)
        minimum_req=request.POST.get('minimum_requirement')
        print(minimum_req)
        vacancy=request.POST.get('vacancy')
        print(vacancy)
        
        if status=="on":
            status=True
        else:
            status=True
        id=User.objects.get(username=request.user)
    
        cmpny=CompanyProfile.objects.get(username=id)
    
        job=Work(work_name=request.POST['wpn'],company=cmpny,salary_or_stipend=salary,Type=Type,about=about,location=location,emp_type=employee,experience_or_time=experience,tech_stack=tech_need,status=status,min_requirement=minimum_req,number_of_vacancy=vacancy)

        '''subject = 'Job Notification'
        message = "Hi geek,\n\nA new job has been posted for a job role of {} by the company named {}.\n\nClick to apply .\n\nWe wish a very good luck.\n\n Thank you".format(request.POST['wpn'],cmpny)
        email_data = Profile.objects.all()

        for i in email_data:
            recepient = [i.username.email]
            print(i,"===>",i.username.email)
            send_mail(subject, message, EMAIL_HOST_USER, recepient, fail_silently = False)
        '''

        #  Fetch all data
        data_w = Work.objects.all()[::-1]

        # Function send to email
        send_email(data_w)


        # Save
        # job.save()

        return redirect('JobHire')
    else:
        return render(request,'placeup/Add_job_form.html')

# def add_form_job(request):
def send_email(data_w):
        subject, from_email = 'Job Notification', EMAIL_HOST_USER
        html_content = render_to_string('email/job_mail.html',{'works':data_w}) # render with dynamic value
        text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.
        # create the email, and attach the HTML version as well.
        emails = Profile.objects.all()
        to = []
        for i in emails:
            to.append(i.username.email)
            # print(i.username.email)
        print(to)
        msg = EmailMultiAlternatives(subject, text_content, 'Job Notify' + EMAIL_HOST_USER, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print('Email ok')
        
def apply_job(request,id):
    print(request.session['username'],id)
    user = User.objects.get(username = request.session['username'])
    profile = Profile.objects.get(username = user)
    work = Work.objects.get(id=id)
    print(profile, work)
    d = work.applicants.add(profile)
    print(d)
    return redirect('myapplications')

def myapplications(request):
    user = User.objects.get(username = request.session['username'])
    profile = Profile.objects.get(username = user)
    myapplications = Work.objects.filter(applicants = profile)
    resume_selected = Work.objects.filter(resume_selected = profile)
    hired = Work.objects.filter(hired = profile)
    # applied = Work.objects.filter(applicants = user)
    print(myapplications,resume_selected)
    myapplications = myapplications[::-1]
    resume_selected = resume_selected[::-1]
    hired = hired[::-1]
    
    return render(request, 'placeup/my-applications.html',{'data':myapplications, 'data1':resume_selected,'data2':hired})


def work_view(request,id):
    work = Work.objects.filter(id=id)
    for i in work:
        print(i.applicants.all())
        applicants = i.applicants.all() 
    for i in work:
        print(i.resume_selected.all())
        resume_selected = i.resume_selected.all()
    for i in work:
        print(i.hired.all())
        hired = i.hired.all()
    # print(type(list(resume_selected)))
    # for i in resume_selected:
    #     for j in applicants:
    #         if i == j:
    #             applicants.remove(i)
    # print(applicants)
    applicants = list(applicants)
    resume_selected = list(resume_selected)
    hired = list(hired)

    for i in resume_selected:
        if i in applicants:
            applicants.remove(i)
    print(applicants)

    for i in hired:
        if i in resume_selected:
            resume_selected.remove(i)
    return render(request,'placeup/job-view.html',{'applicants':applicants,'id':id, 'resume_selected':resume_selected,'hired':hired})


def select_resume(request,id1,work):
    try:
        print(id1,work)
        work = Work.objects.get(id=work)
        user =  User.objects.get(id=id1)
        profile = Profile.objects.get(username = user)
        subject = '{}'.format(work.company.username.first_name)
        message = "Hi {} ,\n\nCongratulations, Your resume has been selected by {}.\n\nWe wish a very good luck for future.\n\n Thank you".format(profile.username,work.company.username.first_name)
        recepient = [profile.username.email]
        print(profile.username.email)
        send_mail(subject, message, EMAIL_HOST_USER, recepient, fail_silently = False)
        print('Email ok')
        d = work.resume_selected.add(profile)
        return redirect('work_view',id=work.id)
    except:
        return HttpResponse('Try one more time.')



def select_hired(request,id1,work):
    try:
        print(id1,work)
        work = Work.objects.get(id=work)
        user =  User.objects.get(id=id1)
        profile = Profile.objects.get(username = user)
        subject = '{}'.format(work.company.username.first_name)
        message = "Hi {} ,\n\nCongratulations, Your are hired by {} for a Job role of {}.\n\nWe wish a very good luck for future.\n\n Thank you".format(profile.username,work.company.username.first_name,work.work_name)
        recepient = [profile.username.email]
        print(profile.username.email)
        send_mail(subject, message, EMAIL_HOST_USER, recepient, fail_silently = False)
        print('Email ok')
        d = work.hired.add(profile)
        return redirect('work_view',id=work.id)
    except:
        return HttpResponse('Try one more time.')
