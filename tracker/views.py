from django.forms.utils import pretty_name
from django.http.response import FileResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import BalanceChange, Category, Method
from .forms import ExpenseForm, ImportForm
from .services import importBalanceChangeCsv
from django.template.defaulttags import register
import csv
import io
...
@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)

def index(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        return render(request, "tracker/index.html")

@login_required
def home(request):
    return render(request, "tracker/home.html")

@login_required
def logExpense(request):
    if (request.method == "POST"):
        # create a form instance and populate it with data from the request:
        form = ExpenseForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            expense = BalanceChange(
                date=form.cleaned_data['date'],
                reason=form.cleaned_data['reason'],
                vendor=form.cleaned_data['vendor'],
                method=form.cleaned_data['method'],
                category=form.cleaned_data['category'],
                amount=form.cleaned_data['amount'] * -1,
                user=request.user
            )
            expense.save()
            return redirect('/home')
        else:
            return render(request, "tracker/logExpense.html", {'form': form})
    else:
        prevUrl = request.GET.get('prevUrl', 'home')
        form = ExpenseForm(initial={'prevUrl': prevUrl})
        
        return render(request, "tracker/logExpense.html", {'form': form})

@login_required
def listBalanceChanges(request):
    
    context = {
        'balanceChanges': BalanceChange.objects.filter(user_id=request.user.id)
    }

    return render(request, "tracker/listBalanceChanges.html", context)

@login_required
def importBalanceChanges(request):
    if (request.method == "POST"):
        form = ImportForm(request.POST, request.FILES)
        print(form.data)
        print(form.errors)

        if form.is_valid():
            print('valid')
            #process form 
            try:
                print('trying')
                decoded_file = request.FILES['csvFile'].read().decode('utf-8')
            except UnicodeDecodeError as e:
                print('except')
                form.add_error('csvFile', 'Error decoding the file, use .csv files only')
                return render(request, 'tracker/import.html', {'form': form})
            print('starting read')
            io_string = io.StringIO(decoded_file)
            csvReader = csv.reader(io_string, delimiter=',')
            results = importBalanceChangeCsv(csvReader, request)
            print('success')
            return render(request, 'tracker/importResults.html', {'results': results})
        else:
            print('invalid')
            return render(request, 'tracker/import.html', {'form': form})
    else:
        print('GET')
        prevUrl = request.GET.get('prevUrl', 'home')
        form = ImportForm(initial={'prevUrl': prevUrl})
        return render(request, 'tracker/import.html', {'form': form})
