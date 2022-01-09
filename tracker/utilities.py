from .models import Transaction
from datetime import datetime, timedelta, date

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