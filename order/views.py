from django.shortcuts import render
from cart.models import Order,OrderItem,Cart
from address.models import Address
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def order_details(request):
    orders =Order.objects.filter(user=request.user)
    cart = Cart.objects.all()

    context ={
        'cart': cart,
        'orders':orders
    }
    
    return render(request,"order/order.html",context)

def vieworder(request, t_no):
    user = request.user
    order = Order.objects.filter(tracking_no=t_no, user=user).first()

    if order:
        address = order.address 
        orderitems = OrderItem.objects.filter(order=order)
        cart = Cart.objects.all()

        context = {
            'cart': cart,
            'address': address,
            'order': order,
            'orderitems': orderitems,
            'user': user
        }
        return render(request, "order/orderview.html", context)
   
