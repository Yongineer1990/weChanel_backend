from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'collections',
            },
        ),
        migrations.CreateModel(
            name='Look',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Collection')),
            ],
            options={
                'db_table': 'looks',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'menus',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=100, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('price', models.DecimalField(decimal_places=4, max_digits=14, null=True)),
                ('unique_id', models.IntegerField(null=True)),
                ('collection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Collection')),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='ProductLook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('look', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Look')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'db_table': 'products_looks',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'db_table': 'products_categories',
            },
        ),
        migrations.AddField(
            model_name='look',
            name='product',
            field=models.ManyToManyField(related_name='look', through='products.ProductLook', to='products.Product'),
        ),
        migrations.AddField(
            model_name='category',
            name='menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Menu'),
        ),
        migrations.AddField(
            model_name='category',
            name='product',
            field=models.ManyToManyField(related_name='category', through='products.ProductCategory', to='products.Product'),
        ),
    ]
