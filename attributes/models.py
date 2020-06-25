from django.db import models
from products.models import Look, Product
# Create your models here.

class Theme(models.Model):
    name = models.CharField(max_length=50, null=True)
    product = models.ManyToManyField(Product, through='Theme_Product', related_name='product')

    class Meta:
        db_table = 'themes'

class Theme_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    class Meta:
        db_table = 'theme_product'

class Shape(models.Model):
    name = models.CharField(max_length=50, null=True)
    product = models.ManyToManyField(Product, through='Shape_Product', related_name='product')

    class Meta:
        db_table = 'shape'

class Shape_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shape = models.ForeignKey(Shape, on_delete=models.CASCADE)

    class Meta:
        db_table = 'shape_product'

class Texture(models.Model):
    name = models.CharField(max_length=50, null=True)
    product = models.ManyToManyField(Product, through='Texture_Product', related_name='product')

    class Meta:
        db_table = 'texture'

class Texture_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    texture = models.ForeignKey(Texture, on_delete=models.CASCADE)

    class Meta:
        db_table = 'texture_product'

class Color(models.Model):
    name = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'color'

class Color_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    class Meta:
        db_table = 'color_product'


class Material(models.Model):
    name = models.CharField(max_length=50, null=True)
    product = models.ManyToManyField(Product, through='Material_Product', related_name='product')

    class Meta:
        db_table = 'material'

class Material_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    class Meta:
        db_table = 'material_product'

class Size(models.Model):
    size_main = models.CharField(max_length=50, null=True)
    size_sub = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'size'

class Size_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    class Meta:
        db_table = 'size_product'

class Product_Image(models.Model):
    url = models.CharField(max_length=2000, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_image'

class Look_Image(models.Model):
    url = models.CharField(max_length=2000, null=True)
    look = models.ForeignKey(Look, on_delete=models.CASCADE)

    class Meta:
        db_table = 'look_image'
