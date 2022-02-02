import datetime
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category, Method
from .forms import TransactionForm, ImportForm, ChartFilterForm
from .services.importService import importTransactionsCsv
import csv
import io
from django.db.models import Sum
from calendar import monthrange
from .utilities import expenseTrackerUtilities
from .services import dataService
from .builders import expenseTrackerBuilder

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
        prevUrl = request.GET.get('prevUrl', 'home')
        context = expenseTrackerBuilder.buildLogExpenseFormContext(prevUrl)
        return render(request, "tracker/fullPageForm.html", context)

@login_required
def logIncome(request):
    if (request.method == "POST"):
        # create a form instance and populate it with data from the request:
        form = TransactionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            income = Transaction(
                date=form.cleaned_data['date'],
                reason=form.cleaned_data['reason'],
                vendor=form.cleaned_data['vendor'],
                method=form.cleaned_data['method'],
                category=form.cleaned_data['category'],
                amount=form.cleaned_data['amount'],
                user=request.user
            )
            income.save()
            return render(request, 'tracker/logIncomeSuccess.html', {'income': income})
        else:
            context = {
                'form': form,
                'submit': True,
                'cancelBack': True
            }

            return render(request, "tracker/fullPageForm.html", context)
    else:
        prevUrl = request.GET.get('prevUrl', 'home')
        form = TransactionForm(initial={'prevUrl': prevUrl, 'date': datetime.datetime.now()})
        form.formId = 'incomeForm'
        form.action = '/logIncome/'
        form.title = 'Log Income'

        context = {
            'form': form,
            'submit': True,
            'cancelBack': True
        }
        
        return render(request, "tracker/fullPageForm.html", context)

@login_required
def listTransactions(request):
    numToShow = 10
    if (request.method == "POST"):
        numToShow = int(request.POST['prevNumToShow']) + 10

    transactions = dataService.getLastNTransactions(request.user, numToShow + 1)
    
    hideShowMore = False
    if (transactions.count() < numToShow + 2):
        hideShowMore = True

    transactions = transactions[:numToShow]

    for transaction in transactions:
        transaction.dateStr = datetime.date.strftime(transaction.date, "%m/%d/%Y")
        amountStr = f"{transaction.amount:,}"
        transaction.amountStr = f"${amountStr:>12}"

    context = {
        'transactions': transactions,
        'hideShowMore': hideShowMore,
        'prevNumToShow': numToShow
    }

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
    currentYear = datetime.datetime.now().year
    currentMonth = datetime.datetime.now().month
    numberOfdays = monthrange(currentYear, currentMonth)[1]
    startDate = datetime.datetime(currentYear, currentMonth, 1)
    endDate = datetime.datetime(currentYear, currentMonth, numberOfdays)

    if (request.method == 'POST'):
        form = ChartFilterForm(request.POST)
        if (form.is_valid()):
            if (bool(form.cleaned_data['allData'])):
                startDate = dataService.getOldestTransaction(request.user).date
                endDate = dataService.getNewestTransaction(request.user).date
                print(startDate, endDate)
            else:
                startDate = form.cleaned_data['startDate']
                endDate = form.cleaned_data['endDate']

    context = expenseTrackerBuilder.buildDashboardContext(request.user, startDate, endDate)
    
    return render(request, 'tracker/dashboard.html', context)
