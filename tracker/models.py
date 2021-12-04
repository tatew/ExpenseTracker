from django.db import models

# Create your models here.

class BalanceChange(models.Model):
    date = models.DateField()
    vendor = models.CharField(max_length=200)
    reason = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
