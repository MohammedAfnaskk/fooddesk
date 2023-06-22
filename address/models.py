from django.db import models
from django.contrib.auth.models import User
 
class Address(models.Model):
    fullname =models.CharField(blank=True,null=True,max_length=50)
    mobile = models.BigIntegerField(blank=True,null=True,)
    house = models.CharField(blank=True,null=True,max_length=50)
    city = models.CharField(blank=True,null=True,max_length=50)
    state =models.CharField(blank=True,null=True,max_length=50)
    zip =models.CharField(blank=True,null=True,max_length=50)
    country = models.CharField(blank=True,null=True,max_length=50)
    customer = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null= True) 
    
    