from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from products.models import Transaksi, DetailTransaksi
from django.db.models import Sum
import datetime

@login_required(login_url='/admin/login/')
def home(request):
    return redirect('/admin/')  # Langsung lempar ke Dashboard Admin setelah login

@login_required(login_url='/admin/login/')
def kasir(request):
    return render(request, 'kasir.html')  # <--- INI YANG KURANG (Menangani tampilan kasir)

@login_required(login_url='/admin/login/')
def laporan(request):
    bulan = request.GET.get('bulan', datetime.date.today().month)
    tahun = request.GET.get('tahun', datetime.date.today().year)

    transaksi = Transaksi.objects.filter(
        created_at__month=bulan,
        created_at__year=tahun
    )

    total_pendapatan = transaksi.aggregate(Sum('total_harga'))['total_harga__sum'] or 0
    total_hpp = transaksi.aggregate(Sum('total_hpp'))['total_hpp__sum'] or 0
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