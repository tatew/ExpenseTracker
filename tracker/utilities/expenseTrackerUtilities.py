from ..models import Category, Method
from datetime import datetime, timedelta, date
from django.db.models import Sum

def fillOutTransactions(transactions, startDate, endDate):

    currentDate = startDate
    resultTransactions = []
    while (currentDate <= endDate):
        try: 
            transactionForDate = transactions.get(date=currentDate)
            resultTransactions.append(transactionForDate)
        except:
            fillerNetTransaction = {
                'date': date(currentDate.year, currentDate.month, currentDate.day),
                'total': 0
            }
            resultTransactions.append(fillerNetTransaction)
        currentDate = currentDate + timedelta(days=1)

    return resultTransactions

def convertToRunningTotal(transactions):
    prevTransaction = 0
    for transaction in transactions:
        transaction['total'] = transaction['total'] + prevTransaction
        prevTransaction = transaction['total']

    return transactions

def sumTransactions(transactions):
    return transactions.aggregate(Sum('amount'))['amount__sum']

def lookupMethod(methodStr):
    try:
        existingMethod = Method.objects.get(name=methodStr)
    except:
        firstLetter = methodStr[0].upper()
        methodStr = methodStr[1:]
        methodStr = firstLetter + methodStr
        method = Method(name=methodStr)
        method.save()
        return method
    return existingMethod


def lookupCategory(categoryStr):
    try:
        existingCategory = Category.objects.get(name=categoryStr)
    except:
        firstLetter = categoryStr[0].upper()
        categoryStr = categoryStr[1:]
        categoryStr = firstLetter + categoryStr
        category = Category(name=categoryStr)
        category.save()
        return category
    return existingCategory