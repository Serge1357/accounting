from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Transaction, Account

@receiver(post_save, sender=Transaction)
def update_account_balance(sender, instance, **kwargs):
    # Получаем связанный с транзакцией аккаунт пользователя
    account = instance.account
    # Получаем текущий баланс пользователя
    balance = account.balance
    print("баланс до", balance)
    difference = instance.difference  # Получаем значение difference из поля модели
    print("difference", difference)
    if difference == None:
        balance += instance.amount
    else:
        balance += difference
    print("instance.amount", instance.amount)
    print("баланс после", balance)
    # Сохраняем новое значение баланса в БД
    Account.objects.filter(pk=account.pk).update(balance=balance)


@receiver(post_delete, sender=Transaction)
def update_account_balance_on_delete(sender, instance, **kwargs):
    account = instance.account
    balance = account.balance
    difference = -instance.amount  # Вычисляем разницу для удаленной транзакции
    balance += difference
    account.balance = balance
    account.save()