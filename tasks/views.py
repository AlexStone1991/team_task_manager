from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer
from django.contrib.auth.decorators import login_required



class TaskViewSet(viewsets.ModelViewSet):
    """API для управления задачами"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Показываем только задачи текущего пользователя
        return Task.objects.filter(assigned_to=self.request.user)

def landing(request):
    """Главная страница с красивым шаблоном"""
    return render(request, 'tasks/landing.html')

@login_required
def task_list(request):
    """Страница со списком задач для текущего пользователя"""
    return render(request, 'tasks/task_list.html')

@login_required
def api_my_tasks(request):
    """API для получения задач текущего пользователя"""
    tasks = Task.objects.filter(assigned_to=request.user).order_by('-created_at')
    
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.strftime('%d.%m.%Y %H:%M'),
            'status': task.status,
            'is_overdue': task.is_overdue,
            'created_at': task.created_at.strftime('%d.%m.%Y %H:%M'),
        })
    
    return JsonResponse({'tasks': tasks_data})

@login_required
def api_complete_task(request, task_id):
    """API для отметки задачи как выполненной"""
    try:
        task = Task.objects.get(id=task_id, assigned_to=request.user)
        task.status = 'completed'
        task.save()
        return JsonResponse({'success': True})
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Задача не найдена'}, status=404)