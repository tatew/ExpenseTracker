from django.db import models
from .models import BalanceChange
from django.forms import Form

class ExpenseForm(Form):
    class Meta:
        fields = ['date', 'reason', 'vendor', 'category', 'method', 'amount']