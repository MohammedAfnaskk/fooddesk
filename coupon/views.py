
from django.shortcuts import render, redirect
from .models import Coupon, Usercoupon
from django.contrib import messages
from django.http.response import JsonResponse
from django.core.exceptions import ValidationError
from cart.models import Cart
# Create your views here.

# Apply Coupon
def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        cart_items = Cart.objects.filter(user=request.user)
        grand_total = 0 
        subtotal = 0
        for item in cart_items:
            if item.variation.offer is None:
                subtotal += item.product_qty * item.variation.price_variant
                tax = subtotal * 0.05  # Assuming tax is 5% of the subtotal
                grand_total = subtotal + tax
            else:
                subtotal += item.product_qty * item.variation.price_variant
                if item.variation.offer is not None:
                    subtotal -= item.variation.offer.discount_amount * item.product_qty
                    tax = subtotal * 0.05  # Assuming tax is 5% of the subtotal
                    grand_total = subtotal + tax
        if coupon_code.strip() == '':
            return JsonResponse({'status': 'Field is blank'})
        
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code, active=True)
        except Coupon.DoesNotExist:
            return JsonResponse({'status': 'Coupon does not exist'})

        if Usercoupon.objects.filter(user=request.user, coupon__coupon_code=coupon_code).exists():
        # if Usercoupon.objects.filter(user=request.user).exists():
            return JsonResponse({'status': 'Coupon already used!'})

        if grand_total > coupon.min_value:
            coupon_discount = coupon.discount
            grand_total = grand_total - (grand_total * (coupon.discount / 100))
            usercoupon = Usercoupon.objects.create(user=request.user, coupon=coupon, used=True, total_price = grand_total)
            usercoupon.save()
            return JsonResponse({'status': 'Coupon added successfully', 'coupon_discount': coupon_discount, 'grand_total': grand_total,})
        else:
            return JsonResponse({'status': 'You are not eligible for this coupon'})
            
    return JsonResponse({'status': 'Invalid request'})


# Admin Side Coupon
def admincoupon(request):
    if not request.user.is_superuser:
        return redirect('signin')
    context = {
        'coupon' : Coupon.objects.all().order_by('-id')
    }
    return render (request,"Admin/coupon.html" ,context)

# Admin Add Coupon             
def addcoupon(request):
    if not request.user.is_superuser:
        return redirect('signin')
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        discount = request.POST.get('discount')
        min_value = request.POST.get('min_value')
        valid_from = request.POST.get('valid_from')
        valid_till = request.POST.get('valid_till')
# Validaiton
        if coupon_code.strip() == '':
            messages.error(request,'Coupon code is empty')
            return redirect('admincoupon')
        if (discount != '' and int(discount) > 30):
            messages.error(request, 'Invalid discount')
            return redirect('admincoupon')
        if min_value == '':
            messages.error(request,'min_value is empty')
            return redirect('admincoupon')
        if Coupon.objects.filter(coupon_code=coupon_code).exists():
            messages.error(request, 'coupon_code already exists')
            return redirect('admincoupon')
        try:
            active = request.POST.get('checkbox', False)
            if active == 'on':
                active = True
            else:
                active = False
        except:
            active = False
        try:
            coupon = Coupon.objects.create(
                coupon_code=coupon_code,
                discount=discount,
                min_value=min_value,
                valid_from=valid_from,
                valid_till=valid_till,
                active=active
            )
            coupon.save()
            return redirect('admincoupon')
        except ValidationError:
            messages.error(request, 'Invalid date format')
            return redirect('admincoupon')
        
# Admin Edit Coupon
def edicoupon(request,edit_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        discount = request.POST.get('discount')
        min_value = request.POST.get('min_value')
        if coupon_code.strip() == '':
            messages.error(request,'Coupon code is empty')
            return redirect('admincoupon')
        if (discount != '' and int(discount) > 30):
            messages.error(request, 'Invalid discount')
            return redirect('admincoupon')
        if min_value == '':
            messages.error(request,'min_value is empty')
            return redirect('admincoupon')
        try:
            active = request.POST.get('checkbox', False)
            if active == 'on':
                active = True
            else:
                active = False
        except:
            active = False
        coupon = Coupon.objects.get(id = edit_id)
        try:
            existing_coupon = Coupon.objects.exclude(id=edit_id).get(coupon_code=coupon_code)
            messages.error(request, 'Coupon code already exists')
            return redirect('admincoupon')
        except Coupon.DoesNotExist:
            coupon.coupon_code = coupon_code
            coupon.save()
        try:
            coupon.discount = discount
            coupon.save()
        except:
            pass
        try:
            valid_from = request.POST.get('valid_from')
            coupon.min_value = min_value
            coupon.save()
        except ValidationError:
            return redirect('admincoupon')
        try:
            valid_till = request.POST.get('valid_till')
            coupon.valid_from = valid_from
            coupon.save()
        except ValidationError:
            return redirect('admincoupon')
        try:
            coupon.valid_till = valid_till
            coupon.save()
        except:
            pass
        coupon.active = active
        coupon.save()
    return redirect('admincoupon')

# Delete Coupon
def deletecoupon(request,delete_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    coupon = Coupon.objects.get(id = delete_id)
    coupon.delete()
    return redirect('admincoupon')

 