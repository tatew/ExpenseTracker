from django.db import models
from django.db.models.deletion import PROTECT
from django.contrib import auth
import datetime 

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

class Transaction(models.Model):
    date = models.DateField()
    vendor = models.CharField(max_length=200)
    reason = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=PROTECT)
    method = models.ForeignKey(Method, on_delete=PROTECT)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(auth.get_user_model(), on_delete=PROTECT)

    def __str__(self):
        typeOfTransaction = ""
        fromOrAt = ""
        if (self.amount < 0):
            typeOfTransaction = "Expense"
            fromOrAt = "at"
        else:
            typeOfTransaction = "Income"
            fromOrAt = "from"
        date = datetime.date.strftime(self.date, "%m/%d/%Y")
        return f"{typeOfTransaction} of ${abs(self.amount)} on {date} {fromOrAt} {self.vendor}"

class TransactionPreset(models.Model):
    name = models.CharField(max_length=100)
    isExpense = models.BooleanField()
    vendor = models.CharField(max_length=200, null=True, blank=True)
    reason = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=PROTECT, null=True, blank=True)
    method = models.ForeignKey(Method, on_delete=PROTECT, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(auth.get_user_model(), on_delete=PROTECT)