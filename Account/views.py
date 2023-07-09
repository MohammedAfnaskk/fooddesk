
import re
from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

from .models import *
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re

# Create your views here.

# User login.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password =request.POST['password']
        user=auth.authenticate(username=username,password = password)
    
  # validation
        if username.strip() == '' or password.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect("login")
        if user is not None:
            auth.login(request, user)
            return redirect('home')

        else:
            messages.error(request,"Your username or password is Incorrect")
            return redirect("login")
    return render(request,"Account/login.html") 


# User Signup
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.user.is_authenticated:
        return redirect('home') 
    """ OTP VERIFICATION """

    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            usr=User.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                auth.login(request,usr)
                UserOTP.objects.filter(user=usr).delete()
                return redirect('home')
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request, 'Account/signup.html',{'otp':True,'usr':usr})
            
        # User rigistration validation
        else:
            firstname = request.POST['firstname']   
            name = request.POST['name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            # null values checking
            check = [name,email,password1,password2]
            for values in check:
                if values == '':
                    context ={
                        'pre_firstname' :firstname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                    messages.info(request,'some fields are empty')
                    return render(request, 'Account/signup.html',context)
                else:
                    pass
            
            result = validate_name(name)
            if result is not False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,result)
                return render(request, 'Account/signup.html',context)
            else:
                pass

            result = validateEmail(email)
            if result is False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,'Enter valid email')
                return render(request, 'Account/signup.html',context)
            else:
                pass
            
            Pass = ValidatePassword(password1)
            if Pass is False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,'Enter Strong Password')
                return render(request, 'Account/signup.html',context)
            else:
                pass
            if password1 == password2:
          
                try:
                    User.objects.get(email=email)
                except:
                    usr = User.objects.create_user(first_name=firstname,username=name,email=email,password=password1)
                    usr.is_active=False
                    usr.save()
                    user_otp=random.randint(100000,999999)
                    UserOTP.objects.create(user=usr,otp=user_otp)
                    mess=f'Hello\t{usr.username},\nYour OTP to verify your account for FOODDESK is {user_otp}\nThanks!'
                    send_mail(
                            "welcome to FOODDESK Verify your Email",
                            mess,
                            settings.EMAIL_HOST_USER,
                            [usr.email],
                            fail_silently=False
                        )
                    return render(request, 'Account/signup.html',{'otp':True,'usr':usr})
                else:
                    context ={
                        'pre_firstname' :firstname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                    messages.error(request,'Email already exist')
                    return render(request,'Account/signup.html',context)
            else:
                context ={
                        'pre_firstname' :firstname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.error(request,'password mismatch')
                return render(request,'Account/signup.html',context)
    else:
       return render(request, 'Account/signup.html')
   
# User Logout
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

    
# Admin Login
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password,is_superuser=True)
        
        if user is not None:
            print("hello")
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "You are not a superuser")
            return redirect('signin')
    return render(request, "Admin/signin.html")

# Admin Signup
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def signupadmin(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method=='POST':
        get_otp=request.POST.get('otp1')
        
        if get_otp: 
            get_email=request.POST.get('email')
 
            usr=User.objects.filter(email=get_email).last()
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                auth.login(request,usr)
                messages.success(request,'Accouunt is created')
                UserOTP.objects.filter(user=usr).delete()
                return redirect('dashboard')
            else:
                messages.error(request,'you enterd wrong otp try again')
                return render(request,'Admin/signupadmin.html',{'otp1':True,'usr':usr}) 
       
        else:
            first_name = request.POST.get('first_name')
            username = request.POST.get('username')
            email = request.POST.get('email_id')
            password = request.POST.get('password')
            confirmpassword = request.POST.get('confirmpassword')
            password_validate = ValidatePassword(password)
        
            if username.strip() == '' or password.strip() == '' or confirmpassword.strip() == '':
                messages.error(request, "Fields can't be blank")
                return redirect('signupadmin')
            
            if password == confirmpassword:
                if password_validate is False:  
                    messages.info(request,'Enter Strong Password')
                    return redirect('signupadmin')
                
            if User.objects.filter(email=email).exists():
               messages.error(request, "Email  already exists.")
               return redirect('signupadmin')
           
            if password != confirmpassword:
                messages.error(request, "Passwords don't match")
                return redirect('signupadmin')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Admin name already exists')
                return redirect('signupadmin')
           
            else:
                user = User.objects.create_user(username=username, password=password, first_name=first_name , email=email, is_superuser=True)
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
                return render(request,'Admin/signupadmin.html', {'otp1':True,'usr':user})
    return render(request, "Admin/signupadmin.html")


# Forgot Password
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def forgot_password(request):
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            usr=User.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                user = User.objects.get(email = get_email)
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                Pass = ValidatePassword(password1)
                if password1 == password2:
                    if Pass is False:
                        context ={
                                'pre_otp':get_otp,
                            }
                        messages.info(request,'Enter Strong Password')
                        return render(request,'Account/forgotpassword.html',context)
                    user.set_password(password1)
                    user.save()
                    UserOTP.objects.filter(user=usr).delete()
                    return redirect('login')
                else:
                    messages.error(request,"Password dosn't match")
                    return render(request,'Account/forgotpassword.html',{'otp':True,'usr':usr})
            else:
                messages.warning(request,'You Entered a wrong OTP')
                return render(request,'Account/forgotpassword.html',{'otp':True,'usr':usr})
            
        # User rigistration validation
        else:
            email = request.POST['email']
            # null values checking
            check = [email]
            for values in check:
                if values == '':
                    context ={
                       'pre_email':email,
                    }
                    return render(request,'Account/forgotpassword.html',context)
                else:
                    pass

            result = validateEmail(email)
            if result is False:
                context ={
                        'pre_email':email,
                    }
                messages.info(request,'Enter valid email')
                return render(request,'Account/forgotpassword.html',context)
            else:
                pass
            
            if User.objects.filter(email = email).exists():
                usr = User.objects.get(email=email) 
                user_otp=random.randint(100000,999999)
                UserOTP.objects.create(user=usr,otp=user_otp)
                mess=f'Hello\t{usr.username},\nYour OTP to verify your account for FOODDESK is {user_otp}\nThanks!'
                send_mail(
                        "welcome to FOODDESK Verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [usr.email],
                        fail_silently=False
                    )
                return render(request,'Account/forgotpassword.html',{'otp':True,'usr':usr})
            else:
                messages.info(request,'You have not an account')
                return render (request, 'Account/forgotpassword.html')
    return render(request,'Account/forgotpassword.html')

# Validate Password
def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False
    
# Validate Email
def validateEmail(email):
    from django.core.validators import validate_email
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

# Validate Name 
def validate_name(value):
    if not re.match(r'^[a-zA-Z\s]*$', value):
        return 'Name should only contain alphabets and spaces'
    
    elif value.strip() == '':
        return 'Name field cannot be empty or contain only spaces' 
    elif User.objects.filter(username=value).exists():
        return 'Usename already exist'
    else:
        return False
    
    
     
          
            
            
        
        

        
