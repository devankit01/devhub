from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    fb = models.CharField(max_length=100)
    lkd = models.CharField(max_length=100)
    git = models.CharField(max_length=100)
    hacker = models.CharField(max_length=100)
    bio = models.TextField(max_length=200)
    username = models.OneToOneField(User, on_delete=models.CASCADE)


class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=30)
    emoji = models.CharField(max_length=30, null=True	)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Certification(models.Model):
    name = models.CharField(max_length=100)
    organisation = models.CharField(max_length=10)
    month_name = models.CharField(max_length=30)
    year = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='images')
    date = models.DateField(auto_now_add=True)
    # profile = models.ForeignKey('Profile',on_delete = models.CASCADE , null = True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Resume(models.Model):
    resume = models.CharField(max_length=210, null=True)
    portfolio = models.CharField(max_length=210, null=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


# Like Model
class Like(models.Model):
    username = models.ManyToManyField(User, related_name='LikedUser')
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    likes_count = models.IntegerField(default=0)

    @classmethod
    def liked(cls, post, LikedUser):
        obj, create = cls.objects.get_or_create(post=post)
        obj.username.add(LikedUser)

    @classmethod
    def dislike(cls, post, dislikeduser):
        obj, create = cls.objects.get_or_create(post=post)
        obj.username.remove(dislikeduser)


class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment_text = models.TextField(max_length=250)


# Follower Model
class Following(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    followed = models.ManyToManyField(User, related_name='followed')
    follower = models.ManyToManyField(User, related_name='follower')

    @classmethod
    def follow(cls, username, another_account):
        obj, create = cls.objects.get_or_create(username=username)
        obj.followed.add(another_account)

    @classmethod
    def unfollow(cls, username, another_account):
        obj, create = cls.objects.get_or_create(username=username)
        obj.followed.remove(another_account)
