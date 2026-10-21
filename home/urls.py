from django.urls import path
from .views import *

urlpatterns = [   
    path('kasir/', kasir, name='kasir'),
    path('laporan/', laporan, name='laporan'),
]