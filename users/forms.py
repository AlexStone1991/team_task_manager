from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=20, 
        required=True,
        help_text='Формат: +79991234567'
    )
    telegram_username = forms.CharField(
        max_length=100,
        required=False,
        help_text='Ваш username в Telegram (без @)'
    )

    class Meta:
        model = User
        fields = ('username', 'phone', 'telegram_username', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)