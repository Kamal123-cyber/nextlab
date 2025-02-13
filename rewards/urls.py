from django.urls import path
from .views import AppsListView, TasksListView, TaskUploadView, HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("apps/", AppsListView.as_view(), name="apps_list"),
    path("tasks/", TasksListView.as_view(), name="tasks_list"),
    path("tasks/upload/", TaskUploadView.as_view(), name="task_upload"),
]
