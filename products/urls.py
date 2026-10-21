from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductView.as_view()),
    path('transaksi/', TransaksiView.as_view()),  # API proses transaksi
    path('pelanggan/', PelangganView.as_view()),  # API daftar pelanggan
    path('bayar-hutang/', BayarHutangView.as_view()),
]