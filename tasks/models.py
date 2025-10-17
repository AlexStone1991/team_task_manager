from django.db import models
from django.conf import settings
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from users.models import User
from rest_framework import serializers

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название задачи")
    description = models.TextField(blank=True, verbose_name="Описание задачи")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Назначена пользователю")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    due_date = models.DateTimeField(verbose_name="Срок выполнения")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', verbose_name="Статус задачи"
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Дата создания")
    
    def __str__(self):
        return self.title
    
    @property
    def is_overdue(self):
        """Проверка просрочена ли задача"""
        return timezone.now() > self.due_date and self.status != 'completed'
    
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        
        super().save(*args, **kwargs)
        
        # Отправляем WebSocket уведомление
        self.send_websocket_notification(is_new)
        
        # Отправляем Telegram уведомление (если новая задача)
        if is_new:
            self.send_assignment_notification()
    
    def send_websocket_notification(self, is_new):
        """Отправка WebSocket уведомления"""
        try:
            channel_layer = get_channel_layer()
            
            task_data = {
                'id': self.id,
                'title': self.title,
                'status': self.status,
                'is_overdue': self.is_overdue,
            }
            
            if is_new:
                # Новая задача
                async_to_sync(channel_layer.group_send)(
                    f'user_{self.assigned_to.id}',
                    {
                        'type': 'task_created',
                        'task': task_data
                    }
                )
            else:
                # Обновление задачи
                async_to_sync(channel_layer.group_send)(
                    f'user_{self.assigned_to.id}',
                    {
                        'type': 'task_update', 
                        'task': task_data
                    }
                )
        except Exception as e:
            print(f"WebSocket error: {e}")
    
    def send_assignment_notification(self):
        """Отправка Telegram уведомления - СИНХРОННАЯ версия"""
        from bot.utils import send_telegram_message_sync
    
        if self.assigned_to.telegram_chat_id:
            message = f"🎯 <b>Новая задача!</b>\n\n{self.title}\n📅 До: {self.due_date.strftime('%d.%m.%Y %H:%M')}"
            send_telegram_message_sync(self.assigned_to.telegram_chat_id, message)
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']