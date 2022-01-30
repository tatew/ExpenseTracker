from multiprocessing.dummy import freeze_support
from django.test import TestCase
from ..models import Transaction, Category, Method
from datetime import datetime
from django.contrib.auth.models import User
from ..services import dataService
from freezegun import freeze_time

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

