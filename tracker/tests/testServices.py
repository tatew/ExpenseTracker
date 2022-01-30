from multiprocessing.dummy import freeze_support
from django.test import TestCase
from ..models import Transaction, Category, Method
from datetime import datetime
from django.contrib.auth.models import User
from ..services import dataService
from freezegun import freeze_time
from decimal import Decimal

class TestDataService(TestCase):

    def setUp(self):
        self.categ1 = Category.objects.create(name="testCategory1")
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
