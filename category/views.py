from venv import logger
from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib import auth
from admindashboard.models import Product,Category
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cart.models import Cart 
from category.models import Wishlist
from django.core.paginator import  EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q


# Create your views here.

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def home(request):
  
  cart = Cart.objects.all()

  dict_list={
    'cart': cart,
    'prod':Product.objects.all()
  }
  return render(request,"home.html", dict_list)


def shop(request,category_slug = None):
  categories =None
  if category_slug != None:
    categories = get_object_or_404(Category,slug =category_slug)
    product = Product.objects.filter(category =categories)
    paginator =Paginator(product, 2)
    page = request.GET.get('page')
    paged_products =paginator.get_page(page)
  
  else:
    cart = Cart.objects.all()
    product = Product.objects.all()
    paginator =Paginator(product, 4)
    page = request.GET.get('page')
    paged_products =paginator.get_page(page)
    dict_list={
       'cart': cart,
      'prod':  paged_products 
    } 
  return render(request,"shop/shop.html", dict_list)

def single_product(request,single_id):
    product = get_object_or_404(Product, id=single_id)
    cart = Cart.objects.all()
    context={
      'cart': cart,
      'oneproduct':product
      }
    
    return render(request,"shop/buyshop.html",context)
  
@login_required(login_url='login') 
def wishlist(request):
  wishlist = Wishlist.objects.filter(user = request.user)
  cart = Cart.objects.all()

  context ={
    'cart': cart,
    'wishlist':wishlist,
 
  }
  return render(request,"shop/wishlist.html", context)

def add_to_wishlist(request):
  if request.method        == 'POST':
    if request.user.is_authenticated:
      prod_id  = int(request.POST.get('product_id'))
      product_check  = Product.objects.get(id=prod_id)
      if product_check:
          if Wishlist.objects.filter(user=request.user.id, product_id=prod_id):
              return JsonResponse({"status": "Product Already in Wishlist"})
          else:
              Wishlist.objects.create(user=request.user, product_id=prod_id)
              return JsonResponse({'status': "Product added Wishlist"})
      else:
          return JsonResponse({'status': "No such product found"})
    else:
        return JsonResponse({'status': "Login to Continue"})
  return redirect('/')


def delete_wishlist_item(request):
    if request.user.is_authenticated:
      itemId  = int(request.POST.get('itemId'))
      if(Wishlist.objects.filter(user=request.user, id =itemId).exists()):
          wishlistitem= Wishlist.objects.get(id=itemId)
          wishlistitem.delete()
          return JsonResponse({"status": "Product removed in Wishlist"})
      else:
          return JsonResponse({'status': "Product not found in   Wishlist"})
              
    else:
        return JsonResponse({'status': "Login to Continue"})
      
# def razorpaycheck(request):
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products= Product.objects.filter(Q(product_description__icontains=keyword) |Q(product_name__icontains=keyword))
            context = {
                'prod': products,
            }
            return render(request, "shop/shop.html", context)

  
  
  


  
 