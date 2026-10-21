from django.urls import path
from . import views  # <--- INI YANG TADI KETINGGALAN DAN BIKIN CRASH!

urlpatterns = [
    path('', views.kasir, name='kasir'),
    path('laporan/', views.laporan, name='laporan'),
]