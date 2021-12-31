from .models import Transaction
from datetime import datetime, timedelta, date

def fillOutNetTransactions(netTransactions, startDate, endDate):

    currentDate = startDate
    resultNetTransactions = []
    while (currentDate <= endDate):
        try: 
            netTransactionForDate = netTransactions.get(date=currentDate)
            resultNetTransactions.append(netTransactionForDate)
        except:
            fillerNetTransaction = {
                'date': date(currentDate.year, currentDate.month, currentDate.day),
                'total': 0
            }
            resultNetTransactions.append(fillerNetTransaction)
        currentDate = currentDate + timedelta(days=1)

    return resultNetTransactions

def convertToRunningTotal(netTransactions):
    prevNetTransaction = 0
    for netTransaction in netTransactions:
        netTransaction['total'] = netTransaction['total'] + prevNetTransaction
        prevNetTransaction = netTransaction['total']

    return netTransactions