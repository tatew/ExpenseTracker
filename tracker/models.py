from django.db import models
from django.db.models.deletion import PROTECT

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Method(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BalanceChange(models.Model):
    date = models.DateField()
    vendor = models.CharField(max_length=200)
    reason = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=PROTECT, null=True)
    method = models.ForeignKey(Method, on_delete=PROTECT, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)