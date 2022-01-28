from django.test import TestCase
from ..models import Transaction, Category, Method
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse

class HomeTests(TestCase):
    def setUp(self):
        self.categ = Category.objects.create(name="testCategory")
        self.method = Method.objects.create(name="testMethod")
        self.user = User.objects.create_user(username='testuser', password='12345')

    def testHomeWhenLoggedInNegativeBalance(self):
        #arrange
        Transaction.objects.create(
            date=datetime.now(),
            vendor="test",
            reason="test",
            category=self.categ,
            method=self.method,
            amount=-10.44,
            user=self.user
        )
        login = self.client.login(username='testuser', password='12345')

        #act
        response = self.client.get(reverse('home'))

        #assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['monthlyBalance'], "-10.44")

    def testHomeWhenLoggedInPositiveBalance(self):
        #arrange
        Transaction.objects.create(
            date=datetime.now(),
            vendor="test",
            reason="test",
            category=self.categ,
            method=self.method,
            amount=10.44,
            user=self.user
        )
        login = self.client.login(username='testuser', password='12345')

        #act
        response = self.client.get(reverse('home'))

        #assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['monthlyBalance'], "10.44")

    def testHomeWhenLoggedInZeroBalance(self):
        #arrange
        login = self.client.login(username='testuser', password='12345')

        #act
        response = self.client.get(reverse('home'))

        #assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['monthlyBalance'], "0.00")

    def testHomeWhenNotLoggedIn(self):
        #arrange

        #act
        response = self.client.get(reverse('home'))

        #assert
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/home/")

class LogExpenseTests(TestCase):
    def setUp(self):
        self.categ = Category.objects.create(name="testCategory")
        self.method = Method.objects.create(name="testMethod")
        self.user = User.objects.create_user(username='testuser', password='12345')

    def testLogExpenseRequestMethodGetNoPrevUrl(self):
        #arrange
        login = self.client.login(username='testuser', password='12345')

        #act
        response = self.client.get(reverse('logExpense'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial['date'].date(), datetime.now().date())
        self.assertEqual(response.context['form'].initial['prevUrl'], 'home')
        self.assertEqual(response.context['form'].action, '/logExpense/')
        self.assertEqual(response.context['form'].formId, 'expenseForm')
        self.assertEqual(response.context['form'].title, 'Log Expense')
        self.assertEqual(response.context['cancelBack'], True)
        self.assertFalse('cancelDisable' in response.context)
        self.assertFalse('delete' in response.context)
        self.assertFalse('edit' in response.context)
        self.assertEqual(response.context['submit'], True)
        
    
    def testLogExpenseWhenNotLoggedIn(self):
        #arrange

        #act
        response = self.client.get(reverse('home'))

        #assert
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/home/") 
        
