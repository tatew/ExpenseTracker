from ..models import Transaction, Category, Method, TransactionPreset
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from ..utilities import expenseTrackerUtilities

def getMonthsFromFirstMonthWithData(user):
    oldestDate = Transaction.objects.filter(user=user).values('date').order_by('date').first()['date']
    months = []
    iteratorDate = datetime(oldestDate.year, oldestDate.month, 1)
    currentDate = datetime(datetime.now().year, datetime.now().month, 1)
    while (iteratorDate <= currentDate):
        months.append({'year': iteratorDate.year, 'month': iteratorDate.month})
        iteratorDate = iteratorDate + relativedelta(months=1)

    return months

def getTransactionsForMonth(user, year, month):
    return Transaction.objects.filter(date__year=year, date__month=month, user=user)

def getIncomesForMonth(user, year, month):
    return Transaction.objects.filter(date__year=year, date__month=month, user=user, amount__gt=0,)

def getExpensesForMonth(user, year, month):
    return Transaction.objects.filter(date__year=year, date__month=month, user=user, amount__lt=0,)

def getTransactionsForDateRange(user, startDate, endDate):
    return Transaction.objects.filter(user=user, date__gte=startDate, date__lte=endDate).order_by('-date')

def getLastNTransactions(user, numToTake):
    return Transaction.objects.filter(user=user).order_by('-date', '-amount')[:numToTake]

def getTransactionById(id):
    return Transaction.objects.get(id=id)

def getIncomeTotalsByDate(user, startDate, endDate):
    incomes = Transaction.objects.filter(user=user, amount__gt=0, date__gte=startDate, date__lte=endDate).order_by('-date')
    return incomes.values('date').order_by('date').annotate(total=Sum('amount'))

def getExpenseTotalsByDate(user, startDate, endDate):
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
    method = getMethodById(form.cleaned_data['method'].id)
    if (not method.active):
        return 

    expense = Transaction(
        date=form.cleaned_data['date'],
        reason=form.cleaned_data['reason'],
        vendor=form.cleaned_data['vendor'],
        method=form.cleaned_data['method'],
        category=form.cleaned_data['category'],
        amount=form.cleaned_data['amount'] * -1,
        user=user
    )
    expense.save()
    return expense

def createIncomeFromForm(form, user):
    method = getMethodById(form.cleaned_data['method'].id)
    if (not method.active):
        return 
    
    income = Transaction(
        date=form.cleaned_data['date'],
        reason=form.cleaned_data['reason'],
        vendor=form.cleaned_data['vendor'],
        method=form.cleaned_data['method'],
        category=form.cleaned_data['category'],
        amount=form.cleaned_data['amount'],
        user=user
    )
    income.save()
    return income

def createPresetTransactionFromForm(form, user):
    method = getMethodById(form.cleaned_data['method'].id)
    if (not method.active):
        return 

    preset = TransactionPreset(
        name=form.cleaned_data['name'],
        isExpense=form.cleaned_data['isExpense'],
        reason=form.cleaned_data['reason'],
        vendor=form.cleaned_data['vendor'],
        method=form.cleaned_data['method'],
        category=form.cleaned_data['category'],
        amount=form.cleaned_data['amount'],
        user=user
    )

    preset.save()
    return preset

def getOldestTransaction(user):
    return Transaction.objects.filter(user=user).all().order_by('date')[0]

def getNewestTransaction(user):
    return Transaction.objects.filter(user=user).all().order_by('-date')[0]

def getTransactionPresetsForUser(user):
    return TransactionPreset.objects.filter(user=user).order_by('name')

def getTransactionPresetById(id):
    return TransactionPreset.objects.get(id=id)

def getMethodsForUser(user):
    return Method.objects.filter(user=user).order_by('name')

def getActiveMethodsForUser(user):
    return Method.objects.filter(user=user, active=True).order_by('name')

def getMethodById(id):
    return Method.objects.get(id=id)

def createMethodFromForm(form, user):
    method = Method(
        name=form.cleaned_data['name'],
        user=user
    )

    method.save()
    return method

def updateMethodFromForm(form, user, id):
    method = getMethodById(id)
    if (method.user != user):
       return 
    else:
        method.name = form.cleaned_data['name']
        method.save()
        return method

def methodToggleActive(user, id):
    method = getMethodById(id)
    if (method.user != user):
       return 
    else:
        method.active = not method.active
        method.save()
        return method

def getTransactionsForFilter(user, transactionFilter):
    return Transaction.objects.filter(user=user, vendor__icontains=transactionFilter['vendor'])