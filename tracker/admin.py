from django.contrib import admin

from tracker.models import BalanceChange, Category, Method

# Register your models here.
admin.site.register(BalanceChange)
admin.site.register(Category)
admin.site.register(Method)