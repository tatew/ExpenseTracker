from django.test import TestCase
from ..models import Transaction, Category, Method, TransactionPreset
from datetime import datetime
from django.contrib.auth.models import User
from ..services import dataService
from freezegun import freeze_time
from decimal import Decimal
from ..forms import TransactionForm, PresetTransactionForm

class TestDataService(TestCase):

    def setUp(self):
        self.categ1 = Category.objects.create(name="testCategory1")
        self.categ2 = Category.objects.create(name="testCategory2")
        self.method1 = Method.objects.create(name="testMethod1")
        self.user1 = User.objects.create_user(username='user1', password='12345')
        self.user2 = User.objects.create_user(username='user2', password='12345')

    @freeze_time("2022-02-1")
    def test_GetMonthsFromFirstMonthWithData_ForUser1(self):
        #arrange
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user1
        )

        Transaction.objects.create(
            date=datetime(2021, 4, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user2
        )

        #act
        result = dataService.getMonthsFromFirstMonthWithData(self.user1)

        #assert
        self.assertEqual(len(result), 8)
        self.assertEqual(result[0]['month'], 7)
        self.assertEqual(result[len(result) -1 ]['month'], 2)
        self.assertEqual(result[0]['year'], 2021)
        self.assertEqual(result[len(result) -1 ]['year'], 2022)

    @freeze_time("2022-02-1")
    def test_GetMonthsFromFirstMonthWithData_ForUser2(self):
        #arrange
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user1
        )

        Transaction.objects.create(
            date=datetime(2021, 4, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user2
        )

        #act
        result = dataService.getMonthsFromFirstMonthWithData(self.user2)

        #assert
        self.assertEqual(len(result), 11)
        self.assertEqual(result[0]['month'], 4)
        self.assertEqual(result[len(result) -1 ]['month'], 2)
        self.assertEqual(result[0]['year'], 2021)
        self.assertEqual(result[len(result) -1 ]['year'], 2022)

    def test_getTransactionsForMonth(self):
        #arrange
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 4, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2020, 7, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user1
        )
        #act
        result = dataService.getTransactionsForMonth(self.user1, 2021, 7)
        #assert
        self.assertEqual(len(result), 2)

    def test_GetExpensesForMonth(self):
        #arrange
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 4, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2020, 7, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user1
        )

        Transaction.objects.create(
            date=datetime(2020, 7, 1),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=10.44,
            user=self.user1
        )
        #act
        result = dataService.getExpensesForMonth(self.user1, 2021, 7)
        #assert
        self.assertEqual(len(result), 2)

    def test_GetIncomesForMonth(self):
        #arrange
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=10.44,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 4, 1),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=10.44,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=10.44,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2020, 7, 1),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=10.44,
            user=self.user1
        )

        Transaction.objects.create(
            date=datetime(2020, 7, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user1
        )
        #act
        result = dataService.getIncomesForMonth(self.user1, 2021, 7)
        #assert
        self.assertEqual(len(result), 2)

    def test_getTransactionsForDateRange(self):
        #arrange
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=10.44,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 2),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=10.44,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=10.44,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=10.44,
            user=self.user1
        )

        Transaction.objects.create(
            date=datetime(2021, 7, 5),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user1
        )
        #act
        startDate = datetime(2021, 7, 2)
        endDate = datetime(2021, 7, 4)
        result = dataService.getTransactionsForDateRange(self.user1, startDate, endDate)
        #assert
        self.assertEqual(len(result), 3)

    def test_getLastNTransactions(self):
        #arrange
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=10.44,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=10.44,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=10.44,
            user=self.user1
        )

        Transaction.objects.create(
            date=datetime(2021, 7, 5),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user1
        )
        #act
        result = dataService.getLastNTransactions(self.user1, 4)
        #assert
        self.assertEqual(len(result), 4)
        self.assertAlmostEqual(result[3].amount, Decimal(10.44))

    def test_getTransactionById(self):
        #arrange
        transaction = Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=10.44,
            user=self.user1
        )
        #act
        result = dataService.getTransactionById(transaction.id)
        #assert
        self.assertEqual(result, transaction)

    def test_getIncomeTotalsByDate(self):
        #arrange
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=1,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 2),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=2,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=3,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-3,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=41,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=42,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 5),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=5,
            user=self.user1
        )
        #act
        startDate = datetime(2021, 7, 2)
        endDate = datetime(2021, 7, 4)
        result = dataService.getIncomeTotalsByDate(self.user1, startDate, endDate)
        #assert
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[0]['total'], Decimal(2))
        self.assertAlmostEqual(result[1]['total'], Decimal(3))
        self.assertAlmostEqual(result[2]['total'], Decimal(83))

    def test_getExpenseTotalsByDate(self):
        #arrange
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-1,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 2),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-2,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-3,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=3,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-41,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-42,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 5),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-5,
            user=self.user1
        )
        #act
        startDate = datetime(2021, 7, 2)
        endDate = datetime(2021, 7, 4)
        result = dataService.getExpenseTotalsByDate(self.user1, startDate, endDate)
        #assert
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[0]['total'], Decimal(-2))
        self.assertAlmostEqual(result[1]['total'], Decimal(-3))
        self.assertAlmostEqual(result[2]['total'], Decimal(-83))

    def test_getNetByDate(self):
        #arrange
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-1,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 2),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-2,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-3,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=3,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-41,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=42,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 5),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-5,
            user=self.user1
        )
        #act
        startDate = datetime(2021, 7, 2)
        endDate = datetime(2021, 7, 4)
        result = dataService.getNetByDate(self.user1, startDate, endDate)
        #assert
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[0]['total'], Decimal(-2))
        self.assertAlmostEqual(result[1]['total'], Decimal(0))
        self.assertAlmostEqual(result[2]['total'], Decimal(1))

    def test_getTransactionsForCategoryInDateRange(self):
        #arrange
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-1,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 2),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-2,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-3,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='differentCateg',
            category=self.categ2,
            method=self.method1,
            amount=3,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-41,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=42,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 5),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-5,
            user=self.user1
        )
        #act
        startDate = datetime(2021, 7, 2)
        endDate = datetime(2021, 7, 4)
        result = dataService.getTransactionsForCategoryInDateRange(self.user1, self.categ1, startDate, endDate)
        #assert
        self.assertEqual(len(result), 4)

    def test_getNetTransactionsForCategoryInDateRange(self):
        #arrange
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-1,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 2),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-2,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-3,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='differentCateg',
            category=self.categ2,
            method=self.method1,
            amount=3,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-41,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=42,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 5),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-5,
            user=self.user1
        )
        #act
        startDate = datetime(2021, 7, 2)
        endDate = datetime(2021, 7, 4)
        result = dataService.getNetTransactionsForCategoryInDateRange(self.user1, self.categ1, startDate, endDate)
        #assert
        self.assertAlmostEqual(result, Decimal(-4))

    def test_getCategories(self):
        #arrange

        #act
        result = dataService.getCategories()

        #assert
        self.assertEqual(len(result), 2)

    def test_createExpenseFromForm(self):
        #arrange
        form = TransactionForm(data={
            'date': "2022-01-28",
            'vendor': 'test',
            'reason': 'test',
            'category': self.categ1.id,
            'method': self.method1.id,
            'amount': 10.44,
            'user': self.user1
        })

        form.is_valid()

        #act
        result = dataService.createExpenseFromForm(form, self.user1)

        #assert
        self.assertEqual(len(Transaction.objects.all()), 1)
        self.assertAlmostEqual(Transaction.objects.all()[0].amount, Decimal(-10.44))

    def test_createIncomeFromForm(self):
        #arrange
        form = TransactionForm(data={
            'date': "2022-01-28",
            'vendor': 'test',
            'reason': 'test',
            'category': self.categ1.id,
            'method': self.method1.id,
            'amount': 10.44,
            'user': self.user1
        })

        form.is_valid()

        #act
        result = dataService.createIncomeFromForm(form, self.user1)

        #assert
        self.assertEqual(len(Transaction.objects.all()), 1)
        self.assertAlmostEqual(Transaction.objects.all()[0].amount, Decimal(10.44))

    def test_createPresetTransactionFromForm(self):
        #arrange
        form = PresetTransactionForm(data={
            'name': 'test',
            'isExpense': True,
            'vendor': 'test',
            'reason': 'test',
            'category': self.categ1.id,
            'method': self.method1.id,
            'amount': 10.44,
            'user': self.user1
        })

        form.is_valid()

        #act
        result = dataService.createPresetTransactionFromForm(form, self.user1)

        #assert
        self.assertEqual(len(TransactionPreset.objects.all()), 1)
        self.assertAlmostEqual(TransactionPreset.objects.all()[0].amount, Decimal(10.44))
        self.assertEqual(TransactionPreset.objects.all()[0].isExpense, True)

    def test_getOldestTransaction(self):
        #arrange
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-1,
            user=self.user2
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 2),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-2,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-3,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='differentCateg',
            category=self.categ2,
            method=self.method1,
            amount=3,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-41,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=42,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 5),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-5,
            user=self.user1
        )
        #act
        result = dataService.getOldestTransaction(self.user1)
        #assert
        self.assertEqual(result.date.year, 2021)
        self.assertEqual(result.date.month, 7)
        self.assertEqual(result.date.day, 2)

    def test_getNewestTransaction(self):
        #arrange
        Transaction.objects.create(
            date=datetime(2021, 7, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-1,
            user=self.user2
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 2),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-2,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-3,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 3),
            vendor='test',
            reason='differentCateg',
            category=self.categ2,
            method=self.method1,
            amount=3,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-41,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 4),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=42,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 5),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-5,
            user=self.user1
        )
        Transaction.objects.create(
            date=datetime(2021, 7, 6),
            vendor='test',
            reason='income',
            category=self.categ1,
            method=self.method1,
            amount=42,
            user=self.user2
        )
        #act
        result = dataService.getNewestTransaction(self.user1)
        #assert
        self.assertEqual(result.date.year, 2021)
        self.assertEqual(result.date.month, 7)
        self.assertEqual(result.date.day, 5)

    def testGetTransactionPresetsForUser(self):
        #arrange
        TransactionPreset.objects.create(
            name="atest",
            user=self.user1,
            isExpense=True
        )
        TransactionPreset.objects.create(
            name="btest",
            user=self.user1,
            isExpense=True
        )
        TransactionPreset.objects.create(
            name="test",
            user=self.user2,
            isExpense=True
        )
        #act
        result = dataService.getTransactionPresetsForUser(self.user1)
        #assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "atest")

    def testGetTransactionPresetById(self):
        #arrange
        txn = TransactionPreset.objects.create(
            name="atest",
            user=self.user1,
            isExpense=True
        )
        TransactionPreset.objects.create(
            name="btest",
            user=self.user1,
            isExpense=True
        )
        TransactionPreset.objects.create(
            name="test",
            user=self.user2,
            isExpense=True
        )
        #act
        result = dataService.getTransactionPresetById(txn.id)
        #assert
        self.assertEqual(result.name, "atest")
