from ..services import dataService
from datetime import datetime
from ..forms import TransactionForm, ImportForm, ChartFilterForm

# Always pass user or other things from request as first argument

def buildHomeContext(user):
    sumOfTransactions = dataService.getSumOfTransactionsForMonth(user, datetime.now().month)
    if (sumOfTransactions == None):
        sumOfTransactions = 0
    
    context = {
        'monthlyBalance': "{:,.2f}".format(sumOfTransactions)
    }

    return context
    
def buildLogExpenseSuccessContext(user, form):
    expense = dataService.createExpenseFromForm(form, user)
    context = {
        'expense': expense
    }
    return context

def buildLogExpenseFormErrorsContext(form):
    context = {
        'form': form,
        'submit': True,
        'cancelBack': True
    }

    return context

def buildLogExpenseFormContext(prevUrl):
    form = TransactionForm(initial={'prevUrl': prevUrl, 'date': datetime.now()})
    form.formId = 'expenseForm'
    form.action = '/logExpense/'
    form.title = 'Log Expense'

    context = {
        'form': form,
        'submit': True,
        'cancelBack': True
    }
    return context