from django import forms
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class QuickTaskForm(forms.ModelForm):
    """Упрощенная форма для быстрого создания задач"""
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем только активных пользователей
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)