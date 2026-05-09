from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save , sender= Account)
def send_welcome_mail(sender , instance , created , **kwargs):
    if created:
        subject = 'Welcmoe to My Shop'
        message = f'Hi {instance.username}. \nThank you for creating an account with us'
        from_mail = settings.DEFAULT_FROM_EMAIL
        user_email = [instance.email]
        
        send_mail(subject ,message , from_mail , user_email)