from cmath import log
from datetime import datetime
import re
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm, PresetTransactionForm, ImportForm, ChartFilterForm, MethodForm
from .services.importService import importTransactionsCsv
import csv
import io
from calendar import monthrange
from .services import dataService
from .builders import expenseTrackerBuilder
from dateutil.relativedelta import relativedelta

def index(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        return render(request, "tracker/index.html")

def notFound(request, exception):
    return render(request, 'tracker/notFound.html')

def internalServerError(request):
    return render(request, 'tracker/internalServerError.html')

@login_required
def home(request):
    context = expenseTrackerBuilder.buildHomeContext(request.user)
    return render(request, "tracker/home.html", context)

@login_required
def chooseTransactionType(request):
    return render(request, 'tracker/chooseTransactionType.html')

@login_required
def logExpense(request):
    if (request.method == "POST"):
        form = TransactionForm(request.POST)
        if form.is_valid():
            context = expenseTrackerBuilder.buildLogExpenseSuccessContext(request.user, form)
            return render(request, 'tracker/logExpenseSuccess.html', context)
        else:
            context = expenseTrackerBuilder.buildLogExpenseFormErrorsContext(form)
            return render(request, "tracker/fullPageForm.html", context)
    else:
        presetId = request.GET.get('presetTransactionId', '')
        prevUrl = request.GET.get('prevUrl', 'home')
        if (presetId != ''):
            presetTransaction = dataService.getTransactionPresetById(presetId)
            context = expenseTrackerBuilder.buildLogExpenseFormContext(prevUrl, presetTransaction, request.user)
        else:
            context = expenseTrackerBuilder.buildLogExpenseFormContext(prevUrl, None, request.user)
        return render(request, "tracker/fullPageForm.html", context)

@login_required
def logIncome(request):
    if (request.method == "POST"):
        # create a form instance and populate it with data from the request:
        form = TransactionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            context = expenseTrackerBuilder.buildLogIncomeSuccessContext(request.user, form)
            return render(request, 'tracker/logIncomeSuccess.html', context)
        else:
            context = expenseTrackerBuilder.buildLogIncomeErrorsContext(form)
            return render(request, "tracker/fullPageForm.html", context)
    else:
        presetId = request.GET.get('presetTransactionId', '')
        prevUrl = request.GET.get('prevUrl', 'home')
        if (presetId != ''):
            presetTransaction = dataService.getTransactionPresetById(presetId)
            context = expenseTrackerBuilder.buildLogIncomeFormContext(prevUrl, presetTransaction, request.user)
        else:
            context = expenseTrackerBuilder.buildLogIncomeFormContext(prevUrl, None, request.user)
        return render(request, "tracker/fullPageForm.html", context)

@login_required
def listTransactions(request):
    transactionFilter = None
    numToShow = 10
    if (request.method == "POST"):
        category = request.POST['category']
        method = request.POST['method']

        if (category != ''):
            category = int(category)

        if (method != ''):
            method = int(method)

        transactionFilter = {
            'date': request.POST['date'],
            'vendor': request.POST['vendor'],
            'reason': request.POST['reason'],
            'category': category,
            'method': method
        }
        numToShow = int(request.POST['numToShow'])

    context = expenseTrackerBuilder.buildListTransactionsContext(request.user, numToShow, transactionFilter)
    return render(request, "tracker/listTransactions.html", context)

@login_required
def importTransactions(request):
    if (request.method == "POST"):
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                decoded_file = request.FILES['csvFile'].read().decode('utf-8')
            except UnicodeDecodeError as e:
                form.add_error('csvFile', 'Error decoding the file, use .csv files only')
                return render(request, 'tracker/import.html', {'form': form})

            io_string = io.StringIO(decoded_file)
            csvReader = csv.reader(io_string, delimiter=',')
            results = importTransactionsCsv(csvReader, request)
            
            context = {
                'results': results
            }
            return render(request, 'tracker/importResults.html', context)
        else:
            context = {
                'form': form,
                'submit': True
            }
            return render(request, 'tracker/import.html', context)
    else:
        prevUrl = request.GET.get('prevUrl', 'home')
        form = ImportForm(initial={'prevUrl': prevUrl})
        context = {
            'form': form,
            'submit': True
        }
        return render(request, 'tracker/import.html', context)

@login_required
def transaction(request, id):
    transaction = dataService.getTransactionById(id)
    if (transaction.user != request.user):
        raise Http404

    isExpense = transaction.amount < 0

    if (request.method == "POST"):
        # create a form instance and populate it with data from the request:
        form = TransactionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            
            amount = form.cleaned_data['amount'] if not isExpense else form.cleaned_data['amount'] * -1

            transaction.date=form.cleaned_data['date']
            transaction.reason=form.cleaned_data['reason']
            transaction.vendor=form.cleaned_data['vendor']
            transaction.method=form.cleaned_data['method']
            transaction.category=form.cleaned_data['category']
            transaction.amount=amount
            transaction.save()

            return render(request, 'tracker/transactionUpdateSuccess.html', { 'transaction': transaction })
        else:
            context = {
                'form': form,
                'cancelBack': False,
                'cancelDisable': True,
                'delete': False,
                'submit': True,
                'edit': False,
                'disableForm': False,
                'id': id
            }
            return render(request, "tracker/fullPageForm.html", context)
    else:
        prevUrl = request.GET.get('prevUrl', 'home')

        inital = {
            'date': transaction.date,
            'reason': transaction.reason,
            'vendor': transaction.vendor,
            'method': transaction.method,
            'category': transaction.category,
            'amount': abs(transaction.amount),
            'user': transaction.user,
            'prevUrl': prevUrl
        }
        form = TransactionForm(initial=inital)
        form.formId = 'updateTransaction'
        form.action = '/transactions/' + str(id)
        form.title = 'Expense Details' if isExpense else 'Income Details'
        
        context = {
            'form': form,
            'cancelBack': True,
            'cancelDisable': False,
            'delete': True,
            'submit': False,
            'edit': True,
            'disableForm': True,
            'id': id
        }

        return render(request, "tracker/fullPageForm.html", context)

def deleteConfirm(request, id):
    transaction = dataService.getTransactionById(id)
    if (request.method == "POST"):
        transaction.delete()
        return redirect('/transactions')
    else:
        context = {
            'transaction': transaction
        }
        return render(request, 'tracker/deleteConfirm.html', context)

@login_required
def dashboard(request):
    currentYear = datetime.now().year
    currentMonth = datetime.now().month
    numberOfdays = monthrange(currentYear, currentMonth)[1]
    startDate = datetime(currentYear, currentMonth, 1)
    endDate = datetime(currentYear, currentMonth, numberOfdays)
    preset = ''

    if (request.method == 'POST'):
        form = ChartFilterForm(request.POST)
        if (form.is_valid()):
            oldestDate = dataService.getOldestTransaction(request.user).date
            oldestDate = datetime(oldestDate.year, oldestDate.month, oldestDate.day)

            preset = form.cleaned_data['preset']
            if (preset != ''):
                if (preset == 'ALL'):
                    startDate = oldestDate
                    endDate = dataService.getNewestTransaction(request.user).date
                    endDate = datetime(endDate.year, endDate.month, endDate.day)
                elif (preset == '1M'):
                    startDate = datetime.now() + relativedelta(months=-1)
                    endDate = datetime.now()
                elif (preset == '3M'):
                    startDate = datetime.now() + relativedelta(months=-3)
                    endDate = datetime.now()
                elif (preset == '6M'):
                    startDate = datetime.now() + relativedelta(months=-6)
                    endDate = datetime.now()
                elif (preset == '1Y'):
                    startDate = datetime.now() + relativedelta(years=-1)
                    endDate = datetime.now()
                elif (preset == 'YTD'):
                    startDate = datetime(datetime.now().year, 1, 1)
                    endDate = datetime.now()

                if (startDate < oldestDate):
                    startDate = oldestDate

            else:
                startDate = form.cleaned_data['startDate']
                endDate = form.cleaned_data['endDate']

    context = expenseTrackerBuilder.buildDashboardContext(request.user, startDate, endDate, preset)
    
    return render(request, 'tracker/dashboard.html', context)

@login_required
def presetTransactions(request):

    context = expenseTrackerBuilder.buildPresetTransactionsContext(request.user)

    return render(request, 'tracker/presetTransactions.html', context)

@login_required
def createPreset(request):
    if (request.method == 'POST'):
        form = PresetTransactionForm(request.POST)
        if (form.is_valid()):
            print(form.cleaned_data)
            context = expenseTrackerBuilder.buildCreatePresetTransactionSuccessContext(request.user, form)
            return render(request, 'tracker/createPresetSuccess.html', context)
        else:
            context = expenseTrackerBuilder.buildCreatePresetTransactionFormErrorsContext(form)
            return render(request, 'tracker/createPresetTransaction.html', context)
    else:
        prevUrl = 'presetTransactions'
        context = expenseTrackerBuilder.buildCreatePresetTransactionFormContext(prevUrl, request.user)
        return render(request, 'tracker/createPresetTransaction.html', context)

@login_required
def settings(request):
    context = expenseTrackerBuilder.buildSettingsHomeContext(request.user)

    return render(request, 'tracker/settingsHome.html', context)

@login_required
def methods(request):
    context = expenseTrackerBuilder.buildMethodsContext(request.user)

    return render(request, 'tracker/methods.html', context)

@login_required
def createMethod(request):
    if (request.method == 'POST'):
        form = MethodForm(request.POST)
        if (form.is_valid()):
            print(form.cleaned_data)
            dataService.createMethodFromForm(form, request.user)
            return redirect('methods')

@login_required
def updateMethod(request, id):
    if (request.method == 'POST'):
        form = MethodForm(request.POST)
        if (form.is_valid()):
            print(form.cleaned_data)
            dataService.updateMethodFromForm(form, request.user, id)
            return redirect('methods')

@login_required
def toggleActive(request, id):
    if (request.method == 'POST'):
        dataService.methodToggleActive(request.user, id)
        return redirect('methods')