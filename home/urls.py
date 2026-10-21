from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kasir/', views.kasir, name='kasir'),
    path('laporan/', views.laporan, name='laporan'),
]