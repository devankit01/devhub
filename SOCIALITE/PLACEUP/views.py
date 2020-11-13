from .models import *
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
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
                return redirect('orgsignin')

        else:
            return render(request, 'placeup/accounts/signup.html', {'msg_pass': "Password do not matched ❌"})
    else:
        return render(request, 'placeup/accounts/signup.html')
    return render(request, 'placeup/accounts/signup.html')


# def orgsignin(request):
#     return render(request, 'placeup/accounts/signin.html')

def orgsignin(request):

    if request.method == 'POST':
        try:
            # Check User in DB
            uname = request.POST['username']
            print(uname)
            uname = uname[0:-10]
            print(uname)
            pwd = request.POST['pass1']
            print(uname, pwd)
            ud = User.objects.get(username=uname)
            dd = CompanyProfile.objects.get(username = ud)
            user_authenticate = auth.authenticate(username=uname, password=pwd)
            if user_authenticate is not None:
                auth.login(request, user_authenticate)
                request.session['username'] = uname
                print('Successfully Login')
                return redirect('orgprofile')

            else:
                print('Login Failed')
                return render(request, 'placeup/accounts/signin.html', {"msg": "Invalid Credentials ❌"})
        except:
            return render(request, 'placeup/accounts/signin.html')
    return render(request, 'placeup/accounts/signin.html')


def orglogout(request):
    try:
        del request.session['username']
    except:
        pass
    return redirect('orgsignin')


def orgprofile(request):
    return render(request, 'placeup/profile.html')


def jobs(request):
    return render(request, 'placeup/jobs-intern-plateform.html')