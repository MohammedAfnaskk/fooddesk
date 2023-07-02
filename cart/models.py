from django.db import models
from django.contrib.auth.models import AbstractUser,User
from admindashboard.models import Product, Variation
from address.models import Address

# Create your models here.
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_qty = models.PositiveIntegerField(null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True)
    total_price = models.FloatField(null=True)
    product_qty = models.PositiveIntegerField(null=True)
    payment_mode = models.CharField(max_length=150, null=True)
    payment_id = models.CharField(max_length=250,null=True)
   
    message = models. TextField(null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    price = models.FloatField(null=True)
    quantity = models.IntegerField(null=True)
    orderstatus =(
            ('Pending','Pending'),
            ('Order Confirmed','Order Confirmed'),
            ('Out for delivery','Out for delivery'),
            ('Delivered','Delivered')
    )
    status = models.CharField(max_length=150, choices=orderstatus, default='Pending')

    
    def __str__(self):
        return '{} - {}'.format(self.order.id, self.order.tracking_no)
 
    