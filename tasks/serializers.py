from rest_framework import serializers
from .models import Task
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to', 
            'assigned_to_username', 'created_by', 'created_by_username',
            'status', 'due_date', 'created_at','is_overdue'
        ]
        read_only_fields = ['created_by', 'created_at']