from django.db import models
from products.models import (
    Look,
    Product
)

class Theme(models.Model):
    name    = models.CharField(max_length=50, null=True)
    product = models.ManyToManyField(Product, through='ThemeProduct', related_name='theme')

    class Meta:
        db_table = 'themes'

class ThemeProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    theme   = models.ForeignKey(Theme, on_delete=models.CASCADE)

    class Meta:
        db_table = 'theme_products'

class Shape(models.Model):
    name    = models.CharField(max_length=50, null=True)
    product = models.ManyToManyField(Product, through='ShapeProduct', related_name='shape')

    class Meta:
        db_table = 'shapes'

class ShapeProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shape   = models.ForeignKey(Shape, on_delete=models.CASCADE)

    class Meta:
        db_table = 'shape_products'

class Texture(models.Model):
    name    = models.CharField(max_length=50, null=True)
    product = models.ManyToManyField(Product, through='TextureProduct', related_name='texture')

    class Meta:
        db_table = 'textures'

class TextureProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    texture = models.ForeignKey(Texture, on_delete=models.CASCADE)

    class Meta:
        db_table = 'texture_products'

class Color(models.Model):
    name    = models.CharField(max_length=50, null=True)
    product = models.ManyToManyField(Product, through='ColorProduct', related_name='color')

    class Meta:
        db_table = 'colors'

class ColorProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color   = models.ForeignKey(Color, on_delete=models.CASCADE)

    class Meta:
        db_table = 'color_products'

class Material(models.Model):
    name    = models.CharField(max_length=50, null=True)
    product = models.ManyToManyField(Product, through='MaterialProduct', related_name='meterial')

    class Meta:
        db_table = 'materials'

class MaterialProduct(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    material    = models.ForeignKey(Material, on_delete=models.CASCADE)

    class Meta:
        db_table = 'material_products'

class Size(models.Model):
    size_main   = models.CharField(max_length=50, null=True)
    size_sub    = models.CharField(max_length=50, null=True)
    product     = models.ManyToManyField(Product, through='SizeProduct', related_name='size')

    class Meta:
        db_table = 'sizes'

class SizeProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size    = models.ForeignKey(Size, on_delete=models.CASCADE)

    class Meta:
        db_table = 'size_products'

class ProductImage(models.Model):
    url     = models.URLField(max_length=500, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_images'

class LookImage(models.Model):
    url     = models.URLField(max_length=500, null=True)
    look    = models.ForeignKey(Look, on_delete=models.CASCADE)

    class Meta:
        db_table = 'look_images'
