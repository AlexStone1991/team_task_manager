# 🚀 Team Task Manager
Проект Алексей Лапшин

Полнофункциональная система управления задачами с real-time уведомлениями и Telegram ботом.

## 🛠 Стек технологий:
- **Backend**: Django 4.2 + Django REST Framework
- **Real-time**: Django Channels + WebSockets  
- **Frontend**: Pure JavaScript
- **Telegram**: Aiogram 3.x
- **Database**: SQLite
- **Package manager**: Poetry

## 🎯 Функциональность:
- 📋 Управление задачами через веб-интерфейс
- 🔗 REST API для интеграций
- 🤖 Telegram бот с уведомлениями  
- ⚡ Real-time обновления через WebSockets
- 🔐 Аутентификация и авторизация

## 🚀 Запуск:
```bash
# Установка
poetry install

# Миграции
poetry run python manage.py migrate

# Запуск
poetry run python manage.py runserver
poetry run python manage.py start_bot