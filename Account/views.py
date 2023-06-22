
import re
from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

#validation

from .models import *
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re
  # Create your views here.

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password =request.POST['password']
        user=auth.authenticate(username=username,password = password)
        
  # validation
        if user is not None:
            auth.login(request, user)
            return redirect('home')

        else:
            messages.error(request,"Your username or password is Incorrect")
            return redirect("login")
    return render(request,"login.html") 


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def signup(request):
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        
        if get_otp:
            get_email=request.POST.get('email')
            usr=User.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                auth.login(request,usr)
                messages.success(request,'Accouunt is created for {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return redirect('home')
            else:
                messages.error(request,'you enterd wrong otp try again')
                return render(request,'signup.html',{'otp':True,'usr':usr}) 
    
        else:    
            name =request.POST['first_name']
            username = request.POST['username']
            email = request.POST['emailid']
            mobile_number= request.POST['mobile_number']
            password = request.POST['password']
            comfirmpassword = request.POST['comfirmpassword']
            
            if username.strip() == '' or password.strip() == '' or comfirmpassword.strip() == '' or email.strip() == '':
                messages.error(request,"Fields can't be blank")
                return redirect('signup')
            if password !=comfirmpassword:
                messages.error(request,"password dosen't Match")
                return redirect('signup')
            if User.objects.filter(username=username).exists():
                messages.error(request, 'User name already exists')
                return redirect('signup')
            
            if not re.match(r'^\d{10}$', mobile_number):
                messages.error(request, 'Invalid mobile number. Please enter a 10-digit mobile number.')
                return redirect('signup')
            
            else:
                user = User.objects.create_user(username=username,password=password,first_name=name,email=email,mobile_number=mobile_number)
                user.is_active=False
                user.save()
                
                user_otp=random.randint(100000,999999)
                UserOTP.objects.create(user=user ,otp=user_otp)
                
                mess=f'Hello\t{user.first_name},\nOTP to verify your account for Fooddesk is {user_otp}\nHappy Shopping..!!'
                send_mail(
                        "Welcome to Fooddesk, Verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False
                    )
                messages.error(request,"Please enter OTP and Finish the registration..!!")
                return render(request,'signup.html',{'otp':True,'usr':user})
    return render(request,"signup.html")

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


# Create your views here.
    
 
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
 
def signin(request):
    # if request.user.is_superuser:
    #     if request.user.is_authenticated:
    #         return redirect('dashboard')
    #     else:
    #         return redirect(signin)
    # else:
    #     return redirect('home')
       
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            
            if request.user.is_superuser:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Your username or password is incorrect")
                return redirect('signin')
    return render(request, "Admin/signin.html")

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def signupadmin(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email_id')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        
        if username.strip() == '' or password.strip() == '' or confirmpassword.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('signupadmin')
        
        if password != confirmpassword:
            messages.error(request, "Passwords don't match")
            return redirect('signupadmin')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signupadmin')
        
        user = User.objects.create_user(username=username, password=password, first_name=first_name , email=email, is_superuser=True)
        user.save()
        messages.success(request, "User created successfully")
        return redirect('signin')
    return render(request, "Admin/signupadmin.html")

                              

     
          
            
            
        
        

        
