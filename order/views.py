from django.shortcuts import render,redirect,get_object_or_404

from cart.models import Order,OrderItem,Cart
from address.models import Address
from django.contrib.auth.decorators import login_required
from category.models import Variation
from django.contrib import messages
from .models import*
from django.http import HttpResponse

# Create your views here.
# User Order Details Page 
@login_required(login_url='login')
def order_details(request):
    orders =Order.objects.filter(user=request.user).order_by('-id')
    cart = Cart.objects.filter(user=request.user)  # Modify this query based on your cart model and user relationship
    cart_count = cart.count() if cart else 0  

    context ={
        'orders':orders,
        'cart_count': cart_count,

    }
    
    return render(request,"order/order.html",context)

# User Order View Page
def vieworder(request, t_no):
    user = request.user
    order = Order.objects.filter(tracking_no=t_no, user=user).first()

    if order:
        address = order.address 
        orderitems = OrderItem.objects.filter(order=order)
        cart = Cart.objects.filter(user=request.user)  # Modify this query based on your cart model and user relationship
        cart_count = cart.count() if cart else 0  
        context = {
            'address': address,
            'order': order,
            'orderitems': orderitems,
            'user': user,
            'cart_count': cart_count,

        }
        return render(request, "order/orderview.html", context)
    else:
        return redirect("order_details")
   
# User Order Cancel  
def ordercancel(request, order_id, item_id):
    try:
       order_item = OrderItem.objects.filter(id = item_id, order__id=order_id)
    except OrderItem.DoesNotExist:
        messages.error(request, 'orderitem_not_found')
        return redirect('order_details')
    for order_item in order_item:
        qty = order_item.quantity
        pid = order_item.variation.id
         
        if order_item.order.payment_mode == 'Razorpay':
            total_price = order_item.price
            
            try:
                wallet = Wallet.objects.get(user=request.user)
                wallet.wallet += total_price
                wallet.save()
            except Wallet.DoesNotExist:
                wallet = Wallet.objects.create(user=request.user, wallet=total_price)

        if order_item.status == 'cancelled':
            messages.error(request, 'Order is already cancelled')
        else:
            order_item.status = 'cancelled'
            order_item.quantity = 0
            order_item.save()
            messages.success(request, 'Order has been cancelled successfully')
            
    variation = Variation.objects.filter(id=pid).first()
    variation.quantity_variant = variation.quantity_variant + qty
    variation.save()
    return redirect('orderview', t_no=order_item.order.tracking_no)

# User Order Return
def order_return(request, order_id):
    try:
        order_return = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, 'order_not_found')
        return redirect('order_details')
    if request.method == 'POST':
        comment = request.POST.getlist('comment')
        image = request.FILES.getlist('image')
        order_return = Orderreturn.objects.create(
            user=request.user,
            order=order_return,
            comment=comment,
            image=image
        )
    return redirect('orderview', t_no=order_return.order.tracking_no)

    
    
 
