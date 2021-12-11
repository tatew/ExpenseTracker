from django.db import models
from django.db.models.base import Model
from .models import BalanceChange
from django import forms #import ModelForm, widgets
from django.forms import ModelForm, widgets
from .validators import validate_file_extension_csv

class ExpenseForm(ModelForm):
    formId = 'expenseForm'
    action = '/logExpense/'

    iconClasses = {
        'date': 'bi bi-calendar-date icon-left',
        'vendor': 'bi bi-shop icon-left',
        'reason': 'bi bi-question-square icon-left',
        'category': 'bi bi-card-list icon-left',
        'method': 'bi bi-credit-card icon-left',
        'amount': 'bi bi-currency-dollar icon-left'
    }

    prevUrl = forms.CharField(widget = forms.HiddenInput(), required = False)

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['min'] = 0

    class Meta:
        model = BalanceChange
        fields = '__all__'
        exclude = ('user',)
        widgets = {
            'date': widgets.DateInput(attrs={'type': 'date'}),
            'amount': widgets.NumberInput(attrs={'pattern': '\d*'})
        }

class ImportForm(forms.Form):
    formId = 'importForm'
    action = '/import/'

    iconClasses = {
        'file': 'bi bi-file-earmark-plus icon-left'
    }

    prevUrl = forms.CharField(widget = forms.HiddenInput(), required = False)
    file = forms.FileField(validators=[validate_file_extension_csv])
