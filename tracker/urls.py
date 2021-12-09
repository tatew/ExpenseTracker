from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    path('home/', views.home, name='home'),
    path('logExpense/', views.logExpense, name='logExpense'),
    path('list/', views.listBalanceChanges, name='list'),
    path('', views.index, name="index")
]