from django.db import models

# Create your models here.

class Account(models.Model):
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=1000)

    # To manually create the name of db table above:
    class Meta:
        db_table = 'account'

#class Product_wishlists(models.Model):
    #this wishlist has two foreign keys, which are 1. product and 2. account
#   product = models.ForeignKey(Product, on_delete=models.CASCADE)
#    account = models.ForeignKey(Account, on_delete=models.CASCADE)

#   class Meta:
#        db_table = 'product_wishlists'

#class Look_wishlists(models.Model):
    #this wishlist has two foreign keys, which are 1. look and 2. account
#    look = models.ForeignKey(Look, on_delete=models.CASCADE)
#    account = models.ForeignKey(Account, on_delete=models.CASCADE)

#    class Meta:
#        db_table = 'look_wishlists'

