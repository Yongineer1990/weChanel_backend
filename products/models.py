from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'menus'

class Collection(models.Model):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'collections'


class Product(models.Model):
    product_code    = models.CharField(max_length=100, null=True)
    name            = models.CharField(max_length=50, null=True)
    price           = models.DecimalField(max_digits = 14, decimal_places=4, null=True)
    collection      = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True)
    unique_id       = models.IntegerField(null=True)

    class Meta:
        db_table = 'products'

class Category(models.Model):
    name    = models.CharField(max_length=50, null=True)
    menu    = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True)
    product = models.ManyToManyField(Product, through='ProductCategory', related_name='category')

    class Meta:
        db_table = 'categories'

class ProductCategory(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_categories'

class Look(models.Model):
    name        = models.CharField(max_length=50, null=True)
    collection  = models.ForeignKey(Collection, on_delete=models.CASCADE)
    product     = models.ManyToManyField(Product, through='ProductLook', related_name='look')

    class Meta:
        db_table = 'looks'

class ProductLook(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    look    = models.ForeignKey(Look, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_looks'
