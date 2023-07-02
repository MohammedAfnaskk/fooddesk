from django.db import models
from django.contrib.auth.models import User
from admindashboard.models import Product, Variation


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='whishlist')
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, related_name='whishlist')
    created_at = models.DateTimeField(auto_now_add=True)



 