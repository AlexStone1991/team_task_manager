import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        if self.user.is_anonymous:
            await self.close()
            return
            
        self.room_group_name = f'user_{self.user.id}'
        
        # Присоединяемся к группе пользователя
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        print(f"WebSocket connected: {self.user.username}")

    async def disconnect(self, close_code):
        # Покидаем группу
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected: {self.user.username}")

    async def receive(self, text_data):
        # Обрабатываем сообщения от клиента
        pass

    async def task_update(self, event):
        # Отправляем обновление клиенту
        await self.send(text_data=json.dumps({
            'type': 'task_update',
            'task': event['task']
        }))

    async def task_created(self, event):
        # Отправляем уведомление о новой задаче
        await self.send(text_data=json.dumps({
            'type': 'task_created', 
            'task': event['task']
        }))

    async def task_completed(self, event):
        # Отправляем уведомление о завершении задачи
        await self.send(text_data=json.dumps({
            'type': 'task_completed',
            'task_id': event['task_id']
        }))