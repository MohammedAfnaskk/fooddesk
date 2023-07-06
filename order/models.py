from django.db import models
from cart.models import Order
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

# Create your models here.
class Orderreturn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    image = models.ImageField(upload_to='photos/')
    
  

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.BigIntegerField(null=True)
    
    def __int__(self):
        return self.wallet