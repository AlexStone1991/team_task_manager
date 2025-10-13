from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'due_date', 'status', 'created_at')
    list_filter = ('status', 'assigned_to', 'due_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'assigned_to')
        }),
        ('Даты и статус', {
            'fields': ('due_date', 'status')
        }),
    )