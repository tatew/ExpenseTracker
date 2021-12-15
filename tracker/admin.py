from django.contrib import admin

from tracker.models import Transaction, Category, Method

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(Method)