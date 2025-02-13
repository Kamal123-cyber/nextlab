from rest_framework import serializers
from .models import App, Task
from django.contrib.auth import get_user_model

User = get_user_model()

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'name', 'points', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    app_name = serializers.ReadOnlyField(source="app.name")
    username = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'uid', 'app_name', 'username', 'screenshot', 'points_earned', 'is_completed']

    def get_username(self, obj):
        return obj.user.username

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['app', 'screenshot']
