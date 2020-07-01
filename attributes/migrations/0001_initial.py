from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'colors',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'materials',
            },
        ),
        migrations.CreateModel(
            name='Shape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'shapes',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_main', models.CharField(max_length=50, null=True)),
                ('size_sub', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'sizes',
            },
        ),
        migrations.CreateModel(
            name='Texture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'textures',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'themes',
            },
        ),
        migrations.CreateModel(
            name='ThemeProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attributes.Theme')),
            ],
            options={
                'db_table': 'theme_products',
            },
        ),
        migrations.AddField(
            model_name='theme',
            name='product',
            field=models.ManyToManyField(related_name='theme', through='attributes.ThemeProduct', to='products.Product'),
        ),
        migrations.CreateModel(
            name='TextureProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('texture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attributes.Texture')),
            ],
            options={
                'db_table': 'texture_products',
            },
        ),
        migrations.AddField(
            model_name='texture',
            name='product',
            field=models.ManyToManyField(related_name='texture', through='attributes.TextureProduct', to='products.Product'),
        ),
        migrations.CreateModel(
            name='SizeProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attributes.Size')),
            ],
            options={
                'db_table': 'size_products',
            },
        ),
        migrations.AddField(
            model_name='size',
            name='product',
            field=models.ManyToManyField(related_name='size', through='attributes.SizeProduct', to='products.Product'),
        ),
        migrations.CreateModel(
            name='ShapeProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('shape', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attributes.Shape')),
            ],
            options={
                'db_table': 'shape_products',
            },
        ),
        migrations.AddField(
            model_name='shape',
            name='product',
            field=models.ManyToManyField(related_name='shape', through='attributes.ShapeProduct', to='products.Product'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=500, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'db_table': 'product_images',
            },
        ),
        migrations.CreateModel(
            name='MaterialProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attributes.Material')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'db_table': 'material_products',
            },
        ),
        migrations.AddField(
            model_name='material',
            name='product',
            field=models.ManyToManyField(related_name='material', through='attributes.MaterialProduct', to='products.Product'),
        ),
        migrations.CreateModel(
            name='LookImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=500, null=True)),
                ('look', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Look')),
            ],
            options={
                'db_table': 'look_images',
            },
        ),
        migrations.CreateModel(
            name='ColorProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attributes.Color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'db_table': 'color_products',
            },
        ),
        migrations.AddField(
            model_name='color',
            name='product',
            field=models.ManyToManyField(related_name='color', through='attributes.ColorProduct', to='products.Product'),
        ),
    ]
