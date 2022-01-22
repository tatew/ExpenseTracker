import imp
from ..models import Transaction, Category, Method
from datetime import datetime
from dateutil.relativedelta import relativedelta

def getMonthlyResultsData():
    oldestDate = Transaction.objects.values('date').order_by('date').first()['date']
    months = []
    iteratorDate = datetime(oldestDate.year, oldestDate.month, 1)
    currentDate = datetime(datetime.now().year, datetime.now().month, 1)
    while (iteratorDate <= currentDate):
        months.append({'year': iteratorDate.year, 'month': iteratorDate.month})
        iteratorDate = iteratorDate + relativedelta(months=1)

    return months
