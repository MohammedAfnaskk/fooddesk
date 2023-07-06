
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from admindashboard.models import *
from django.contrib import auth
from cart.models import Order,OrderItem
from address.models import Address
from slugify import slugify
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.db.models import Sum
from datetime import datetime,timedelta
from django.db.models.functions import TruncDay
from django.db.models import DateField
from django.db.models.functions import Cast
import datetime
from reportlab.pdfgen import canvas
from io import BytesIO
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import csv
 





@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('signin')

    delivered_items = OrderItem.objects.filter(status='Order Confirmed')

    revenue = 0
    for item in delivered_items:
        revenue += item.order.total_price
    print(revenue)
    top_selling = OrderItem.objects.annotate(total_quantity=Sum('quantity')).order_by('-total_quantity').distinct()[:5]

    recent_sale = OrderItem.objects.all().order_by('-id')[:5]

    today = datetime.date.today()
    date_range = 7

    four_days_ago = today - timedelta(days=date_range)

    orders = Order.objects.filter(created_at__gte=four_days_ago, created_at__lte=today)

    sales_by_day = orders.annotate(day=TruncDay('created_at')).values('day').annotate(total_sales=Sum('total_price')).order_by('day')

    sales_dates = Order.objects.annotate(sale_date=Cast('created_at', output_field=DateField())).values('sale_date').distinct()

    context = {
        'total_users':User.objects.count(),
        'sales':OrderItem.objects.count(),
        'revenue':revenue,  
        'top_selling':top_selling,
        'recent_sales':recent_sale,
        'sales_by_day':sales_by_day,
        'sales_dates': sales_dates,
    }
    return render(request,'Admin/dashboard.html',context)

     

def signout(request):
   auth.logout(request)
   return redirect('signin')
 
# user
def userlist(request):
    if not request.user.is_superuser:
        return redirect('signin')
    users=User.objects.all().order_by('id')
    return render(request,"Admin/user_list.html",{'users':users})

# Block User
def blockuser(request,user_id):
    if not request.user.is_superuser:
        return redirect('signin')
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect("userlist")
#product
def productlist(request):
    if not request.user.is_superuser:
        return redirect('signin')
    dict_list={
        'prod':Product.objects.all()
     }
    return render(request,"Admin/productlist.html",dict_list)

# Add product
def addproduct(request):
    if not request.user.is_superuser:
        return redirect('signin')
    if request.method == 'POST':
        name= request.POST['product_name']
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        description=request.POST['product_description']
      
        
        # Validaiton
        if Product.objects.filter(product_name=name).exists():
            messages.error(request,'Product name already exists')
            return redirect('addproduct')
     
        
        #Save
        product =Product(product_name =name,
                         product_description = description,
                         category= category)
        product.save()
        return redirect('productlist')
    context = {
        'category' : Category.objects.all()
    }
    return render(request,"Admin/addproduct.html",context) 
# edit product
def editproduct(request, prod_id):
    if not request.user.is_superuser:
        return redirect('signin')
    try:
       prd = Product.objects.get(id=prod_id)
    except Product.DoesNotExist:
        messages.error(request, 'orderitem_not_found')
        return redirect('productlist')

    if request.method == 'POST':
        name = request.POST['product_name']
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)        
        description = request.POST['product_description']
        

        # # Validation
        if Product.objects.filter(product_name=name).exclude(id=prod_id).exists():
            messages.error(request, 'Product name already exists')
            return redirect('editproduct', prod_id=prod_id)

      
        # Save
        prd.product_name = name
        prd.product_description = description
        prd.category = category
        prd.save()
        return redirect('productlist')
    context = {
        'prd': prd,
        'category': Category.objects.all()
    }
    return render(request, 'Admin/editproduct.html',context)  

# delete product
def deleteproduct(request,prod_id):
    if not request.user.is_superuser:
        return redirect('signin')
    prod = Product.objects.get(id=prod_id)
    prod.delete()
    messages.success(request,'Product Deleted successfully')
    return redirect('productlist')
 
def orderlist(request):
    if not request.user.is_superuser:
        return redirect('signin')
    orders = OrderItem.objects.all()
    context = {
        'orders': orders
    }
    return render(request, "Admin/vieworder.html", context)

 

def update_status(request, order_item_id):
    if not request.user.is_superuser:
        return redirect('signin')
    order_item = OrderItem.objects.get(id=order_item_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        order_item.status = status
        order_item.save()
        return redirect('orderlist')

def category(request):
    if not request.user.is_superuser:
        return redirect('signin')
    context={
        'catg':Category.objects.all()
    }
    return render(request,"Admin/category.html",context)

def addcategory(request):
    if not request.user.is_superuser:
        return redirect('signin')
    if request.method =='POST':
        name = request.POST.get('category_name')
        discription = request.POST.get('category_description')
        image = request.FILES.get('category_image')
    
 # Validation
        if not name.strip():
            messages.error(request, 'Name field is empty')
            return redirect('category')
        if not image:
            messages.error(request, 'Image not uploaded')
            return redirect('category')
        
# Save          
        slug = slugify(name)

        categ = Category(category_name = name,category_description = discription,category_image=image,slug = slug)
        categ .save()
        return redirect("category")

    return render(request,'Admin/addcategory.html')
 

 
 
def editcategory(request, editcategory_id):
    if not request.user.is_superuser:
        return redirect('signin')
    try:
       category_obj = Category.objects.get(id=editcategory_id)
    except Category.DoesNotExist:
        messages.error(request, 'editcategory_not_found')
        return redirect('category')
    if request.method == 'POST':
        name = request.POST['category_name']
        description = request.POST['category_description']
        
        # Validation
        try:
            category_obj = Category.objects.get(id=editcategory_id)
            image = request.FILES.get('image')
            if image:
                category_obj.categories_image = image
                category_obj.save()
        except Category.DoesNotExist:
            messages.error(request, 'Image Not Found')
            return redirect('category')
        
        if name.strip() == '':
            messages.error(request, 'Name field is empty')
            return redirect('category')

        category_obj = Category.objects.get(id=editcategory_id)
        category_obj.category_name = name
        category_obj.category_description = description
        category_obj.save()
        return HttpResponse("Category edited successfully")  # Example response

        # Add any additional context data needed for the template
        
    return render(request, 'Admin/editcategory.html',{'category': category_obj})
 

    
def deletecategory(request,deletecategory_id):
    if not request.user.is_superuser:
        return redirect('signin')
    categre = Category.objects.get(id=deletecategory_id)
    categre.delete()
    return redirect('category')

# Sales reprt
def salesreport(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    context = {}
    if request.method == 'POST':
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        
        if start_date == '' or end_date == '':
            messages.error(request, 'Give date first')
            return redirect(salesreport)
            
        if start_date == end_date:
            date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            order_items = OrderItem.objects.filter(order__created_at__date=date_obj.date())
            if order_items:
                context.update(sales=order_items, s_date=start_date, e_date=end_date)
                return render(request, 'admin/salesreport.html', context)
            else:
                messages.error(request, 'No data found')
            return redirect(salesreport)
        order_items = OrderItem.objects.filter(order__created_at__date__gte=start_date, order__created_at__date__lte=end_date)
        
        if order_items:
            context.update(sales=order_items, s_date=start_date, e_date=end_date)
        else:
            messages.error(request, 'No data found')
    else:    
         # Get the current month and year
        current_date = datetime.date.today()
        current_month = current_date.month
        current_year = current_date.year   
     
          # Get the start and end dates of the current month
        start_date = f'{current_year}-{current_month:02d}-01'
        end_date = current_date.strftime('%Y-%m-%d')

        
            # Query the sales data for the current month
        order_items = OrderItem.objects.filter(order__created_at__date__gte=start_date, order__created_at__date__lte=end_date)
        


        if order_items:
            context.update(sales=order_items, s_date=start_date, e_date=end_date)
        else:
            messages.error(request, 'No data found')
   
    # Check if the user requested a download
    if request.GET.get('download') == '1':
        # Generate the sales report data
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        order_items = OrderItem.objects.filter(order__created_at__date__gte=start_date, order__created_at__date__lte=end_date)

        # Create a list to store the table data
        table_data = [['ID', 'Date', 'Customer', 'Product Name', 'Quantity', 'Total Price']]
   
        # Populate the table data with the relevant sales data
        for item in order_items:
           table_data.append([item.order.id, item.order.created_at.date(), item.order.address.customer, item.product.product_name, item.quantity, item.order.total_price])

        # Create a PDF document
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        elements = []

        # Create the table and set its style
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Add the table to the PDF document
        elements.append(table)

        # Build the PDF document
        doc.build(elements)

        # Set the appropriate response headers for downloading the PDF
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
        return response
    
    #    # excel download
    # if 'download' in request.GET:
    #     sales = context.get('sales')
    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

    #     writer = csv.writer(response)
    #     writer.writerow(['Order ID', 'Customer', 'Quantity', 'product', 'Price'])

    #     for sale in sales :
    #         writer.writerow([
    #             sale.order.id,
    #             sale.order.address.customer,
    #             sale.quantity,
    #             sale.product.product_name,
    #             sale.order.total_price
    #         ])
    #     return response

    return render(request, 'Admin/salesreport.html', context)





def addproduct_variant(request):
    if not request.user.is_superuser:
        return redirect('signin')

    if request.method == 'POST':
        product_nam = request.POST['product_variant']
        size = request.POST['size']
        image = request.FILES.get('image_variant', None)
        quantity = request.POST.get('quantity_variant')
        price = request.POST.get('price_variant')
        offer = request.POST.get('offer')


        # Validation
        if offer == 'No offer':
            offer_id = None
        else:
            offer_id = Offer.objects.get(id=offer)
        try:
            
            product = Product.objects.get(id=product_nam)
        except Product.DoesNotExist:
            messages.error(request, 'Product does not exist')
            return redirect('addproduct_variant')

        try:
            size_obj= Size.objects.get(id=size)
        except Size.MultipleObjectsReturned:
            messages.error(request, 'Multiple sizes found')
            return redirect('addproduct_variant')

        if Variation.objects.filter(product_variant=product, size=size_obj).exists():
            messages.error(request, 'This variant already exists')
            return redirect('addproduct_variant')

        if not image:
            messages.error(request, 'Image not uploaded')

        if not quantity:
            messages.error(request, 'Quantity is blank')

        if not price:
            messages.error(request, 'Price not included')
            return redirect('addproduct_variant')

        variation = Variation()
        variation.product_variant = product
        variation.size = size_obj
        variation.quantity_variant = quantity
        variation.price_variant = price
        variation.image_variant = image
        variation.offer = offer_id
        variation.save()

    context = {
        'variation': Variation.objects.all(),
        'size':Size.objects.all(),
        'product':Product.objects.all(),
        'offer':Offer.objects.all(),
            
    }
    return render(request, 'Admin/addproduct_variant.html', context)

def edit_variation(request, variation_id):
    if not request.user.is_superuser:
        return redirect('signin')
    variations = Variation.objects.filter(id = variation_id)
  
    try:
        variation = Variation.objects.get(id=variation_id)
    except Variation.DoesNotExist:
        messages.error(request, 'Variation does not exist')
        return redirect('addproduct_variant')
  
    if request.method == 'POST':
        product_name = request.POST['product_variant']
        size = request.POST['size']
        image = request.FILES.get('image_variant', variation.image_variant)
        quantity = request.POST.get('quantity_variant')
        price = request.POST.get('price_variant')
        offer = request.POST.get('offer')


        # Validation
        if offer == 'No offer':
           offer_id = None
        else:
           offer_id = Offer.objects.get(id=offer)
        try:
            product = Product.objects.get(id=product_name)
        except Product.DoesNotExist:
            messages.error(request, 'Product does not exist')
            return redirect('edit_variation', variation_id=variation_id)

        try:
            size_obj = Size.objects.get(id=size)
        except Size.DoesNotExist:
            messages.error(request, 'Size does not exist')
            return redirect('edit_variation', variation_id=variation_id)

        if Variation.objects.filter(product_variant=product, size=size_obj).exclude(id=variation_id).exists():
            messages.error(request, 'This variant already exists')
            return redirect('edit_variation', variation_id=variation_id)

        if not image:
            messages.error(request, 'Image not uploaded')

        if not quantity:
            messages.error(request, 'Quantity is blank')

        if not price:
            messages.error(request, 'Price not included')
            return redirect('edit_variation', variation_id=variation_id)

        variation.product_variant = product
        variation.size = size_obj
        variation.quantity_variant = quantity
        variation.price_variant = price
        variation.image_variant = image
        variation.offer = offer_id

        variation.save()

        messages.success(request, 'Variation updated successfully.')
    context = {
        'variation':variations,
        'size':Size.objects.all(),
        'product':Product.objects.all(),
        'offer':Offer.objects.all(),
                
     }
    return render(request, 'Admin/editvariant.html' , context)
 



# Delete Variations
def delete_variation(request, variation_id):
    if not request.user.is_superuser:
        return redirect('signin')
    variation = Variation.objects.get(id = variation_id)
    variation.delete()
    messages.success(request,'Product Deleted successfully')
    return redirect('Product_Variant_list')

def Product_Variant_list(request):
    if not request.user.is_superuser:
        return redirect('signin')
    context ={
        'var':Variation.objects.all().order_by('id')
    }
    return render(request, 'Admin/Variant_list.html', context)

# offer
def adminoffer(request):
    if not request.user.is_superuser:
        return redirect('signin')
    context = {
        'offer' : Offer.objects.all()
    }

    return render (request,'Admin/offer.html',context)


def addoffer(request):
    if not request.user.is_superuser:
        return redirect('signin')
    if request.method =='POST': 
        ordername = request.POST.get('ordername')
        discount = request.POST.get('discount')
        if ordername.strip() == '':
            messages.error(request, "Can't blank order name")
            return redirect('adminoffer')
        if discount.strip() =='':
            messages.error(request, "Can't blank Discount")
            return redirect('adminoffer')
        offer = Offer.objects.create(offer_name=ordername,discount_amount=discount)
        offer.save()
        return redirect('adminoffer')

def editoffer(request,offer_id):
  if not request.user.is_superuser:
    return redirect('signin')
  if request.method == 'POST':
    Offername = request.POST.get('Offername')
    discount = request.POST.get('discount')
    if Offername.strip() == '':
        messages.error(request, "Order name cannot be blank.")
        return redirect('adminoffer')
    if discount.strip() == '':
        messages.error(request, "Can't blank Offer field")
        return redirect('adminoffer')
    try:
        if Offer.objects.filter(id=offer_id,offer_name = Offername).exists():
            pass
        else:
            offer = Offer.objects.get(id=offer_id)
            offer.offer_name = Offername
            offer.save()
            messages.success(request, "Offer name updated successfully.")
    except Offer.DoesNotExist:
        messages.error(request, "The specified offer does not exist.")
        return redirect('adminoffer')

    try:
        if Offer.objects.filter(id=offer_id,discount_amount = discount).exists():
            pass
        else:
            offer = Offer.objects.get(id=offer_id)
            offer.discount_amount = discount
            offer.save()
            messages.success(request, "Offer Discount updated successfully.")
        return redirect('adminoffer')
    except Offer.DoesNotExist:
        messages.error(request, "The specified offer does not exist.")
        return redirect('adminoffer')

def deleteoffer(request,delete_id):
    if not request.user.is_superuser:
        return redirect('signin')
    try:
        offer = Offer.objects.filter(id = delete_id)
        offer.delete()
        return redirect('adminoffer')
    except Offer.DoesNotExist:
        messages.error(request, "The specified offer does not exist.")
        return redirect('adminoffer')

    
    

   
   



