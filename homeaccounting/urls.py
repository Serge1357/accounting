"""homeaccounting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, SignUpView
from finance.views import MyLoginView, base, home, create_transaction,signup, logout_view, edit_transaction, delete_transaction, filter_transactions
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
   # path('register/', SignUpView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('', base, name='base'),
    path('home/', home, name='home'),
    path('create_transaction/', create_transaction, name='create_transaction'),
    path('filter_transactions/', filter_transactions, name='filter_transactions'),
    path('transactions/<int:pk>/edit/', edit_transaction, name='edit_transaction'),
    path('delete/<int:pk>/', delete_transaction, name='delete_transaction'),
    path('signup/', signup, name='signup'),
]





