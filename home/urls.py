from django.urls import path
from .views import *

urlpatterns = [
    path('', views.kasir, name='kasir'),
    path('laporan/', views.laporan, name='laporan'),
]