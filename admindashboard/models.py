 
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    category_image = models.ImageField(upload_to='photos/categories',default='No image available')
    category_name = models.CharField(max_length=50, unique=True)
    category_description = models.TextField()
    slug = models.SlugField(max_length=250,unique=True)
    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    def __str__(self) :
        return self.category_name

# Offer
class Offer(models.Model):
    offer_name = models.CharField(max_length=100)
    discount_amount = models.PositiveIntegerField()
    
    def __str__(self):
        return self.offer_name


class Product(models.Model): 
    product_name = models.CharField(unique=True,max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_description = models.TextField()
    image = models.ImageField(upload_to='photos/products',default='No image available')
    quantity = models.IntegerField(blank= False,null=True)
    product_price =models.IntegerField(blank=False,null=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True )

# class Product_Variant(models.Model):
#     product_variant =models.ForeignKey(Product,on_delete=models.CASCADE)
#     size =    
    
