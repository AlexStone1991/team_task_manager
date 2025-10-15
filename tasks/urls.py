from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, task_list, api_my_tasks, api_complete_task, quick_create_task, api_wrapper

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('api-drf/', include(router.urls)),
    path('my-tasks/', task_list, name='my_tasks'),
    path('api/my-tasks/', api_my_tasks, name='api_my_tasks'),
    path('api/complete-task/<int:task_id>/', api_complete_task, name='api_complete_task'),
    path('quick-create/', quick_create_task, name='quick_create'),
    path('api/', api_wrapper, name='api_wrapper'),
]
