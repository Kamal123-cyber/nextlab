import requests
from django.shortcuts import redirect, render
from django.views.generic import ListView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# API_BASE_URL = "https://ktechs.in/api/rewards"


class HomeView(TemplateView):
    print('indie')
    template_name = "rewards/home.html"


class AppsListView(LoginRequiredMixin, ListView):
    template_name = "rewards/app_list.html"
    context_object_name = "apps"

    def get_queryset(self):
        headers = {
            "Authorization": f"Bearer {self.request.session.get('token')}",
            "Content-Type": "application/json",
        }
        response = requests.get("https://ktechs.in/api/rewards/apps/", headers=headers)
        return response.json() if response.status_code == 200 else []


class TasksListView(LoginRequiredMixin, ListView):
    template_name = "rewards/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        # headers = {"Authorization": f"Bearer {self.request.session.get('token')}"}
        headers = {
            "Authorization": f"Bearer {self.request.session.get('token')}",
            "Content-Type": "application/json",
        }
        print(self.request.session.get('token'))
        response = requests.get("https://ktechs.in/api/rewards/apps/", headers=headers)
        print(response, 'Response')
        return response.json() if response.status_code == 200 else []


class TaskUploadView(LoginRequiredMixin, FormView):
    template_name = "rewards/task_upload.html"

    def post(self, request, *args, **kwargs):
        headers = {"Authorization": f"Bearer {request.session.get('token')}"}
        files = {"screenshot": request.FILES["screenshot"]}
        data = {"app": request.POST["app"]}

        response = requests.post(f"https://ktechs.in/api/tasks/upload/", headers=headers, files=files, data=data)
        if response.status_code == 201:
            return redirect("tasks_list")
        return render(request, self.template_name, {"error": response.json()})
