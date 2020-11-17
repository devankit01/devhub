from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from .models import *
import math
import json
from PLACEUP.models import CompanyProfile
from PLACEUP.views import orgprofile
# Create your views here.
def home(request):
    return render(request, 'social/index.html')

def signup(request):
    if request.method == "POST":
        if request.POST['pass1'] == request.POST['pass2']:
            try:
                email = request.POST['email']
                # email = email[0:-10]
                user = User.objects.filter(email=email)
                if len(user) == 0:
                    raise User.DoesNotExist
                return render(request, 'social/accounts/signup.html', {'msg': 'Email already exists 🔑', 'c': 'red'})
            except User.DoesNotExist:
                username = request.POST['email'][0:-10]
                user_obj = User.objects.create_user(first_name=request.POST['fname'], last_name=request.POST['lname'],
                                                    username=username, password=request.POST['pass1'], email=request.POST['email'])
                print(user_obj)
                user_obj.save()
                new_prof = Profile(username=user_obj, fb="",
                                   lkd="", git="", hacker="", bio="", college_name="", college_year="", resume="", portfolio = "")
                new_prof.save()
                print(new_prof)
                new_resume = Resume(resume="", portfolio="", username=user_obj)
                new_resume.save()
                return redirect('signin')

        else:
            return render(request, 'social/accounts/signup.html', {'msg_pass': "Password do not matched ❌"})
    else:
        return render(request, 'social/accounts/signup.html')
    return render(request, 'social/accounts/signup.html')


def signin(request):

    if request.method == 'POST':
        try:
            # Check User in DB
            uname = request.POST['username']
            print(uname)
            uname = uname[0:-10]
            print(uname)
            pwd = request.POST['pass1']
            print(uname, pwd)
            kk = User.objects.get(username=uname)

            user_authenticate = auth.authenticate(username=uname, password=pwd)
            if user_authenticate is not None:
                auth.login(request, user_authenticate)
                request.session['username'] = uname
                print('Successfully Login')
                try:
                    Profile.objects.get(username = kk)
                    return redirect('dashboard')
                except:
                    try:
                        dd = CompanyProfile.objects.get(username = kk)
                        return redirect('orgprofile')
                    except:
                        pass
            else:
                print('Login Failed')
                return render(request, 'social/accounts/signin.html', {"msg": "Invalid Credentials ❌"})
        except:
            return render(request, 'social/accounts/signin.html')
    return render(request, 'social/accounts/signin.html')


def dashboard(request):
    # print(request.session['is_login'])
    if request.session.has_key('username'):
        obj = User.objects.get(username=request.session['username'])
        # print(obj)
        user = User.objects.get(username=obj)
        p = Profile.objects.get(username=user)
        posts = Post.objects.all()
        posts = posts[::-1]
        t = []

        # Prevent Liked Post
        liked_post = []
        # Likes Count
        for i in posts:
            is_liked = Like.objects.filter(
                post=i, username=user.id)
            if is_liked:
                liked_post.append(i.id)
            else:
                pass
        # print("like",liked_post)

        get_comment = []

        for i in posts:
            try:
                y = Comment.objects.filter(post=i)
                print(y)
                l = len(y)
                print(l)
            except:
                l = 0
            get_comment.append(l)
        print(get_comment)

        f = user.first_name
        l = user.last_name
        context = {
            'icon': str(f[0].upper()+l[0].upper()),
        }
        try:
            s = Skill.objects.filter(username=user)
            # print(s)
        except:
            pass
        like_list = []
        # Likes Of Post
        for i in posts:
            try:
                c = Like.objects.get(post=i)
                # print(c.username.count())
                x = c.username.count()
            except:
                x = 0

            like_list.append(x)
        posts = posts
        how_many = like_list
        data = zip(posts, how_many, get_comment)
        return render(request, 'social/dashboard.html', {'d': context, 'data': data, 'p': p, 's': s, 'posts': posts, 't': t, 'liked_post': liked_post, 'like_list': like_list})

    else:
        return HttpResponse('Error 404')


def profile(request):
    try:
        obj = User.objects.get(username=request.session['username'])
        print(obj)
        user = User.objects.get(username=obj)
        try:
            p = Profile.objects.get(username=user)
        except:
            pass

        f = user.first_name
        l = user.last_name

        context = {
            'icon': str(f[0].upper()+l[0].upper()),
            'name': str(f+' '+l)
        }
        try:
            s = Skill.objects.filter(username=user)
            c = Certification.objects.filter(username=user)
            print(len(s), len(c))
        except:
            pass
        a = s[0:math.ceil(len(s)/2)]
        b = s[len(a):(len(s))]

        x = c[0:math.ceil((len(c)/2))]
        y = c[len(x):(len(c))]

        print('a=', a, 'b=', b)
        print(x, y)
        # Get Follow
        try:
            follow_obj = Following.objects.get(username=obj)
            following = follow_obj.followed.count()
        except:
            following = 0

        print('Following=', following)
        return render(request, 'social/profile.html', {'d': context, 'p': p, 's': s, 'a': a, 'b': b, 'x': x, 'y': y, 'following': following})

    except:
        return HttpResponse('Error 404')


def update_profile(request):

    obj = User.objects.get(username=request.session['username'])
    print(obj)
    user = User.objects.get(username=obj)
    p = Profile.objects.get(username=user)
    p.lkd = request.POST['linkedin']
    p.hacker = request.POST['hacker']
    p.git = request.POST['git']
    p.bio = request.POST['bio']
    p.college_name = request.POST['cname']
    p.college_year = request.POST['cyear']
    p.resume = request.POST['resume']
    p.portfolio = request.POST['portfolio']
    p.save()

    print(request.POST['linkedin'],
           request.POST['hacker'], request.POST['git'], request.POST['bio'])
    return redirect('/user/profile')



def skills(request):

    obj = User.objects.get(username=request.session['username'])
    print(obj)
    user = User.objects.get(username=obj)
    try:
        p = Profile.objects.get(username=user)
        print(p)
    except:
        pass
    f = user.first_name
    l = user.last_name

    context = {
        'icon': str(f[0].upper()+l[0].upper()),
        'name': str(f+' '+l)
    }
    try:
        s = Skill.objects.filter(username=user)
        print(s)
    except:
        pass
    return render(request, 'social/skills.html', {'d': context, 'p': p, 's': s})


def add_skill(request):
    try:
        print(request.POST['name'], request.POST['skill'])
        obj = User.objects.get(username=request.session['username'])
        user = User.objects.get(username=obj)
        x = request.POST['skill']
        if x == 0:
            level = 'Beginner'
            emoji = '🥉'
        elif x == 1:
            level = 'Intermediate'
            emoji = '🥈'
        elif x == 2:
            level = 'Expert'
            emoji = '🥇'
        else:
            level = 'Beginner'
            emoji = '🥉'
        s = Skill(name=request.POST['name'],
                  level=level, username=user, emoji=emoji)
        s.save()

        return redirect('/user/skills')
    except:
        return HttpResponse('Error 404')


def edit_skill(request, id):
    try:
        # print(id)
        s = Skill.objects.get(id=id)
        print(s.level)
        if request.method == 'POST':
            print('ok')
            print(id, request.POST['name'], request.POST['skill'])
            s = Skill.objects.get(id=id)
            x = int(request.POST['skill'])
            print(x, type(x))
            if x == 0:
                level = 'Beginner'
                emoji = '🥉'
            elif x == 1:
                level = 'Intermediate'
                emoji = '🥈'
            elif x == 2:
                level = 'Expert'
                emoji = '🥇'
            else:
                level = 'Beginner'
                emoji = '🥉'

            s.level = str(level)
            s.name = request.POST['name']
            s.emoji = emoji
            s.save()
            return redirect('/user/skills')
        s = Skill.objects.get(id=id)
        return render(request, 'social/edit_skill.html', {'s': s})
    except:
        return HttpResponse('Error 404')


def delete_skill(request, key):
    print(key)
    delete_skill = Skill.objects.get(id=key)
    obj = User.objects.get(username=request.session['username'])
    print(obj)
    user = User.objects.get(username=obj)
    x = Skill.objects.filter(username=user)
    print(x, user)
    delete_skill.delete()

    return redirect('/user/skills')


def certifications(request):
    try:
        obj = User.objects.get(username=request.session['username'])
        print(obj)
        user = User.objects.get(username=obj)
        try:
            p = Profile.objects.get(username=user)
            print(p)
        except:
            pass
        f = user.first_name
        l = user.last_name

        context = {
            'icon': str(f[0].upper()+l[0].upper()),
            'name': str(f+' '+l)
        }
        try:
            c = Certification.objects.filter(username=user)
            print(c)
        except:
            pass
        return render(request, 'social/certifications.html', {'d': context, 'p': p, 'c': c})
    except:
        return HttpResponse('Error 404')


def add_certification(request):

    # print(request.POST['name'],request.POST['skill'])
    obj = User.objects.get(username=request.user)
    user = User.objects.get(username=obj)

    c = Certification(name=request.POST['name'], organisation=request.POST['organisation'],
                      month_name=request.POST['month'], year=request.POST['year'], url=request.POST['url'], username=user)
    c.save()

    return redirect('/user/certifications')


def edit_certification(request, id):
    print(id)
    c = Certification.objects.get(id=id)

    if request.method == 'POST':
        print('ok')
        c = Certification.objects.get(id=id)

        c.name = request.POST['name']
        c.organisation = request.POST['organisation']
        c.month_name = request.POST['month']
        c.year = request.POST['year']
        c.url = request.POST['url']
        c.save()
        return redirect('/user/certifications')
    # s = Skill.objects.get(id=id)
    return render(request, 'social/edit_certification.html', {'c': c})


def delete_certification(request, id):
    try:
        delete = Certification.objects.get(id=id)
        obj = User.objects.get(username=request.user)
        print(obj)
        user = User.objects.get(username=obj)

        x = Certification.objects.filter(username=user)

        for i in x:
            print(i.id)
            if str(i.id) == str(id):
                delete.delete()
            else:
                return HttpResponse('Something Went Wrong')
        return redirect('/user/certifications')
    except:
        return HttpResponse('Something Went Wrong')


def posts(request):
    obj = User.objects.get(username=request.session['username'])
    print(obj)
    user = User.objects.get(username=obj)
    try:
        p = Profile.objects.get(username=user)
        print(p)
    except:
        pass
    f = user.first_name
    l = user.last_name

    context = {
        'icon': str(f[0].upper()+l[0].upper()),
        'name': str(f+' '+l)
    }

    l = []
    m = []
    try:
        po = Post.objects.filter(username=user)
        # print(p)
        print(po)
        for i in po:
            c = Like.objects.get(post=i)
            x = c.username.count()
            l.append(x)

            comments = Comment.objects.filter(post=i)
            m.append(len(comments))
        print(l, m)

    except:
        pass
    post = po

    k = zip(po, l, m)
    print("data", po, l, m)

    return render(request, 'social/post.html', {'d': context, 'p': p, 'k': k, 'post': po})


def add_post(request):
    try:
        obj = User.objects.get(username=request.session['username'])
        user = User.objects.get(username=obj)
        try:
            if request.FILES['img']:
                i = request.FILES['img']
            else:
                i = ''
        except:
            i = ""
        p = Post(content=request.POST['content'], image=i, username=user)
        p.save()

        return redirect('/user/posts')
    except:
        return HttpResponse('Error 404')


def edit_post(request, id):
    print(id)
    p = Post.objects.get(id=id)

    if request.method == 'POST':
        print('ok')
        p = Post.objects.get(id=id)
        p.content = request.POST['content']
        try:
            if request.FILES['img']:
                i = request.FILES['img']
            else:
                i = ''
        except:
            i = ""
        p.image = i
        p.save()
        return redirect('/user/posts')
    # s = Skill.objects.get(id=id)
    return render(request, 'social/edit_post.html', {'p': p})


def delete_post(request, id):
    try:
        delete = Post.objects.get(id=id)
        obj = User.objects.get(username=request.session['username'])
        print(obj)
        user = User.objects.get(username=obj)

        x = Post.objects.filter(username=user)
        print(user, x)

        for i in x:
            if str(i.id) == str(id):
                delete.delete()
                print('delete')
        return redirect('/user/posts')
    except:
        pass


def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return redirect('/')


def user_profile(request, id):

    print(id)
    obj = User.objects.get(username=request.session['username'])
    print(obj)
    user = User.objects.get(username=obj)

    if str(id) != str(user):
        if not request.user.is_authenticated:
            return redirect('accounts/signin')

        # updated
        p_user = User.objects.get(username=id)

        x = Profile.objects.get(username=p_user)
        z = User.objects.get(profile=x)
        print(z.first_name)
        # print(type(p_user),p_user.username,z.git)

        f = z.first_name
        l = z.last_name

        context_p = {
            'user_icon': str(f[0].upper()+l[0].upper())
        }

        try:
            s = Skill.objects.filter(username=z)
            c = Certification.objects.filter(username=z)
            print(len(s), len(c))
        except:
            pass
        a = s[0:math.ceil(len(s)/2)]
        b = s[len(a):(len(s))]

        x = c[0:math.ceil((len(c)/2))]
        y = c[len(x):(len(c))]

        obj = User.objects.get(username=request.user)
        print(obj)
        user = User.objects.get(username=obj)

        f = user.first_name
        l = user.last_name

        context = {
            'icon': str(f[0].upper()+l[0].upper())
        }
        p = Profile.objects.get(username=user)
        main_user = request.user
        try:
            to_follow = User.objects.get(username=id)
            is_follow = Following.objects.filter(
                username=main_user, followed=to_follow)
            print(is_follow)
        except:
            pass

        # Get Follow
        try:
            follow_obj = Following.objects.get(username=p_user)
            following = follow_obj.followed.count()
            print('Follower==========', following)
        except:
            following = 0
        return render(request, 'social/user_profile.html', {'z': z, 'd': context, 'p': p, 'context': context_p, 'a': a, 'b': b, 'x': x, 'y': y, 'following': following, 'is_follow': is_follow})
    else:
        return redirect('/user/profile')


def like_dislike_post(request):
    print('test ok')
    id = request.GET.get('likedId', '')
    print(id)
    post = Post.objects.get(id=id)
    user = request.user
    check_liked = Like.objects.filter(post=post, username=user)

    counter = False

    if check_liked:
        # counter = False
        x = Like.dislike(post, user)

    else:
        counter = True
        Like.liked(post, user)  # classmethod access

    resp = {
        'counter': counter,
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type='application/json')

    post = Post.objects.get(id=id)
    if request.method == "POST":
        comment = Comment(
            comment_text=request.POST['comment'], post=post, username=request.session['username'])
        print(comment)
        comment.save()

        try:
            c = Like.objects.get(post=post)
            print(c.username.count())
            c = c.username.count()
        except:
            c = 0

        try:
            y = Comment.objects.filter(post=post)
            print(y)
            l = len(y)
            print(l)
        except:
            l = 0
        y = y[::-1]
        all_comments = []
        for i in y:
            print(i.comment_text)
            all_comments.append(i.comment_text)
        data = Comment.objects.filter(
            username=request.session['username'], post=post)
        lst = []
        for k in data:
            lst.append(k.id)
        print(lst)
        return render(request, 'add_comment.html', {'post': post, 'c': c, 'l': l, 'y': y, 'lst': lst})

    else:
        try:
            c = Like.objects.get(post=post)
            print(c.username.count())
            c = c.username.count()
        except:
            c = 0

        try:
            y = Comment.objects.filter(post=post)
            print(y)
            l = len(y)
            print(l)
        except:
            l = 0

        all_comments = []

        # Delete Option
        data = Comment.objects.filter(
            username=request.session['username'], post=post)
        lst = []
        for k in data:
            lst.append(k.id)
        print(lst)
        y = y[::-1]
        return render(request, 'social/add_comment.html', {'post': post, 'c': c, 'l': l, 'y': y, 'lst': lst})


def comment_post(request, id):

	post = Post.objects.get(id=id)
	if request.method == "POST":
		comment = Comment(
		    comment_text=request.POST['comment'], post=post, username=request.user)
		print(comment)
		comment.save()

		try:
			c = Like.objects.get(post=post)
			print(c.username.count())
			c = c.username.count()
		except:
			c = 0

		try:
			y = Comment.objects.filter(post=post)
			print(y)
			l = len(y)
			print(l)
		except:
			l = 0
		y = y[::-1]
		all_comments = []
		for i in y:
			print(i.comment_text)
			all_comments.append(i.comment_text)
		data = Comment.objects.filter(username=request.user, post=post)
		lst = []
		for k in data:
			lst.append(k.id)
		print(lst)
		return render(request, 'social/add_comment.html', {'post': post, 'c': c, 'l': l, 'y': y, 'lst': lst})

	else:
		try:
			c = Like.objects.get(post=post)
			print(c.username.count())
			c = c.username.count()
		except:
			c = 0

		try:
			y = Comment.objects.filter(post=post)
			print(y)
			l = len(y)
			print(l)
		except:
			l = 0

		all_comments = []

		# Delete Option
		data = Comment.objects.filter(username=request.user, post=post)
		lst = []
		for k in data:
			lst.append(k.id)
		print(lst)
		y = y[::-1]
		return render(request, 'social/add_comment.html', {'post': post, 'c': c, 'l': l, 'y': y, 'lst': lst})


def delete_comment(request, id):
    try:
        delete = Comment.objects.get(id=id)
        delete.delete()
    except:
        return HttpResponse('Something Went Wrong')
    return redirect('/user/dashboard')


def follow(request, id):
	main_user = request.user
	to_follow = User.objects.get(id=id)

	following = Following.objects.filter(username=main_user, followed=to_follow)
	print(following)

	is_following = True if following else False

	if is_following:
		print(main_user, to_follow)
		Following.unfollow(main_user, to_follow.id)
		is_following = False
	else:
		Following.follow(main_user, to_follow)
		is_following = True

	resp = {
		'following': is_following,
	}
	response = json.dumps(resp)
	return HttpResponse(response, content_type='application/json')



def myresume(request):

    obj = User.objects.get(username=request.session['username'])
    user = User.objects.get(username=obj)
    kk = Resume.objects.get(username = user)
    print(obj)
    if request.method == 'POST':
        user = User.objects.get(username=obj)
        kk = Resume.objects.get(username = user)
        url1 = request.POST['resume']
        url2 = request.POST['portfolio']
        print(url1 , url2)

        kk = Resume.objects.get(username = user)
        kk.resume = url1
        kk.portfolio = url2
        kk.save()
        print(kk)
        try:
            p = Profile.objects.get(username=user)
            print(p)
        except:
            pass
        f = user.first_name
        l = user.last_name

        context = {
            'icon': str(f[0].upper()+l[0].upper()),
            'name': str(f+' '+l)
        }
        return render(request, 'social/resume.html',{'d': context,'kk':kk})
    else:

        try:
            p = Profile.objects.get(username=user)
            print(p)
        except:
            pass
        f = user.first_name
        l = user.last_name

        context = {
            'icon': str(f[0].upper()+l[0].upper()),
            'name': str(f+' '+l)
        }
        return render(request, 'social/resume.html',{'d': context,'p':p,'kk':kk})


