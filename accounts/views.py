from django.shortcuts import render , redirect
from .forms import RegisterForm 
import uuid
from .models import Account
from django.contrib.auth import authenticate , login as auth_login
from django.db import transaction
from django.contrib import messages
from .tasks import send_verification_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

def register(request):
    form = RegisterForm()
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                country = form.cleaned_data['country']
                password = form.cleaned_data['password']
                username =  f"{email.split('@')[0]}_{uuid.uuid4().hex[:6]}"
                phone_number = form.cleaned_data['phone_number']

                user = Account.objects.create_user(first_name = first_name , last_name = last_name , email = email , country = country , username = username , password = password , phone_number = phone_number ) # type: ignore
                #eamil verification
                send_verification_email.delay(user.id) # type: ignore
                
                return redirect('login' + f"?command=verification&mail={email}")

    else: 
        form = RegisterForm()

    context = {'form':form}
    return render(request , 'accounts/register.html', context)    


def activate(request , uidb64 , token):
    try :
        uid =  urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk = uid)
    except(TypeError , ValueError , OverflowError , Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user , token): 
        user.is_active = True
        user.save()
        messages.success(request , 'Verification Success')
        return redirect('accounts:login')
    else:
        messages.error(request, 'verification Failed, please try again!')
        return redirect('accounts:register') 


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate( request , username = email , password = password)
        if user is not None and user.is_active : 
            auth_login(request , user )
            messages.success(request , 'Login Success')
            return redirect('store:list_products')
        elif user is not None and user.is_active == False:
            messages.error(request, 'Activate your account, check your email box')
        else: 
            messages.error(request , 'Login Failed , Check your info')
            return redirect('accounts:login')

    return render(request , 'accounts/login.html')
      
