from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *

@receiver(m2m_changed , sender = Following.followed.through )
def add_follower(sender , instance , action , reverse , pk_set , **kwargs):

    followed_users = [] #list of users i followed
    logged_user = User.objects.get (username = request.user)

    for i in pk_set:
        user = User.objects.get(id = i)
        followed_obj = Following.objects.get(username = user)
        followed_users.append(followed_obj)

        if action == "pre_add":
            for i in followed_users:
                i.follower.add(logged_user)
                i.save()

        if action == "pre_remove":
            for i in followed_users:
                i.follower.remove(logged_user)
                i.save()

