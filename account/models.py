from django.db import models
from products.models import (
        Product, 
        Look
)

class Account(models.Model):
    email      = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    password   = models.CharField(max_length=1000)

    class Meta:
        db_table = 'accounts'

class ProductWishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_wishlists'

class LookWishlist(models.Model):
    look    = models.ForeignKey(Look, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        db_table = 'look_wishlists'
