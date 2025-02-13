from django.urls import path
from .api_views import RegisterAPIView, LoginAPIView, UserProfileAPIView

urlpatterns = [
    path('signup/', RegisterAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
]
