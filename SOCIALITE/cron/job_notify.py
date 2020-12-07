from Django_Socialite.models import *
from PLACEUP.models import *

from SOCIALITE.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

# For html content sending
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_notification():
    data_w = Work.objects.all()
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