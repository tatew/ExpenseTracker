from calendar import month
from ..services import dataService
from datetime import datetime
from ..forms import TransactionForm, ImportForm, ChartFilterForm
from ..utilities import expenseTrackerUtilities

# Always pass user or other things from request as first argument

def buildHomeContext(user):
    transactionsForMonth = dataService.getTransactionsForMonth(user, datetime.now().year, datetime.now().month)
    sumOfTransactions = expenseTrackerUtilities.sumTransactions(transactionsForMonth)
    if (sumOfTransactions == None):
        sumOfTransactions = 0
    
    context = {
        'monthlyBalance': "{:,.2f}".format(sumOfTransactions)
    }

    return context
    
def buildLogExpenseSuccessContext(user, form):
    expense = dataService.createExpenseFromForm(form, user)
    context = {
        'expense': expense
    }
    return context

def buildLogExpenseFormErrorsContext(form):
    context = {
        'form': form,
        'submit': True,
        'cancelBack': True
    }

    return context

def buildLogExpenseFormContext(prevUrl):
    form = TransactionForm(initial={'prevUrl': prevUrl, 'date': datetime.now()})
    form.formId = 'expenseForm'
    form.action = '/logExpense/'
    form.title = 'Log Expense'

    context = {
        'form': form,
        'submit': True,
        'cancelBack': True
    }
    return context

def buildDashboardContext(user, startDate, endDate):
        
    form = ChartFilterForm(initial={'startDate': startDate, 'endDate': endDate})

    chartData = buildChartData(user, startDate, endDate)
    monthlyData = buildMonthlyData(user)

    context = {
        'chartData': chartData,
        'monthlyData': monthlyData,
        'form': form,
        'submit': True,
        'currentMonth': datetime.strptime(str(datetime.now().month), "%m").strftime("%B"),
        'currentYear': datetime.now().year,
    }

    return context


def buildChartData(user, startDate, endDate):

    netByDate = dataService.getNetByDate(user, startDate, endDate)
    netByDate = expenseTrackerUtilities.fillOutTransactions(netByDate, startDate, endDate)
    netByDate = expenseTrackerUtilities.convertToRunningTotal(netByDate)

    incomesByDate = dataService.getIncomesByDate(user, startDate, endDate)
    expensesByDate = dataService.getExpensesByDate(user, startDate, endDate)

    incomesByDate = expenseTrackerUtilities.fillOutTransactions(incomesByDate, startDate, endDate)
    expensesByDate = expenseTrackerUtilities.fillOutTransactions(expensesByDate, startDate, endDate)

    categories = dataService.getCategories()
    categoryData = []
    for category in categories:
        if (str(category) != 'Income'):
            totalForCategory = dataService.getNetTransactionsForCategoryInDateRange(user, category, startDate, endDate)
            if (totalForCategory != None):
                totalForCategory = abs(totalForCategory)
            else: 
                totalForCategory = 0
            categoryData.append({
                'name': str(category),
                'total': totalForCategory
            })

    chartData = {
        'incomesByDate': list(incomesByDate),
        'expensesByDate': list(expensesByDate),
        'netByDate': list(netByDate),
        'categoryData': categoryData
    }

    return chartData

def buildMonthlyData(user):

    monthlyData = dataService.getTotalsForMonth(user, datetime.now().year, datetime.now().month)

    return monthlyData
