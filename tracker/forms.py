from django.db import models
from django.db.models.base import Model
from .models import BalanceChange
from django.forms import ModelForm, widgets

class ExpenseForm(ModelForm):

    iconClasses = {
        'date': 'bi bi-calendar-date icon-left',
        'vendor': 'bi bi-shop icon-left',
        'reason': 'bi bi-question-square icon-left',
        'category': 'bi bi-card-list icon-left',
        'method': 'bi bi-credit-card icon-left',
        'amount': 'bi bi-currency-dollar icon-left'
    }

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['min'] = 0

    class Meta:
        model = BalanceChange
        fields = '__all__'
        exclude = ('user',)
        widgets = {
            'date': widgets.DateInput(attrs={'type': 'date'}),
            'amount': widgets.TextInput(attrs={'pattern': '\d*'})
        }