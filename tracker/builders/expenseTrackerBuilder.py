from tracker.models import Method
from ..services import dataService
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from ..forms import TransactionForm, PresetTransactionForm, ChartFilterForm, MethodForm
from ..utilities import expenseTrackerUtilities
import decimal

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

def buildLogExpenseFormContext(prevUrl, preset, user):
    if (preset == None):
        form = TransactionForm(initial={'prevUrl': prevUrl, 'date': datetime.now(), 'user': user})
    else:
        form = TransactionForm(initial={
            'prevUrl': prevUrl,
            'date': datetime.now(),
            'vendor': preset.vendor,
            'reason': preset.reason,
            'method': preset.method,
            'category': preset.category,
            'amount': preset.amount,
            'user': user
        })

    form.formId = 'expenseForm'
    form.action = '/logExpense/'
    form.title = 'Log Expense'

    context = {
        'form': form,
        'submit': True,
        'cancelBack': True
    }
    return context

def buildLogIncomeSuccessContext(user, form):
    income = dataService.createIncomeFromForm(form, user)
    context = {
        'income': income
    }
    return context

def buildLogIncomeErrorsContext(user, form):
    context = {
        'form': form,
        'submit': True,
        'cancelBack': True
    }
    
    return context

def buildLogIncomeFormContext(prevUrl, preset, user):
    if (preset == None):
        form = TransactionForm(initial={'prevUrl': prevUrl, 'date': datetime.now(), 'user': user})
    else:
        form = TransactionForm(initial={
            'prevUrl': prevUrl,
            'date': datetime.now(),
            'vendor': preset.vendor,
            'reason': preset.reason,
            'method': preset.method,
            'category': preset.category,
            'amount': preset.amount,
            'user': user
        })

    form.formId = 'incomeForm'
    form.action = '/logIncome/'
    form.title = 'Log Income'

    context = {
        'form': form,
        'submit': True,
        'cancelBack': True
    }
    return context 



def buildDashboardContext(user, startDate, endDate, preset):
        
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
        'activePreset': preset
    }

    return context


def buildChartData(user, startDate, endDate):

    netByDate = dataService.getNetByDate(user, startDate, endDate)
    netByDate = expenseTrackerUtilities.fillOutTransactions(netByDate, startDate, endDate)
    netByDate = expenseTrackerUtilities.convertToRunningTotal(netByDate)

    incomesByDate = dataService.getIncomeTotalsByDate(user, startDate, endDate)
    expensesByDate = dataService.getExpenseTotalsByDate(user, startDate, endDate)

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

    oldestTransactionDate = dataService.getOldestTransaction(user).date
    oldestTransactionDateMonthAndYear = datetime(oldestTransactionDate.year, oldestTransactionDate.month, 1)

    monthlyDataList = []
    totalExpenses = 0
    totalIncomes = 0
    currentDate = datetime(datetime.now().year, datetime.now().month, 1)
    endDate = oldestTransactionDateMonthAndYear

    while (currentDate >= endDate):
        totalForMonth = getTotalsForMonth(user, currentDate.year, currentDate.month)
        totalForMonth['year'] = currentDate.year
        totalForMonth['month'] = datetime.strptime(str(currentDate.month), "%m").strftime("%B")
        monthlyDataList.append(totalForMonth)

        totalExpenses += totalForMonth['numericSumOfExpensesForMonth']
        totalIncomes += totalForMonth['numericSumOfImcomesForMonth']

        currentDate += relativedelta(months=-1)

    avgExpense = totalExpenses / len(monthlyDataList)
    avgExpense = avgExpense.quantize(decimal.Decimal("0.01"))
    avgExpenseString = f"{avgExpense:,}"
    avgExpenseString = f"${avgExpenseString:>12}"

    avgIncome = totalIncomes / len(monthlyDataList)
    avgIncome = avgIncome.quantize(decimal.Decimal("0.01"))
    avgIncomeString = f"{avgIncome:,}"
    avgIncomeString = f"${avgIncomeString:>12}"

    avgNet = (totalIncomes + totalExpenses) / len(monthlyDataList)
    avgNet = avgNet.quantize(decimal.Decimal("0.01"))
    avgNetString = f"{avgNet:,}"
    avgNetString = f"${avgNetString:>12}"

    monthlyData = {
        'monthlyDataList': monthlyDataList,
        'avgExpense': avgExpenseString,
        'avgIncome': avgIncomeString,
        'avgNet': avgNetString
    }

    return monthlyData

def getTotalsForMonth(user, year, month):
    sumOfIncomesForMonth = expenseTrackerUtilities.sumTransactions(dataService.getIncomesForMonth(user, year, month))
    incomesString = f"{sumOfIncomesForMonth:,}"
    incomesString = f"${incomesString:>12}"
    sumOfExpensesForMonth = expenseTrackerUtilities.sumTransactions(dataService.getExpensesForMonth(user, year, month))
    expnesesString = f"{sumOfExpensesForMonth:,}"
    expnesesString = f"${expnesesString:>12}"
    netBalanceForMonth = sumOfIncomesForMonth + sumOfExpensesForMonth
    netBalanceString = f"{netBalanceForMonth:,}"
    netBalanceString = f"${netBalanceString:>12}"

    totalsForMonth = {
        'sumOfExpensesForMonth': expnesesString,
        'sumOfImcomesForMonth': incomesString,
        'netBalanceForMonth': netBalanceString,
        'numericSumOfExpensesForMonth': sumOfExpensesForMonth,
        'numericSumOfImcomesForMonth': sumOfIncomesForMonth
    }

    return totalsForMonth

def buildPresetTransactionsContext(user):
    presets = dataService.getTransactionPresetsForUser(user);

    context = {
        'presets': presets
    }

    return context

def buildCreatePresetTransactionFormContext(prevUrl, user):
    form = PresetTransactionForm(initial={'prevUrl': prevUrl, 'isExpense': True, 'user': user})

    context = {
        'form': form,
        'submit': True,
        'cancelBack': True
    }

    return context

def buildCreatePresetTransactionFormErrorsContext(form):
    context = {
        'form': form,
        'submit': True,
        'cancelBack': True
    }

    return context

def buildCreatePresetTransactionSuccessContext(user, form):
    preset = dataService.createPresetTransactionFromForm(form, user)
    context = {
        'preset': preset
    }

    return context

def buildSettingsHomeContext(user):
    return {}

def buildMethodsContext(user):
    methods = dataService.getMethodsForUser(user)

    context = {
        'methods': methods,
        'user': user.username
    }
    
    return context

def buildListTransactionsContext(user, numToShow, transactionFilter):
    hideShowMore = False

    if (transactionFilter == None):
        transactions = dataService.getLastNTransactions(user, numToShow + 1)
    else:
        transactions = dataService.getTransactionsForFilter(user, transactionFilter)

    hideShowMore = (transactions.count() < numToShow + 1)
    transactions = transactions[:numToShow]

    for transaction in transactions:
        transaction.dateStr = date.strftime(transaction.date, "%m/%d/%Y")
        amountStr = f"{transaction.amount:,}"
        transaction.amountStr = f"${amountStr:>12}"

    categories = dataService.getCategories()
    methods = dataService.getMethodsForUser(user)

    context = {
        'transactions': transactions,
        'hideShowMore': hideShowMore,
        'nextNumToShow': numToShow + 10,
        'methods': methods,
        'categories': categories,
        'transactionFilter': transactionFilter
    }

    return context