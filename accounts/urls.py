from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from .views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('register/', RegisterView.as_view()),
]