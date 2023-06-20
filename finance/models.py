from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone
from datetime import date
from django.contrib.auth import get_user_model


class Category(models.Model):
    CATEGORIES = (
        ('ED', 'Еда'),
        ('HR', 'Хозяйственные расходы'),
        ('CU', 'Коммунальные услуги'),
        ('OO', 'Одежда/обувь'),
        ('RV', 'Развлечения'),
        ('BT', 'Бытовая техника'),
        ('TR', 'Путешествия'),
        ('OT', 'Другое'),
    )
    CATEGORIES_INCOME = (
        ('SAL', 'Зарплата'),
        ('INV', 'Инвестиции'),
        ('GIF', 'Подарки'),
        ('OTH', 'Другое'),
    )

    name = models.CharField(max_length=255)
    expense_category = models.BooleanField(default=True)
    income_category = models.BooleanField(default=False)


    def get_transactions(self):
        return self.transaction_set.all()

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} - {self.balance}"

    def get_current_balance(self):
        start_date = date.min  # начало периода - минимальная дата
        end_date = date.today()  # конец периода - сегодняшняя дата
        return self.get_total_balance(start_date, end_date)

    def get_total_balance(self):
        transactions = Transaction.objects.filter(account=self)
        total_income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum']
        print("total_income", total_income)
        total_expense = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum']
        print("total_expense", total_expense)
        total_income = total_income if total_income is not None else 0
        total_expense = total_expense if total_expense is not None else 0
        total_balance = total_income - total_expense
        return total_balance



class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('IN', 'Дохід'),
        ('OUT', 'Витрати'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField(default=timezone.now)
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    difference = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.user} {self.transaction_type} {self.amount} ({self.category}) [{self.date.strftime('%d.%m.%Y')}]"

    def save(self, *args, **kwargs):
        # попытка автоматического определения категории
        #print(f"Selected category: {self.category}")
        #self.category = self._get_category()

        # если категория не определена, запрашиваем ее у пользователя
        #if self.category is None:
            #self.category = self._ask_for_category()

        # если пользователь не выбрал категорию, то используем категорию "Другое"
        #if self.category is None:
            #self.category = Category.objects.get(name='Другое')

        if not self.account:
            user = self.user
            try:
                account = Account.objects.get(user=user)
            except Account.DoesNotExist:
                account = Account.objects.create(user=user)
            self.account = account
        super().save(*args, **kwargs)


    def _get_category(self):
        # определение категории на основе правил
        # например, если описание транзакции содержит "еда", то относим ее к категории "Еда"
        if 'еда' in self.description.lower():
            return Category.objects.get(name='Еда')
        # если не удалось определить категорию, то возвращаем None
        return None
"""
    def input_select(message, choices):
        
        Выводит сообщение и предоставляет пользователю выбрать опцию из списка.
        Возвращает идентификатор выбранной опции.

        :param message: Сообщение для вывода пользователю.
        :param choices: Список вариантов. Каждый элемент должен быть кортежем (id, name).
        :return: Идентификатор выбранной опции.
        
        while True:
            print(message)
            for choice in choices:
                print('  {}. {}'.format(choice[0], choice[1]))

            choice_id = input('Введите номер выбранной категории: ')
            try:
                choice_id = int(choice_id)
                if choice_id in [choice[0] for choice in choices]:
                    return choice_id
            except ValueError:
                pass

            print('Некорректный выбор. Попробуйте снова.')


    def _ask_for_category(self):
        # запрашиваем у пользователя категорию для транзакции
        categories = Category.objects.all()
        category_choices = [(category.id, category.name) for category in categories]
        category_choices.append(('other', 'Другое'))
        message = 'Выберите категорию для транзакции "{}":\n'.format(self.description)
        category_id = input_select(message, category_choices)

        if category_id is None:
            return Category.objects.get(name='Другое')
        if category_id == 'other':
            category_name = input_text('Введите название категории: ')
            return Category.objects.create(name=category_name)
        else:
            return Category.objects.get(id=category_id)
"""





class User(models.Model):

    def get_income(self, start_date, end_date):
        # Получаем сумму всех входящих транзакций за указанный период
        income = self.transactions.filter(
            transaction_type='IN', date__range=[start_date, end_date]
        ).aggregate(Sum('amount'))['amount__sum']
        return Decimal(income) if income is not None else Decimal('0.00')

    def get_expenses(self, start_date, end_date):
        # Получаем сумму всех исходящих транзакций за указанный период
        expenses = self.transactions.filter(
            transaction_type='OUT', date__range=[start_date, end_date]
        ).aggregate(Sum('amount'))['amount__sum']
        return Decimal(expenses) if expenses is not None else Decimal('0.00')

    def get_balance(self):
        # Получаем текущий баланс пользователя
        account = Account.objects.get(user=self)
        return account.balance


    def get_expenses_by_category(self, start_date, end_date):
        expenses_by_category = self.transactions.filter(
            transaction_type='OUT', date__range=[start_date, end_date]
        ).values('category__name').annotate(Sum('amount'))

        # Преобразуем результат в список кортежей (категория, сумма)
        return [(item['category__name'], item['amount__sum']) for item in expenses_by_category]

    def get_transactions_by_date_range(self, start_date, end_date):
        return self.transactions.filter(date__range=[start_date, end_date])
