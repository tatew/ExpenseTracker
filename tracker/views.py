from django.forms.utils import pretty_name
from django.http.response import FileResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import BalanceChange, Category, Method
from .forms import ExpenseForm

def index(request):
    return render(request, "tracker/index.html")

@login_required
def home(request):
    return render(request, "tracker/home.html")

@login_required
def logExpense(request):
    if (request.method == "POST"):
        print(request.POST)
        # create a form instance and populate it with data from the request:
        form = ExpenseForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print(form.cleaned_data)
            expense = BalanceChange(
                date=form.cleaned_data['date'],
                reason=form.cleaned_data['reason'],
                vendor=form.cleaned_data['vendor'],
                method=Method.objects.first(id=form.cleaned_data['method']),
                category=Category.objects.first(id=form.cleaned_data['category']),
                amount=form.cleaned_data['amount'] * -1
            )
            expense.save()
            return redirect('/home')
        else:
            print("not valid")
            return redirect('/home')
    else:
        categories = Category.objects.order_by("name")
        methods = Method.objects.order_by("name")

        context = {
            'categories': categories,
            'methods': methods
        }
        
        return render(request, "tracker/logExpense.html", context)
