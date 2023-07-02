 
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
     
    def __str__(self):
        return self.product_name

    def get_min_price(self):
        variations = self.variation_set.all()
        if variations.exists():
            return min(variations.values_list('price_variant', flat=True))
        return 0
    
    def get_max_price(self):
        variations = self.variation_set.all()
        if variations.exists():
            return max(variations.values_list('price_variant', flat=True))
        return 0

class Size(models.Model):
    size = models.CharField( max_length=50)
    def __str__(self):
        return self.size
    

class Variation(models.Model):
    product_variant= models.ForeignKey(Product,on_delete=models.CASCADE)
    size =models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity_variant =models.IntegerField(blank=True,null=True)
    price_variant =models.IntegerField(blank=True,null=True)
    image_variant = models.ImageField(upload_to='photos/product',default='No image available')
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True )

    
    def __str__(self):
       return f"{self.product_variant} - {self.size.size}"
    
    def get_offer(self):
       return self.price_variant - self.offer.discount_amount
