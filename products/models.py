from django.db import models

# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'menus'

class Category(models.Model):
    name = models.CharField(max_length=50, null=True)
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'categories'

class Collection(models.Model):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'collections'

class Product(models.Model):
    product_code = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=50, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'products'

class Look(models.Model):
    name = models.CharField(max_length=50, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='Product_look', related_name='products')

    class Meta:
        db_table = 'looks'

class Product_look(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    look = models.ForeignKey(Look, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_looks'
