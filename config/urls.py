from django.contrib import admin
from django.urls import path, include
from tasks.views import landing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='home'),
    path('', include('tasks.urls')),  # Добавляем API URLs
]