from .models import Transaction, TransactionPreset
from django import forms
from django.forms import ModelForm, widgets
from .validators import validate_file_extension_csv

class TransactionForm(ModelForm):
    formId = ''
    action = ''
    title = ''
    formWrapperClass = 'form-wrapper'

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
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['min'] = 0

    class Meta:
        model = Transaction
        fields = '__all__'
        exclude = ('user',)
        widgets = {
            'date': widgets.DateInput(attrs={'type': 'date'}),
            'amount': widgets.NumberInput(attrs={'inputmode': 'decimal'})
        }

class PresetTransactionForm(ModelForm):

    formId = 'presetTransactionForm'
    action = '/presetTransactions/new/'
    title = 'Create Preset'
    formWrapperClass = 'form-wrapper'

    iconClasses = {
        'name': 'bi bi-quote icon-left',
        'vendor': 'bi bi-shop icon-left',
        'reason': 'bi bi-question-square icon-left',
        'category': 'bi bi-card-list icon-left',
        'method': 'bi bi-credit-card icon-left',
        'amount': 'bi bi-currency-dollar icon-left'
    }

    def __init__(self, *args, **kwargs):
        super(PresetTransactionForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['min'] = 0

    prevUrl = forms.CharField(widget = forms.HiddenInput(), required = False)



    class Meta:
        model = TransactionPreset
        fields = '__all__'
        exclude = ('user', 'date', 'isExpense')
        widgets = {
            'amount': widgets.NumberInput(attrs={'inputmode': 'decimal'})
        }
    

class ImportForm(forms.Form):
    formId = 'importForm'
    action = '/import/'
    hasEncType = True
    enctype = 'multipart/form-data'
    formWrapperClass = 'form-wrapper'

    iconClasses = {
        'csvFile': 'bi bi-file-earmark-plus icon-left'
    }

    prevUrl = forms.CharField(widget = forms.HiddenInput(), required = False)
    csvFile = forms.FileField(validators=[validate_file_extension_csv], label="CSV file")

class ChartFilterForm(forms.Form):
    formId = 'chartFilterForm'
    action = '/dashboard/'
    title = 'Filter Chart'
    formWrapperClass = 'filter-form-wrapper'

    iconClasses = {
        'startDate': 'bi bi-calendar-date icon-left',
        'endDate': 'bi bi-calendar-date icon-left',
    }

    startDate = forms.DateField(widget = widgets.DateInput(attrs={'type': 'date'}), label='Start Date')
    endDate = forms.DateField(widget = widgets.DateInput(attrs={'type': 'date'}), label='End Date')
    preset = forms.CharField(widget = forms.HiddenInput(), required=False)

