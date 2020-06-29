# Generated by Django 3.0.7 on 2020-06-29 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterModelTable(
            name='account',
            table='accounts',
        ),
    ]
