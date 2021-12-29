import datetime
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category, Method
from .forms import TransactionForm, ImportForm
from .services import importTransactionsCsv
import csv
import io
from django.db.models import Sum
from django.conf import settings

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
    print(type(settings.DEBUG))
    print(settings.DEBUG)
    transactionsForThisMonth = Transaction.objects.filter(date__month=datetime.datetime.now().month, user=request.user)
    
    sumOfTransactions = transactionsForThisMonth.aggregate(Sum('amount'))['amount__sum']
    if (sumOfTransactions == None):
        sumOfTransactions = 0
    


    context = {
        'monthlyBalance': "{:,.2f}".format(sumOfTransactions)
    }
    return render(request, "tracker/home.html", context)

@login_required
def chooseTransactionType(request):
    return render(request, 'tracker/chooseTransactionType.html')

@login_required
def logExpense(request):
    if (request.method == "POST"):
        # create a form instance and populate it with data from the request:
        form = TransactionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            expense = Transaction(
                date=form.cleaned_data['date'],
                reason=form.cleaned_data['reason'],
                vendor=form.cleaned_data['vendor'],
                method=form.cleaned_data['method'],
                category=form.cleaned_data['category'],
                amount=form.cleaned_data['amount'] * -1,
                user=request.user
            )
            expense.save()
            return render(request, 'tracker/logExpenseSuccess.html', {'expense': expense})
        else:
            context = {
                'form': form,
                'submit': True,
                'cancelBack': True
            }

            return render(request, "tracker/fullPageForm.html", context)
    else:
        prevUrl = request.GET.get('prevUrl', 'home')
        form = TransactionForm(initial={'prevUrl': prevUrl})
        form.formId = 'expenseForm'
        form.action = '/logExpense/'
        form.title = 'Log Expense'

        context = {
            'form': form,
            'submit': True,
            'cancelBack': True
        }
        
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
        form = TransactionForm(initial={'prevUrl': prevUrl})
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
        print(request.POST)
        numToShow = int(request.POST['prevNumToShow']) + 10

    print(numToShow)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-amount')[:numToShow + 1]
    
    hideShowMore = False
    if (transactions.count() < numToShow + 1):
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
            return render(request, 'tracker/import.html', {'form': form})
    else:
        prevUrl = request.GET.get('prevUrl', 'home')
        form = ImportForm(initial={'prevUrl': prevUrl})
        return render(request, 'tracker/import.html', {'form': form})

@login_required
def transaction(request, id):
    transaction = Transaction.objects.get(id=id)
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
    transaction = Transaction.objects.get(id=id)
    isExpense = transaction.amount < 0
    if (request.method == "POST"):
        transaction.delete()
        return redirect('/transactions')
    else:
        context = {
            'transaction': transaction
        }
        return render(request, 'tracker/deleteConfirm.html', context)
