import requests
from django.shortcuts import redirect, render
from django.views.generic import ListView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

API_BASE_URL = "http://127.0.0.1:8006/api/rewards"


class HomeView(TemplateView):
    print('indie')
    template_name = "rewards/home.html"


class AppsListView(LoginRequiredMixin, ListView):
    template_name = "rewards/app_list.html"
    context_object_name = "apps"

    def get_queryset(self):
        headers = {"Authorization": f"Bearer {self.request.session.get('token')}"}
        response = requests.get(f"{API_BASE_URL}/apps/", headers=headers)
        return response.json() if response.status_code == 200 else []


class TasksListView(LoginRequiredMixin, ListView):
    template_name = "rewards/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        headers = {"Authorization": f"Bearer {self.request.session.get('token')}"}
        print(headers, 'Headser')
        response = requests.get(f"{API_BASE_URL}/tasks/", headers=headers)
        print(response, 'Response')
        return response.json() if response.status_code == 200 else []


class TaskUploadView(LoginRequiredMixin, FormView):
    template_name = "rewards/task_upload.html"

    def post(self, request, *args, **kwargs):
        headers = {"Authorization": f"Bearer {request.session.get('token')}"}
        files = {"screenshot": request.FILES["screenshot"]}
        data = {"app": request.POST["app"]}

        response = requests.post(f"{API_BASE_URL}/tasks/upload/", headers=headers, files=files, data=data)
        if response.status_code == 201:
            return redirect("tasks_list")
        return render(request, self.template_name, {"error": response.json()})
