from django.contrib import admin
from .models import Category, Transaction, Account, User

# Register your models here.
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Account)
admin.site.register(User)