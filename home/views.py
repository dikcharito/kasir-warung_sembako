from django.shortcuts import render
from products.models import Transaksi, DetailTransaksi
from django.db.models import Sum
import datetime

def home(request):
    return render(request, 'home.html')

def kasir(request):
    return render(request, 'kasir.html')

def laporan(request):
    # Filter by bulan/tahun kalau ada
    bulan = request.GET.get('bulan', datetime.date.today().month)
    tahun = request.GET.get('tahun', datetime.date.today().year)

    # Ambil semua transaksi bulan ini
    transaksi = Transaksi.objects.filter(
        created_at__month=bulan,
        created_at__year=tahun
    )

    # Hitung total
    total_pendapatan = transaksi.aggregate(
        Sum('total_harga'))['total_harga__sum'] or 0
    total_hpp = transaksi.aggregate(
        Sum('total_hpp'))['total_hpp__sum'] or 0
    total_laba = total_pendapatan - total_hpp
    total_transaksi = transaksi.count()

    return render(request, 'laporan.html', {
        'transaksi': transaksi,
        'total_pendapatan': total_pendapatan,
        'total_hpp': total_hpp,
        'total_laba': total_laba,
        'total_transaksi': total_transaksi,
        'bulan': bulan,
        'tahun': tahun,
    })