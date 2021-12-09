from django.db import models
from django.db.models.deletion import PROTECT
from django.contrib import auth

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
    category = models.ForeignKey(Category, on_delete=PROTECT)
    method = models.ForeignKey(Method, on_delete=PROTECT)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(auth.get_user_model(), on_delete=PROTECT)