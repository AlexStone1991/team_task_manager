from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """модель пользователя"""
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)
    telegram_username = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.username