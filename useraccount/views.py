import requests
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

  # Ensures the name exists

# API_BASE_URL = "https://ktechs.in/api"

class RegisterView(TemplateView):
    template_name = "useraccount/register.html"

    def post(self, request, *args, **kwargs):
        data = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
        }
        try:
            response = requests.post(
                "https://ktechs.in/api/auth/signup/",
                json=data,  # This sends JSON data
                headers={"Content-Type": "application/json"},  # Ensure proper headers
            )
            if response.status_code == 201:
                return redirect(reverse("login"))
            try:
                error_response = response.json()
            except requests.exceptions.JSONDecodeError:
                error_response = {"error": "Invalid response from server."}

            return render(request, self.template_name, {"error": error_response})
        except requests.RequestException as e:
            return render(request, self.template_name, {"error": "Failed to connect to server."})

class LoginView(TemplateView):
    template_name = "useraccount/login.html"
    def post(self, request, *args, **kwargs):
        data = {
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
        }
        response = requests.post(
            "https://ktechs.in/api/auth/login/",
            json=data,  # This sends JSON data
            headers={"Content-Type": "application/json"},  # Ensure proper headers
        )
        if response.status_code == 200:
            response_data = response.json()
            request.session["token"] = response_data.get("access")
            # return redirect(reverse("profile"))

            return redirect(reverse("tasks_list"))
        return render(request, self.template_name, {"error": response.json()})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "useraccount/profile.html"

    def get(self, request, *args, **kwargs):
        # headers = {"Authorization": f"Bearer {request.session.get('token')}"}
        headers = {
            "Authorization": f"Bearer {request.session.get('token')}",
            "Content-Type": "application/json",
        }
        response = requests.get(
            "https://ktechs.in/api/auth/profile/",  # Ensure data is sent as JSON
            headers=headers,
        )

        if response.status_code == 200:
            user_data = response.json()
            return render(request, self.template_name, {"user": user_data})
        return redirect("login")
