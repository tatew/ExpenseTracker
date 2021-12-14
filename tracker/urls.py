from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    path('home/', views.home, name='home'),
    path('balanceChangeType/', views.chooseBalanceChangeType, name='chooseBalanceChangeType'),
    path('logIncome/', views.logIncome, name='logIncome'),
    path('logExpense/', views.logExpense, name='logExpense'),
    path('list/', views.listBalanceChanges, name='list'),
    path('import/', views.importBalanceChanges, name='import'),
    path('', views.index, name="index")
]