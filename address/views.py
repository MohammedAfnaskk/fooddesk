 
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


# Create your views here.
@login_required(login_url='login')
def userprofile(request):
    user = User.objects.get(username=request.user)
    addresses = Address.objects.filter(customer=request.user)
    cart = Cart.objects.filter(user=request.user)
    userdetails = {
        'cart': cart,
        'user': user,
        'addresses': addresses
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
  
def delete_address(request, address_id):
    address = Address.objects.get(id=address_id)
    address.delete()
    messages.success(request, 'Address deleted successfully.')
    return redirect('userprofile')  


def change_password(request):
  if request.method == 'POST':
    current_password = request.POST.get('password')
    change_psw = request.POST.get('newpassword')
    comfirm_psw = request.POST.get('renewpassword')
    
    user = authenticate(username=request.user, password=current_password)
    if change_psw !=comfirm_psw:
      messages.error(request,"password dosen't Match")
      return redirect('change_password')
    
    if user is not None:
      user.set_password(change_psw)
      user.save()
      messages.error(request,"password change succesfully")

      
      
  return redirect('userprofile')



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
  