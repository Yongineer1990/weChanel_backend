from django.db import models

# Create your models here.

class Menus(models.Model):
    name = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'menus'

class Categories(models.Model):
    name = models.CharField(max_length=50, null=True)
    menu = models.ForeignKey('Menus', on_delete=models.SET_NULL, null=False)

    class Meta:
        db_table = 'categories'

class Collections(models.Model):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'collections'

class Looks(models.Model):
    name = models.CharField(max_length=50, null=True)
    collection = models.ForeignKey('Collections', on_delete=models.SET_NULL, null=False)
    product = models.ForeignKey('Products', on_delete=models.SET_NULL, null=False)

    class Meta:
        db_table = 'looks'

class Products(models.Model):
    product_code = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=50, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    category = models.ForeignKey('Categories', on_delete=models.SET_NULL, null=False)
    collection = models.ForeignKey('Collections', on_delete=models.SET_NULL, null=False)

    class Meta:
        db_table = 'products'
