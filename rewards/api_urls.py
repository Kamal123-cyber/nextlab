from django.urls import path
from .api_views import AppListAPIView, TaskCreateAPIView, TaskListAPIView, TaskScreenshotUploadView

urlpatterns = [
    path('apps/', AppListAPIView.as_view(), name='app-list'),
    path('tasks/', TaskListAPIView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateAPIView.as_view(), name='task-create'),
    path("tasks/<uuid:uid>/upload/", TaskScreenshotUploadView.as_view(), name="task_screenshot_upload"),
]
