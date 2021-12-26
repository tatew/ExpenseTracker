from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    path('home/', views.home, name='home'),
    path('chooseTransactionType/', views.chooseTransactionType, name='chooseTransactionType'),
    path('logIncome/', views.logIncome, name='logIncome'),
    path('logExpense/', views.logExpense, name='logExpense'),
    path('list/', views.listTransactions, name='list'),
    path('import/', views.importTransactions, name='import'),
    path('transactions/<int:id>', views.transaction, name='transaction'),
    path('transactions/<int:id>/delete', views.deleteConfirm, name="transactionDeleteConfirm"),
    path('', views.index, name="index")
]