from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth.views import LoginView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.models import User
from .models import Transaction, Category, Account
from .forms import TransactionForm, TransactionFilterForm, SignUpForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib import messages
from django.core.exceptions import ValidationError





def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('username')
        password = request.POST.get('pass')
        confirm_password = request.POST.get('confirm-pass')
        email = request.POST.get('mail')
        confirm_email = request.POST.get('confirm-mail')
        last_name = request.POST.get('surname')

        if password != confirm_password:
            error_message = 'Passwords do not match.'
            return render(request, 'base.html', {'error_message': error_message})

        if email != confirm_email:
            error_message = 'Emails do not match.'
            return render(request, 'base.html', {'error_message': error_message})

        # Проверка уникальности имени пользователя и адреса электронной почты
        if User.objects.filter(username=email).exists():
            error_message = 'Email is already registered.'
            return render(request, 'base.html', {'error_message': error_message})

        if User.objects.filter(email=email).exists():
            error_message = 'Email is already registered.'
            return render(request, 'base.html', {'error_message': error_message})

        # Создание пользователя
        user = User.objects.create_user(username=email, first_name=first_name, password=password, email=email, last_name=last_name)

        # Аутентификация пользователя и редирект или отображение ошибки
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Failed to authenticate user.'
            return render(request, 'base.html', {'error_message': error_message})

    return render(request, 'signup.html')




def transactions_view(request):
    # Обработка GET-запроса
    if request.method == 'GET':
        form = TransactionFilterForm(request.GET)
        if form.is_valid():
            # Получаем данные из формы
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            transaction_type = form.cleaned_data['transaction_type']
            category = form.cleaned_data['category']

            # Получаем список транзакций с заданными параметрами
            transactions = Transaction.objects.filter(date__range=(start_date, end_date))
            if transaction_type:
                transactions = transactions.filter(type=transaction_type)
            if category:
                transactions = transactions.filter(category=category)

            # Вычисляем баланс на начало и конец заданного периода
            balance_start = Transaction.objects.filter(date__lt=start_date).aggregate(models.Sum('amount'))['amount__sum'] or 0
            balance_end = Transaction.objects.filter(date__lte=end_date).aggregate(models.Sum('amount'))['amount__sum'] or 0

            # Передаем данные в шаблон и рендерим страницу
            return render(request, 'transactions.html', {
                'form': form,
                'transactions': transactions,
                'balance_start': balance_start,
                'balance_end': balance_end,
            })

    # Если это не GET-запрос, создаем пустую форму
    else:
        form = TransactionFilterForm()

    # Рендерим страницу с пустой формой
    return render(request, 'transactions.html', {'form': form})

def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user_id = request.user.id  # добавляем user_id
            # Изменяем знак суммы транзакции, если тип "OUT"
            if transaction.transaction_type == 'OUT':
                transaction.amount *= -1
            transaction.save()
            return redirect('home')
    else:
        form = TransactionForm()
    return render(request, 'create_transaction.html', {'form': form})

def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    old_amount = transaction.amount  # Получаем предыдущую сумму
    old_transaction_type = transaction.transaction_type
    print("old_amount", old_amount)
    account = Account.objects.get(user=request.user)
    print("account.balance before", account.balance)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            #old_amount = transaction.amount  # Получаем предыдущую сумму
            #print("old_amount", old_amount)
            new_transaction = form.save(commit=False)
            if new_transaction.transaction_type != old_transaction_type:
                new_transaction.amount *= -1
            new_amount = new_transaction.amount  # Получаем новую сумму
            print("new_amount", new_amount)
            # Вычисляем разницу между предыдущей и новой суммой
            difference = new_amount - old_amount
            print("difference", difference)
            new_transaction.difference = difference  # Сохраняем значение difference в поле модели
            # Обновляем баланс аккаунта
            account = Account.objects.get(user=request.user)
            print("account.balance before", account.balance)
            account.balance += difference
            print("account.balance", account.balance)
            #account.save()
            new_transaction.save()
            return redirect('home')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'edit_transaction.html', {'form': form, 'transaction': transaction})


def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    old_amount = transaction.amount  # Получаем предыдущую сумму
    old_transaction_type = transaction.transaction_type
    print("old_amount", old_amount)
    account = Account.objects.get(user=request.user)
    print("account.balance before", account.balance)
    difference = - old_amount
    print("difference", difference)
    # Обновляем баланс аккаунта
    account = Account.objects.get(user=request.user)
    print("account.balance before", account.balance)
    account.balance += difference
    print("account.balance", account.balance)
    transaction.delete()
    return redirect('home')

def filter_transactions(request):

    if request.GET:
        form = TransactionFilterForm(request.GET)
    #else:
        #form = TransactionFilterForm()
        #print("Ошибки нет:")


        transactions = Transaction.objects.all()

        if form.is_valid():
        # Получение параметров фильтра из формы
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            transaction_type = form.cleaned_data['transaction_type']
            category = form.cleaned_data['category']

        # Фильтрация транзакций
            if request.user.is_authenticated:
                transactions = Transaction.objects.filter(account__user=request.user.id)
            else:
                transactions = Transaction.objects.none()

            if start_date:
                transactions = transactions.filter(date__gte=start_date)
            if end_date:
                transactions = transactions.filter(date__lte=end_date)
            if transaction_type:
                transactions = transactions.filter(transaction_type=transaction_type)
            if category:
                transactions = transactions.filter(category_id=category)

        # Вычисление суммы отфильтрованных транзакций
            filtered_transactions_sum = transactions.aggregate(Sum('amount'))['amount__sum']

        # Отображение отфильтрованных транзакций и их суммы в шаблоне filter_transactions.html
            return render(request, 'home.html', { 'transactions': transactions, 'filtered_transactions_sum': filtered_transactions_sum})
        # Возвращаем пустой HttpResponse в случае, если форма не является валидной
        else:
            # Форма не валидна
            errors = form.errors.as_data()
            print("errors:", errors)
            for field, field_errors in errors.items():
                for error in field_errors:
                    print(f"Ошибка в поле {field}: {error}")
            return HttpResponse()
    else:
        form = TransactionFilterForm()
        print("Ошибки нет:")
        return render(request, 'filter_transactions.html', {'form': form})#, 'transactions': transactions})

class MyLoginView(LoginView):
    template_name = 'login.html'  # шаблон страницы авторизации
    redirect_authenticated_user = True  # если пользователь уже авторизован, перенаправляем его на главную страницу
    success_url = reverse_lazy('home')  # перенаправление после успешной авторизации

    def form_invalid(self, form):
        messages.error(self.request, 'Неправильний логін або пароль.')
        return super().form_invalid(form)

    def get_success_url(self):
        return self.success_url

def logout_view(request):
    logout(request)
    return redirect('base')

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'

class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

def base(request):
    context = {
    }
    return render(request, 'base.html', context)

@login_required
def home(request):
    start_date = date.min
    end_date = datetime.now()

    # Проверяем, существует ли объект Account для данного пользователя
    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        # Если объект Account не существует, создаем его
        account = Account.objects.create(user=request.user)

    transactions = Transaction.objects.filter(
        user=request.user, date__range=[start_date, end_date]
    )

    total_balance = account.get_total_balance()


    context = {
        'transactions': transactions,
        'start_date': start_date,
        'end_date': end_date,
        'categories': Category.objects.all(),
        'total_balance': total_balance,
        'account': account,
    }

    return render(request, 'home.html', context=context)
