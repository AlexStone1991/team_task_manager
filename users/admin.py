from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'telegram_username', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'telegram_username')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Telegram', {'fields': ('telegram_chat_id', 'telegram_username')}),
    )