from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('kasir/', kasir, name='kasir'),
    path('laporan/', laporan, name='laporan'),
]