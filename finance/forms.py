from django import forms
from .models import Transaction, Category
from django.forms.widgets import SelectDateWidget, Select
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import F

class CustomSelectWidget(Select):
    def optgroups(self, name, value, attrs=None):
        groups = super().optgroups(name, value, attrs)

        for group in groups:
            group_name, group_html, group_values = group

            print(f"Group name: {group_name}")
            print(f"Group HTML: {group_html}")
            print(f"Group values: {group_values}")

        return groups


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class TransactionForm(forms.ModelForm):
    #transaction_type = forms.ChoiceField(choices=Transaction.TRANSACTION_TYPES, label='Тип транзакції')

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount', 'description', 'category']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Определите, какой тип транзакции выбран
    #     transaction_type = self.initial.get('transaction_type') or self.data.get('transaction_type')
    #     if transaction_type == 'IN':
    #         # Если выбран тип "Income", используйте список категорий для доходов
    #         self.fields['category'].choices = Category.CATEGORIES_INCOME
    #     else:
    #         # Иначе используйте список категорий для расходов
    #         self.fields['category'].choices = Category.CATEGORIES
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     categories = Category.objects.all()
    #     category_choices = []
    #
    #     for category in categories:
    #         if category.expense_category:
    #             for key, value in Category.CATEGORIES:
    #                 if key == category.name:
    #                     category_choices.append((category.id, value))
    #         elif category.income_category:
    #             for key, value in Category.CATEGORIES_INCOME:
    #                 if key == category.name:
    #                     category_choices.append((category.id, value))
    #
    #     self.fields['category'].choices = category_choices

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        transaction_type = self.initial.get('transaction_type') or self.data.get('transaction_type')
        category_choices = []
        if transaction_type == 'IN':
            # Если выбран тип "Income", используйте список категорий для доходов
            categories = Category.objects.filter(income_category=True)
            categories_model = Category.CATEGORIES_INCOME
        else:
            # Иначе используйте список категорий для расходов
            categories = Category.objects.filter(expense_category=True)
            categories_model = Category.CATEGORIES
        for category in categories:
            for key, value in categories_model:
                if key == category.name:
                    category_choices.append((category.id, value))
        print("transaction_type:", transaction_type)
        print("category_choices:", category_choices)
        self.fields['category'].choices = category_choices


class TransactionFilterForm(forms.Form):
    TRANSACTION_TYPES = [
        ('', 'All'),  # Пустое значение для выбора всех типов
        ('IN', 'Income'),
        ('OUT', 'Expense'),
    ]

    transaction_type = forms.ChoiceField(
        choices=TRANSACTION_TYPES,
        required=False,
        label='Transaction type'
    )

    start_date = forms.DateField(
        label='Start date',
        widget=forms.SelectDateWidget(),
        required=False
    )

    end_date = forms.DateField(
        label='End date',
        widget=forms.SelectDateWidget(),
        required=False
    )

    category = forms.ChoiceField(
        choices=[],
        required=False,
        label='Category'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = self.get_category_choices()

    def get_category_choices(self):
        transaction_type = self.initial.get('transaction_type') or self.data.get('transaction_type')
        if transaction_type == 'IN':
            category_choices = Category.objects.filter(income_category=True).values_list('id', 'name')
        else:
            category_choices = Category.objects.filter(expense_category=True).values_list('id', 'name')
        choices = [('', 'All')] + list(category_choices)
        return choices







