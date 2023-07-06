
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.views.decorators.cache import cache_control

from django.contrib.auth.decorators import login_required
from admindashboard.models import Product, Variation
from django.contrib.auth.models import User
from address.models import Address
import random
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect
from coupon.models  import *
 
# Create your views here.
@login_required(login_url='login')
def cart(request):
    user = request.user
    cart = Cart.objects.filter(user=request.user)  # Modify this query based on your cart model and user relationship
    cart_count = cart.count() if cart else 0
    cart = Cart.objects.filter(user=user)
    subtotal = 0
    for item in cart:
        if item.variation.offer is None:
            subtotal += item.product_qty * item.variation.price_variant
        else:
            subtotal += item.product_qty * item.variation.price_variant
            if item.variation.offer is not None:
                subtotal -= item.variation.offer.discount_amount * item.product_qty

    tax = subtotal * 0.05  # Assuming tax is 5% of the subtotal
    totalamount = subtotal + tax

        
    context = {
        'cart': cart,
        'subtotal': subtotal,
        'tax': tax,
        'totalamount': totalamount,
        'cart_count': cart_count,

    }
    return render(request, "shop/cart.html", context)


def addtocart(request):
    if request.method  == 'POST':
        if request.user.is_authenticated:
            var_id          = int(request.POST.get('variation_id'))
            prod_id          = int(request.POST.get('product_id'))
            product_check    = Product.objects.get(id=prod_id)
            variation    = Variation.objects.get(id=var_id)
            if product_check:
                if Cart.objects.filter(user=request.user.id, product_id=prod_id,variation =var_id):
                    return JsonResponse({"status": "Product Already in Cart"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    if variation.quantity_variant >= prod_qty:
                        Cart.objects.create(user=request.user, product_id=prod_id,variation = variation, product_qty=prod_qty)
                        return JsonResponse({'status': "Product added successfully"})
                    else:
                        return JsonResponse({'status': "Only " + str(variation.quantity_variant) + " quantity available"})
            else:
                return JsonResponse({'status': "No such product found"})
        else:
            return JsonResponse({'status': "Login to Continue"})
    return redirect('/')
 
def update_cart(request):
    if request.method == 'POST':
        variation_id = request.POST.get('product_id')
        if (Cart.objects.filter(user=request.user, variation=variation_id)):
            prod_qty = request.POST.get('product_qty')
            cart = Cart.objects.get(variation=variation_id, user=request.user)
            cartes = cart.variation.quantity_variant
            if int(cartes) >= int(prod_qty):
                cart.product_qty = prod_qty
                cart.save()
                carts = Cart.objects.filter(user = request.user).order_by('id')
                total_price = 0
                for item in carts:
                    if item.variation.offer == None:
                       total_price = total_price + item.variation.price_variant * item.product_qty
                    else:
                        total_price = total_price + item.variation.price_variant * item.product_qty
                        total_price = total_price - item.variation.offer.discount_amount * item.product_qty
                    
                return JsonResponse({'status': 'Updated successfully','sub_total':total_price,})
            else:
                return JsonResponse({'status': 'Not quantity'})
    return JsonResponse('something went wrong, reload page',safe=False)


def removeFromCart(request, cart_id):
    if request.method == 'POST':
        delete_cart   = get_object_or_404(Cart, id=cart_id)
        delete_cart.delete()
        messages.success(request, 'Product deleted successfully')
        return redirect('cart')
    else:
        return redirect('cart')
    
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='login')
def checkout(request):
    address = Address.objects.filter(customer=request.user) 
    cart = Cart.objects.filter(user=request.user)
    cart_count = cart.count() if cart else 0  
    subtotal = 0
   
    for item in cart:
        if item.variation.offer is None:
            subtotal += item.product_qty * item.variation.price_variant
        else:
            subtotal += item.product_qty * item.variation.price_variant
            if item.variation.offer is not None:
                subtotal -= item.variation.offer.discount_amount * item.product_qty

    tax = subtotal * 0.05  # Assuming tax is 5% of the subtotal
    totalamount = subtotal + tax

    usercoupon = Usercoupon.objects.filter(user=request.user).last()
    coupons = Coupon.objects.all()


    context = {
        'cart': cart,
        'subtotal1': subtotal,
        'tax1': tax,
        'totalamount1': totalamount,
        'address': address,
        'usercoupon':usercoupon,
        'coupons': coupons,
        'cart_count': cart_count

    }
 
    return render(request, "shop/checkout.html", context)



 

 
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='login')
def place_order(request):
    if request.method == 'POST':
        new_order = Order()
        user = request.user
        selected_address_index = int(request.POST.get('address-toggle'))
        print(selected_address_index,'daxo')
        
        addresses = Address.objects.filter(customer=user)
        address = addresses[selected_address_index]
        
        if address is None:
            messages.error(request, 'Please add an address before placing an order.')
            return redirect('checkout')
        payment_mode = request.POST.get('payment_mode')
        
        cart_items = Cart.objects.filter(user=user)
        subtotal = 0
        for item in cart_items:
            if item.variation.offer is None:
               subtotal += item.product_qty * item.variation.price_variant
            else:
                subtotal += item.product_qty * item.variation.price_variant
                if item.variation.offer is not None:
                    subtotal -= item.variation.offer.discount_amount * item.product_qty

        tax = subtotal * 0.05

        total = 0
        if Usercoupon.objects.filter(user = request.user).exists():
            usercoupon = Usercoupon.objects.get(user = request.user)
            total= usercoupon.total_price
            usercoupon.delete()
        else:
            total = subtotal + tax

        # new_order = Order(total_price=total_price)  # Assign total_price to new_order
        # new_order.save()


        trackno = 'fooddesk' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = 'fooddesk' + str(random.randint(1111111, 9999999))

        new_order = Order.objects.create(
            user=user,
            address=address,
            total_price = total,
            payment_mode=payment_mode,
            tracking_no=trackno
        )

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            product = item.product  # Retrieve the product instance
            variation = item.variation
            OrderItem.objects.create(
                order=new_order,
                product=product,  # Assign the product instance
                variation = variation,
                price=variation.price_variant,  # Set the price
                quantity=item.product_qty
            )

            # Decrease product quantity from available stock
            order_product = Variation.objects.filter(id=item.variation.id).first()
            order_product.quantity_variant -= item.product_qty
            order_product.save()
        payment_mode = request.POST.get('payment_mode')
        if (payment_mode == "Razorpay"):
            Cart.objects.filter(user=request.user).delete()
            return JsonResponse({'status' : "Yout order has been placed successfully"})
        # Clear user's cart
        cart_items.delete()

        messages.success(request, 'Your order has been placed successfully')
        
       
    return HttpResponseRedirect('checkout')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='login')
def razarypaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    grand_total = 0
    for item in cart:
        if item.variation.offer is None:
           total_price += item.variation.price_variant * item.product_qty
        else:
            total_price += item.variation.price_variant * item.product_qty
            if item.variation.offer is not None:
                total_price -= item.variation.offer.discount_amount * item.product_qty      
    tax = total_price * 0.05 
    grand_total += total_price+tax
    if Usercoupon.objects.filter(user = request.user).exists():
        usercoupon = Usercoupon.objects.get(user = request.user)
        grand_total= usercoupon.total_price
        usercoupon.delete()
    else:
        grand_total = total_price + tax
    return JsonResponse({'total_price': grand_total})

 
 
        
        
        
        
        

 
 

     

    