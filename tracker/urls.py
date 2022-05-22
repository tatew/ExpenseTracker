from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    path('home/', views.home, name='home'),
    path('chooseTransactionType/', views.chooseTransactionType, name='chooseTransactionType'),
    path('choosePresetTransaction/', views.choosePresetTransaction, name='choosePresetTransaction'),
    path('presetTransactions/new/', views.createPreset, name='createPreset'),
    path('presetTransactions/', views.presetTransactions, name='presetTransactions'),
    path('presetTransactions/<int:id>/', views.presetTransaction, name='presetTransaction'),
    path('presetTransactions/<int:id>/delete', views.deleteConfirmPresetTransaction, name='transactionPresetDeleteConfirm'),
    path('logIncome/', views.logIncome, name='logIncome'),
    path('logExpense/', views.logExpense, name='logExpense'),
    path('import/', views.importTransactions, name='import'),
    path('transactions/', views.listTransactions, name='transactions'),
    path('transactions/<int:id>', views.transaction, name='transaction'),
    path('transactions/<int:id>/delete', views.deleteConfirmTransaction, name="transactionDeleteConfirm"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),
    path('methods/', views.methods, name='methods'),
    path('methods/new/', views.createMethod, name='createMethod'),
    path('methods/<int:id>/update', views.updateMethod, name='updateMethod'),
    path('methods/<int:id>/toggleActive', views.toggleActive, name='toggleActive'),
    path('', views.index, name="index")
]