from django.db import models

class Account(models.Model):
    email      = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    password   = models.CharField(max_length=1000)

    class Meta:
        db_table = 'accounts'
