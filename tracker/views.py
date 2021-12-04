from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "tracker/index.html")

@login_required
def home(request):
    return render(request, "tracker/home.html")
