from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import datetime
from .models import *
from .serializers import *

class ProductView(APIView):
    def get(self, request):
        category = request.query_params.get('category')
        if category:
            queryset = Product.objects.filter(
                category__category_name=category)
        else:
            queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response({
            'count': len(list(serializer.data)),
            'data': serializer.data
        })

class TransaksiView(APIView):
    def post(self, request):
        data = request.data
        # Ambil data dari request
        items = data.get('items', [])          # List item yang dibeli
        metode_bayar = data.get('metode_bayar', 'tunai')  # Metode bayar
        uang_bayar = data.get('uang_bayar', 0) # Uang yang dibayarkan
        pelanggan_id = data.get('pelanggan_id', None)  # ID pelanggan (opsional)

        # Validasi: items tidak boleh kosong
        if not items:
            return Response(
                {'error': 'Keranjang kosong!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate nomor nota otomatis
        # Format: TRX-YYYYMMDD-XXX (contoh: TRX-20260613-001)
        today = datetime.date.today().strftime('%Y%m%d')
        # Hitung transaksi hari ini untuk urutan nomor
        transaksi_hari_ini = Transaksi.objects.filter(
            created_at__date=timezone.now().date()
        ).count()
        # Urutan 3 digit, mulai dari 001
        urutan = str(transaksi_hari_ini + 1).zfill(3)
        nomor_nota = f'TRX-{today}-{urutan}'

        # Hitung total harga dan total HPP
        total_harga = 0
        total_hpp = 0

        # Validasi stok semua item sebelum proses
        for item in items:
            produk = Product.objects.get(id=item['id'])
            if produk.stock < item['qty']:
                return Response(
                    {'error': f'Stok {produk.product_name} tidak cukup! Sisa: {produk.stock}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Proses transaksi
        # Ambil pelanggan jika ada
        pelanggan = None
        if pelanggan_id:
            try:
                pelanggan = Pelanggan.objects.get(id=pelanggan_id)
            except Pelanggan.DoesNotExist:
                pass

        # Hitung total dulu
        for item in items:
            produk = Product.objects.get(id=item['id'])
            subtotal = int(produk.price) * item['qty']
            hpp_item = float(produk.hpp) * item['qty']
            total_harga += subtotal
            total_hpp += hpp_item

        # Hitung kembalian
        kembalian = int(uang_bayar) - total_harga if metode_bayar == 'tunai' else 0

        # Buat objek Transaksi
        transaksi = Transaksi.objects.create(
            nomor_nota=nomor_nota,
            pelanggan=pelanggan,
            total_harga=total_harga,
            total_hpp=total_hpp,
            uang_bayar=uang_bayar if metode_bayar == 'tunai' else 0,
            kembalian=kembalian,
            metode_bayar=metode_bayar
        )

        # Buat DetailTransaksi dan potong stok per item
        for item in items:
            produk = Product.objects.get(id=item['id'])
            subtotal = int(produk.price) * item['qty']

            # Simpan detail transaksi
            DetailTransaksi.objects.create(
                transaksi=transaksi,
                produk=produk,
                jumlah=item['qty'],
                harga_jual=produk.price,
                hpp_saat_transaksi=produk.hpp,
                subtotal=subtotal
            )

            # Potong stok otomatis
            produk.stock -= item['qty']
            produk.save()

        # Jika metode hutang, tambahkan ke total hutang pelanggan
        if metode_bayar == 'hutang' and pelanggan:
            pelanggan.total_hutang += total_harga
            pelanggan.save()

        return Response({
            'success': True,
            'nomor_nota': nomor_nota,
            'total_harga': total_harga,
            'kembalian': kembalian,
            'message': 'Transaksi berhasil!'
        })

class PelangganView(APIView):
    def get(self, request):
        # Ambil semua pelanggan
        pelanggan = Pelanggan.objects.all()
        data = [{'id': p.id, 'nama': p.nama, 'total_hutang': float(p.total_hutang)} for p in pelanggan]
        return Response(data)

    def post(self, request):
        nama = request.data.get('nama', '').strip()
        no_telp = request.data.get('no_telp', '').strip()

        if not nama:
            return Response({'error': 'Nama tidak boleh kosong!'}, status=400)

        if Pelanggan.objects.filter(nama__iexact=nama).exists():
            return Response({'error': f'Pelanggan "{nama}" sudah terdaftar!'}, status=400)

        pelanggan = Pelanggan.objects.create(nama=nama, no_telp=no_telp)
        return Response({
            'success': True,
            'id': pelanggan.id,
            'nama': pelanggan.nama,
            'no_telp': pelanggan.no_telp,
            'message': f'Member "{nama}" berhasil didaftarkan!'
        })

class BayarHutangView(APIView):
    def post(self, request):
        pelanggan_id = request.data.get('pelanggan_id')
        jumlah_bayar = request.data.get('jumlah_bayar')

        try:
            pelanggan = Pelanggan.objects.get(id=pelanggan_id)
            hutang_sebelum = float(pelanggan.total_hutang)  # simpan dulu sebelum dikurangi
            
            pelanggan.total_hutang -= int(jumlah_bayar)
            if pelanggan.total_hutang < 0:
                pelanggan.total_hutang = 0
            pelanggan.save()
            
            kembalian = int(jumlah_bayar) - hutang_sebelum
            
            return Response({
                'success': True,
                'hutang_sebelum': hutang_sebelum,
                'sisa_hutang': float(pelanggan.total_hutang),
                'kembalian': kembalian if kembalian > 0 else 0,
                'message': f'Pembayaran hutang Rp {int(jumlah_bayar):,} berhasil!'
            })
        except Pelanggan.DoesNotExist:
            return Response({'error': 'Pelanggan tidak ditemukan'}, status=400)