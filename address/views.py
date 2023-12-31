 
from django.contrib import messages
from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from address.models import Address
from cart.models import Cart 
from django.contrib.auth import authenticate
from order.models import Wallet
from django.core.exceptions import ValidationError


# Create your views here.

# User Profile
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='login')
def userprofile(request):
  user = User.objects.get(username=request.user)
  addresses = Address.objects.filter(customer=request.user)
  cart = Cart.objects.filter(user=request.user)  # Modify this query based on your cart model and user relationship
  cart_count = cart.count() if cart else 0  
  wallet = Wallet.objects.filter(user=request.user).last()
 

  userdetails = {
        'cart': cart,
        'user': user,
        'addresses': addresses,
        'wallet': wallet,
        'cart_count': cart_count,

    }

  if request.method == 'POST':
        image = request.FILES.get('image')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        mobilenumber = request.POST.get('mobile_number')
        email = request.POST.get('email')

        if firstname:
            user.first_name = firstname
        if lastname:
            user.last_name = lastname
        if mobilenumber:
            user.mobile_number = mobilenumber
        if email:
            user.email = email
        if image:
            user.image = image
        user.save()
        return redirect('userprofile')

  return render(request, "profile/profile.html", userdetails)

# Add address 
def add_address(request):
  
  user =  request.user
  new_name =request.POST.get('fullname')
  new_mobile =request.POST.get('mobile')
  new_house = request.POST.get('house1')
  new_city = request.POST.get('city1')
  new_state = request.POST.get('state1')
  new_zip = request.POST.get('zip1')
  new_country = request.POST.get('country1')
  
  address = Address(customer = user, fullname = new_name,mobile = new_mobile, house = new_house,city = new_city, state = new_state,zip = new_zip,country = new_country)
  address.save()
  return redirect('userprofile')

#Update address
def update_address(request,adrs_id):
  address = Address.objects.get(id = adrs_id)

  if request.method == 'POST':
    new_name =request.POST.get('fullname')
    new_mobile =request.POST.get('mobile')
    new_house = request.POST.get('house1')
    new_city = request.POST.get('city1')
    new_state = request.POST.get('state1')
    new_zip = request.POST.get('zip1')
    new_country = request.POST.get('country1')
    if new_name:
      address.fullname = new_name
    if new_mobile:
      address.mobile = new_mobile
    if new_house:
      address.house=  new_house
    if new_city:
      address.city = new_city
    if new_state:
      address.state = new_state
    if new_zip:
      address.zip = new_zip
    if new_country:
      address.country = new_country
    address.save()
    return redirect('userprofile')
  
# Delete address 
def delete_address(request, address_id):
    address = Address.objects.get(id=address_id)
    address.delete()
    messages.success(request, 'Address deleted successfully.')
    return redirect('userprofile')  

# Change Password
def change_password(request):
  if request.method == 'POST':
    current_password = request.POST.get('password')
    change_psw = request.POST.get('newpassword')
    comfirm_psw = request.POST.get('renewpassword')
    password_validate = ValidatePassword(change_psw)
        
    user = authenticate(username=request.user, password=current_password)
    if change_psw !=comfirm_psw:
      messages.error(request,"password dosen't Match")
      return redirect('change_password')
    
    if  change_psw == comfirm_psw :
        if password_validate is False:  
            messages.info(request,'Enter Strong Password')
            return redirect('change_password')

    if user is not None:
      user.set_password(change_psw)
      user.save()
      messages.error(request,"password change succesfully")
 
  return redirect('userprofile')

# Validate Password
def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False

# Add Address Checkout Page
def add_address_checkout(request):
  user =  request.user
  new_name =request.POST.get('fullname')
  new_mobile =request.POST.get('mobile')
  new_house = request.POST.get('house1')
  new_city = request.POST.get('city1')
  new_state = request.POST.get('state1')
  new_zip = request.POST.get('zip1')
  new_country = request.POST.get('country1')
  
  address = Address(customer = user, fullname = new_name,mobile = new_mobile,house = new_house,city = new_city, state = new_state,zip = new_zip,country = new_country)
  address.save()
  return redirect('checkout')

# Update Address Checkout
def update_address_checkout(request,adrs_id):
  address = Address.objects.get(id = adrs_id)

  if request.method == 'POST':
    new_name =request.POST.get('fullname')
    new_mobile =request.POST.get('mobile')
    new_house = request.POST.get('house1')
    new_city = request.POST.get('city1')
    new_state = request.POST.get('state1')
    new_zip = request.POST.get('zip1')
    new_country = request.POST.get('country1')
    if new_name:
      address.fullname = new_name
    if new_mobile:
      address.mobile = new_mobile
    if new_house:
      address.house=  new_house
    if new_city:
      address.city = new_city
    if new_state:
      address.state = new_state
    if new_zip:
      address.zip = new_zip
    if new_country:
      address.country = new_country
    address.save()
    return redirect('checkout')
  
# Delete Address Checkout Page
def delete_address_checkout(request, address_id):
    address = Address.objects.get(id=address_id)
    address.delete()
    messages.success(request, 'Address deleted successfully.')
    return redirect('checkout')  