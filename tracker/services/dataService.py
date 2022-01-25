from ..models import Transaction, Category, Method
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Sum

def getMonthlyResultsData():
    oldestDate = Transaction.objects.values('date').order_by('date').first()['date']
    months = []
    iteratorDate = datetime(oldestDate.year, oldestDate.month, 1)
    currentDate = datetime(datetime.now().year, datetime.now().month, 1)
    while (iteratorDate <= currentDate):
        months.append({'year': iteratorDate.year, 'month': iteratorDate.month})
        iteratorDate = iteratorDate + relativedelta(months=1)

    return months

def getTransactionsForMonth(user, month):
    return Transaction.objects.filter(date__month=month, user=user)

def getTransactionsForDateRange(user, startDate, endDate):
    return Transaction.objects.filter(user=user, date__gte=startDate, date__lte=endDate).order_by('-date')

def getSumOfTransactionsForMonth(user, month):
    return getTransactionsForMonth(user, month).aggregate(Sum('amount'))['amount__sum']

def getLastNTransactions(user, numToTake):
    return Transaction.objects.filter(user=user).order_by('-date', '-amount')[:numToTake + 1]

def getTransactionById(id):
    return Transaction.objects.get(id=id)

def getIncomesByDate(user, startDate, endDate):
    incomes = Transaction.objects.filter(user=user, amount__gt=0, date__gte=startDate, date__lte=endDate).order_by('-date')
    return incomes.values('date').order_by('date').annotate(total=Sum('amount'))

def getExpensesByDate(user, startDate, endDate):
    expenses = Transaction.objects.filter(user=user, amount__lt=0, date__gte=startDate, date__lte=endDate).order_by('-date')
    return expenses.values('date').order_by('date').annotate(total=Sum('amount'))

def getNetByDate(user, startDate, endDate):
    transactions = Transaction.objects.filter(user=user, date__gte=startDate, date__lte=endDate).order_by('-date')
    return transactions.values('date').order_by('date').annotate(total=Sum('amount'))

def getTransactionsForCategoryInDateRange(user, category, startDate, endDate):
    transactions = getTransactionsForDateRange(user, startDate, endDate)
    return transactions.filter(category=category)

def getNetTransactionsForCategoryInDateRange(user, category, startDate, endDate):
    transactionsForCategory = getTransactionsForCategoryInDateRange(user, category, startDate, endDate)
    return transactionsForCategory.aggregate(Sum('amount'))['amount__sum']

def getCategories():
    return Category.objects.all()

def createExpenseFromForm(form, user):
    expense = Transaction(
        date = form.cleaned_data['date'],
        reason = form.cleaned_data['reason'],
        vendor = form.cleaned_data['vendor'],
        method = form.cleaned_data['method'],
        category = form.cleaned_data['category'],
        amount = form.cleaned_data['amount'] * -1,
        user = user
    )
    expense.save()
    return expense