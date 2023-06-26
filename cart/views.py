
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.contrib.auth.decorators import login_required
from admindashboard.models import Product
from django.contrib.auth.models import User
from address.models import Address
import random
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect
from coupon.models  import *
 
# Create your views here.
@login_required(login_url='login')
def cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    subtotal = 0
    for item in cart:
        subtotal += item.product_qty * item.product.product_price

    tax = subtotal * 0.05  # Assuming tax is 5% of the subtotal
    totalamount = subtotal + tax
    context = {
        'cart': cart,
         'subtotal': subtotal,
        'tax': tax,
        'totalamount': totalamount
    }
    return render(request, "shop/cart.html", context)


def addtocart(request):
    if request.method  == 'POST':
        if request.user.is_authenticated:
            prod_id          = int(request.POST.get('product_id'))
            product_check    = Product.objects.get(id=prod_id)
            if product_check:
                if Cart.objects.filter(user=request.user.id, product_id=prod_id):
                    return JsonResponse({"status": "Product Already in Cart"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({'status': "Product added successfully"})
                    else:
                        return JsonResponse({'status': "Only " + str(product_check.quantity) + " quantity available"})
            else:
                return JsonResponse({'status': "No such product found"})
        else:
            return JsonResponse({'status': "Login to Continue"})
    return redirect('/')
 
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if (Cart.objects.filter(user=request.user, product=product_id)):
            prod_qty = request.POST.get('product_qty')
            cart = Cart.objects.get(product=product_id, user=request.user)
            cartes = cart.product.quantity
            if int(cartes) >= int(prod_qty):
                cart.product_qty = prod_qty
                cart.save()
                carts = Cart.objects.filter(user = request.user).order_by('id')
                total_price = 0
                for item in carts:
                    total_price = total_price + item.product.product_price * item.product_qty
                    
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
    

 

def checkout(request):
    address = Address.objects.filter(customer=request.user) 
    cart = Cart.objects.filter(user=request.user)

    subtotal = 0
    for item in cart:
        subtotal += item.product_qty * item.product.product_price
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
        'coupons': coupons
    }
 
    return render(request, "shop/checkout.html", context)



 

 
 

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
            subtotal += item.product_qty * item.product.product_price

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
            OrderItem.objects.create(
                order=new_order,
                product=product,  # Assign the product instance
                price=product.product_price,  # Set the price
                quantity=item.product_qty
            )

            # Decrease product quantity from available stock
            order_product = Product.objects.filter(id=item.product.id).first()
            order_product.quantity -= item.product_qty
            order_product.save()
        payment_mode = request.POST.get('payment_mode')
        if (payment_mode == "Razorpay"):
            Cart.objects.filter(user=request.user).delete()
            return JsonResponse({'status' : "Yout order has been placed successfully"})
        # Clear user's cart
        cart_items.delete()

        messages.success(request, 'Your order has been placed successfully')
        
       
    return HttpResponseRedirect('checkout')

def razarypaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    grand_total = 0
    for item in cart:
        total_price += item.product.product_price * item.product_qty
    tax = total_price * 0.05 
    grand_total += total_price+tax
    return JsonResponse({'total_price': grand_total})

 
 
        
        
        
        
        

 
 

     

    