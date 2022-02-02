from django.test import TestCase
from ..models import Transaction, Category, Method
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from calendar import monthrange

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
        self.assertTemplateUsed(response, 'tracker/home.html')
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
        self.assertTemplateUsed(response, 'tracker/home.html')
        self.assertEqual(response.context['monthlyBalance'], "10.44")

    def testHomeWhenLoggedInZeroBalance(self):
        #arrange
        login = self.client.login(username='testuser', password='12345')

        #act
        response = self.client.get(reverse('home'))

        #assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/home.html')
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

        #assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/fullPageForm.html')
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
        
    def testLogExpenseRequestMethodGetHasPrevUrl(self):
        #arrange
        login = self.client.login(username='testuser', password='12345')

        #act
        response = self.client.get('/logExpense/', {'prevUrl': 'chooseTransactionType'})

        #assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/fullPageForm.html')
        self.assertEqual(response.context['form'].initial['date'].date(), datetime.now().date())
        self.assertEqual(response.context['form'].initial['prevUrl'], 'chooseTransactionType')
        self.assertEqual(response.context['form'].action, '/logExpense/')
        self.assertEqual(response.context['form'].formId, 'expenseForm')
        self.assertEqual(response.context['form'].title, 'Log Expense')
        self.assertEqual(response.context['cancelBack'], True)
        self.assertFalse('cancelDisable' in response.context)
        self.assertFalse('delete' in response.context)
        self.assertFalse('edit' in response.context)
        self.assertEqual(response.context['submit'], True)

    def testLogExpenseRequestMethodPostValidForm(self):
        #arrange
        login = self.client.login(username='testuser', password='12345')
        form = {
            'date': "2022-01-28",
            'vendor': 'test',
            'reason': 'test',
            'category': self.categ.id,
            'method': self.method.id,
            'amount': 10.44,
        }

        #act
        response = self.client.post(reverse('logExpense'), form)

        #assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/logExpenseSuccess.html')
        self.assertEqual(response.context['expense'].date, datetime(2022, 1, 28).date())
        self.assertEqual(response.context['expense'].vendor, 'test')
        self.assertEqual(response.context['expense'].reason, 'test')
        self.assertEqual(response.context['expense'].category, self.categ)
        self.assertEqual(response.context['expense'].method, self.method)
        self.assertAlmostEqual(response.context['expense'].amount, Decimal(-10.44))
        self.assertEqual(response.context['expense'].user, self.user)

    def testLogExpenseRequestMethodPostNotValidForm(self):
        #arrange
        login = self.client.login(username='testuser', password='12345')
        form = {
            'date': "",
            'vendor': 'test',
            'reason': 'test',
            'category': self.categ.id,
            'method': self.method.id,
            'amount': 10.44,
        }

        #act
        response = self.client.post(reverse('logExpense'), form)

        #assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/fullPageForm.html')
        self.assertEqual(response.context['form'].errors['date'][0], 'This field is required.')
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

class DashboardTests(TestCase):
    #incomplete
    def setUp(self):
        self.categ1 = Category.objects.create(name="testCategory1")
        self.categ2 = Category.objects.create(name="testCategory2")
        self.categIncome = Category.objects.create(name="Income")
        self.method1 = Method.objects.create(name="testMethod1")
        self.method2 = Method.objects.create(name="testMethod2")
        self.method3 = Method.objects.create(name="testMethod3")
        self.user = User.objects.create_user(username='testuser', password='12345')
        Transaction.objects.create(
            date=datetime(datetime.now().year, datetime.now().month, 1),
            vendor='test',
            reason='expense',
            category=self.categ1,
            method=self.method1,
            amount=-10.44,
            user=self.user
        )
        Transaction.objects.create(
            date=datetime(datetime.now().year, datetime.now().month, 1),
            vendor='test',
            reason='expense',
            category=self.categ2,
            method=self.method2,
            amount=-8.44,
            user=self.user
        )
        Transaction.objects.create(
            date=datetime(datetime.now().year, datetime.now().month, 4),
            vendor='test',
            reason='expense',
            category=self.categ2,
            method=self.method2,
            amount=-7.44,
            user=self.user
        )
        Transaction.objects.create(
            date=datetime(datetime.now().year, datetime.now().month, 4),
            vendor='test',
            reason='income',
            category=self.categIncome,
            method=self.method3,
            amount=12.44,
            user=self.user
        )
        Transaction.objects.create(
            date=datetime(datetime.now().year, datetime.now().month, 10),
            vendor='test',
            reason='income',
            category=self.categIncome,
            method=self.method3,
            amount=13.44,
            user=self.user
        )
        

    def testDashboardLoggedInGet(self):
        #arrange
        login = self.client.login(username='testuser', password='12345')
        numberOfdays = monthrange(datetime.now().year, datetime.now().month)[1]

        #act
        response = self.client.get(reverse('dashboard'))

        #assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/dashboard.html')
        self.assertEqual(response.context['currentMonth'], datetime.strptime(str(datetime.now().month), "%m").strftime("%B"))
        self.assertEqual(response.context['currentYear'], datetime.now().year)
        #form asserts
        self.assertEqual(response.context['form'].initial['startDate'].date(), datetime(datetime.now().year, datetime.now().month, 1).date())
        self.assertEqual(response.context['form'].initial['endDate'].date(), datetime(datetime.now().year, datetime.now().month, numberOfdays).date())
        self.assertEqual(response.context['form'].action, '/dashboard/')
        self.assertEqual(response.context['form'].formId, 'chartFilterForm')
        self.assertEqual(response.context['form'].title, 'Filter Chart')
        self.assertFalse('cancelBack' in response.context)
        self.assertFalse('cancelDisable' in response.context)
        self.assertFalse('delete' in response.context)
        self.assertFalse('edit' in response.context)
        self.assertEqual(response.context['submit'], True)
        #chart data asserts
        self.assertEqual(len(response.context['chartData']['incomesByDate']), numberOfdays)
        self.assertEqual(len(response.context['chartData']['expensesByDate']), numberOfdays)
        self.assertAlmostEqual(response.context['chartData']['expensesByDate'][0]['total'], Decimal(-18.88))
        self.assertEqual(len(response.context['chartData']['netByDate']), numberOfdays)
        self.assertAlmostEqual(response.context['chartData']['netByDate'][0]['total'], Decimal(-18.88))
        self.assertAlmostEqual(response.context['chartData']['netByDate'][3]['total'], Decimal(-13.88))
        self.assertAlmostEqual(response.context['chartData']['netByDate'][10]['total'], Decimal(-0.44))
        self.assertEqual(len(response.context['chartData']['categoryData']), 2)
        #monthly data asserts

    def testDashboardNotLoggedIn(self):
        #arrange

        #act
        response = self.client.get(reverse('dashboard'))

        #assert
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/dashboard/") 
        
