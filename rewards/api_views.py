from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import App, Task
from .serializers import AppSerializer, TaskSerializer, TaskCreateSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404


class AppListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]  # Anyone can view apps

    def get(self, request):
        apps = App.objects.all()
        serializer = AppSerializer(apps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TaskCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Task submitted successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=self.request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TaskScreenshotUploadView(APIView):
    authentication_classes = [JWTAuthentication]  # Secure API with JWT
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Handle File Uploads

    def post(self, request, uid, *args, **kwargs):
        task = get_object_or_404(Task, uid=uid, user=request.user)

        if "screenshot" in request.FILES:
            task.screenshot = request.FILES["screenshot"]
            task.status = "approved"
            task.points_earned = task.app.points
            task.is_completed = True
            task.save()
            return Response(
                {"message": "Screenshot uploaded successfully!", "screenshot_url": task.screenshot.url},
                status=status.HTTP_200_OK
            )

        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)