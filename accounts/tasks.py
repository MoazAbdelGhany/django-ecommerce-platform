from django.core.mail import EmailMessage 
from celery import shared_task 
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes 
from django.utils.http import  urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from .models import Account

@shared_task 
def send_verification_email(user_id):
    user = Account.objects.get(id = user_id)
    domain_name = settings.SITE_DOMAIN
    mail_subject = 'please verify you email'
    verification_mail =render_to_string('accounts/account_verification_email.html',{
        'user':user,
        'domain':domain_name,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user)
    }) 

    to_email = user.email 
    email = EmailMessage(mail_subject , verification_mail , to=[to_email])
    email.send()