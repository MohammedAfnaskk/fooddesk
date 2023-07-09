from venv import logger
from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib import auth
from admindashboard.models import *
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cart.models import Cart 
from category.models import Wishlist
from django.core.paginator import  EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from admindashboard.models import Variation,Size
from django.contrib import messages


# Create your views here.

# Home Page
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def home(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user) 
        cart_count = cart.count() if cart else 0
    dict_list={
     'prod':Variation.objects.all(),
     'cart_count': cart_count,
    }
    return render(request,"home.html", dict_list)

# Shoping Page
def shop(request, category_slug=None):
    categories = None
    filter = request.GET.get('filter')
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories)
    else:
        products = Variation.objects.all()

    if filter == 'low_to_high':
        products = products.order_by('price_variant')
    elif filter == 'high_to_low':
        products = products.order_by('-price_variant')
    elif filter == 'atoz':
        products = products.order_by('product_variant')
    elif filter == 'ztoa':
        products = products.order_by('-product_variant')

    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    cart_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)  # Modify this query based on your cart model and user relationship
        cart_count = cart.count() if cart else 0
    dict_list = {
        'categories': categories,
        'prod': paged_products,
        'filter': filter,
        'cart_count': cart_count,

        }

    return render(request, "shop/shop.html", dict_list)

# Product Show Page
def single_product(request, var_id):
    try:
        variation = Variation.objects.get(id=var_id)
    except Variation.DoesNotExist:
            return render(request, "home.html")
    cart_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)  # Modify this query based on your cart model and user relationship
        cart_count = cart.count() if cart else 0  
    if request.method == 'POST':
            size_id = request.POST.get('size_id')
            prod_id = request.POST.get('prod_id')
            variation = Variation.objects.get(size=size_id, product_variant=prod_id)
            variation_quantity = variation.quantity_variant
            return JsonResponse({'variation_id':variation.id, 'variation_quantity':variation_quantity})
    
    variation_list = Variation.objects.filter(product_variant=variation.product_variant.id)
    context = {  
        'sizes': Size.objects.all(),
        'variations':variation,
        'variation_list': variation_list,
        'cart_count': cart_count,

    }

    return render(request, "shop/buyshop.html", context)

# Wishlist
@login_required(login_url='login') 
def wishlist(request):
  wishlist = Wishlist.objects.filter(user = request.user)
  cart_count = 0
  if request.user.is_authenticated:
    cart = Cart.objects.filter(user=request.user)  # Modify this query based on your cart model and user relationship
    cart_count = cart.count() if cart else 0 
  context ={
    'cart': cart,
    'wishlist':wishlist,
    'cart_count': cart_count,

  }
  return render(request,"shop/wishlist.html", context)

# Add Wishlist
def add_to_wishlist(request):
  if request.method== 'POST':
    if request.user.is_authenticated:
      var_id = int(request.POST.get('variation_id'))
      prod_id  = int(request.POST.get('product_id'))
      product_check  = Product.objects.get(id=prod_id)
      variant_check  = Variation.objects.get(id=var_id)
      if product_check:
          if Wishlist.objects.filter(user=request.user.id, product_id=prod_id, variation = var_id):
              return JsonResponse({"status": "Product Already in Wishlist"})
          else:
              Wishlist.objects.create(user=request.user, product_id=prod_id, variation = variant_check)
              return JsonResponse({'status': "Product added Wishlist"})
      else:
          return JsonResponse({'status': "No such product found"})
    else:
        return JsonResponse({'status': "Login to Continue"})
  return redirect('/')

# Delete Wishlist Product
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
      
# Search Product  
def search(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)  # Modify this query based on your cart model and user relationship
        cart_count = cart.count() if cart else 0  
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            # products = Variation.objects.filter(Q(product_variant__product_description__icontains=keyword)|Q(product_variant__icontains=keyword))
            products = Variation.objects.filter(product_variant__product_description__icontains=keyword)

            context = {
                'prod': products,
                'cart_count': cart_count,

            }
            return render(request, "shop/shop.html", context)
        
# 404 Page           
def page_not_found(request):
    return render(request, "error.html")
 

  
  
  


  
 