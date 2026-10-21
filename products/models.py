from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, blank=True)
    image = models.ImageField (
        upload_to='static/category', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"

class QuantityVariant(models.Model):
    variant_name = models.CharField(max_length=100)

    def __str__(self):
        return self.variant_name

    class Meta:
        verbose_name_plural = "Quantity Variants"

class ColorVariant(models.Model):
    color_name = models.CharField(max_length=100)
    color_code = models.CharField(max_length=10)

    def __str__(self):
        return self.color_name

    class Meta:
        verbose_name_plural = "Color Variants"

class SizeVariant(models.Model):
    size_name = models.CharField(max_length=100)

    def __str__(self):
        return self.size_name

    class Meta:
        verbose_name_plural = "Size Variants"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/product')

    # Harga jual eceran
    price = models.CharField(max_length=20)
    # Harga Pokok Penjualan (HPP) / harga beli dari supplier
    hpp = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Harga jual grosir (pembelian dalam jumlah banyak)
    harga_grosir = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    description = models.TextField()
    # Stok dalam satuan eceran
    stock = models.IntegerField(default=100)
    # Batas stok kritis - akan muncul alert jika stok di bawah nilai ini
    stok_kritis = models.IntegerField(default=5)

    quantity = models.ForeignKey(
        QuantityVariant, on_delete=models.PROTECT, null=True, blank=True)
    color_type = models.ForeignKey(
        ColorVariant, on_delete=models.PROTECT, null=True, blank=True)
    size_type = models.ForeignKey(
        SizeVariant, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.product_name

    def is_stok_kritis(self):
        # Method untuk cek apakah stok sudah kritis
        return self.stock <= self.stok_kritis

    class Meta:
        verbose_name_plural = "Products"

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='static/products')

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name_plural = "Product Images"

class Pelanggan(models.Model):
    # Model untuk data pelanggan tetap warung
    nama = models.CharField(max_length=100)
    no_telp = models.CharField(max_length=15, blank=True)
    
    #tambahalamat
    alamat = models.TextField(blank=True)
    #jalanin migrasi di terminal
    #python manage.py makemigrations
    #python manage.py migrate

    # Total hutang pelanggan yang belum dibayar
    total_hutang = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "Pelanggan"

class Transaksi(models.Model):
    METODE_BAYAR = [
        ('tunai', 'Tunai'),
        ('hutang', 'Hutang'),
    ]

    nomor_nota = models.CharField(max_length=50, unique=True)
    pelanggan = models.ForeignKey(
        Pelanggan, on_delete=models.SET_NULL, null=True, blank=True)
    total_harga = models.DecimalField(max_digits=10, decimal_places=2)
    total_hpp = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    uang_bayar = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    kembalian = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metode_bayar = models.CharField(max_length=10, choices=METODE_BAYAR, default='tunai')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota {self.nomor_nota}"

    def laba(self):
        # Hitung laba = total harga jual - total HPP
        return self.total_harga - self.total_hpp

    class Meta:
        verbose_name_plural = "Transaksi"

class DetailTransaksi(models.Model):
    transaksi = models.ForeignKey(
        Transaksi, on_delete=models.CASCADE, related_name='details')
    produk = models.ForeignKey(Product, on_delete=models.PROTECT)
    jumlah = models.IntegerField()
    harga_jual = models.DecimalField(max_digits=10, decimal_places=2)
    hpp_saat_transaksi = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produk.product_name} x {self.jumlah}"

    class Meta:
        verbose_name_plural = "Detail Transaksi"

class PenerimaanBarang(models.Model):
    produk = models.ForeignKey(Product, on_delete=models.CASCADE)
    jumlah = models.IntegerField()
    harga_beli = models.DecimalField(max_digits=10, decimal_places=2)
    tanggal_terima = models.DateField()
    keterangan = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        produk = self.produk

        # Cek apakah harga beli berubah dari HPP sebelumnya
        if produk.hpp != self.harga_beli:
            # Catat perubahan harga otomatis ke RiwayatHarga
            RiwayatHarga.objects.create(
                produk=produk,
                harga_lama=produk.hpp,
                harga_baru=self.harga_beli,
                keterangan=f'Update otomatis dari penerimaan barang {self.tanggal_terima}'
            )
            # Update HPP produk dengan harga beli terbaru
            produk.hpp = self.harga_beli

        # Tambah stok produk
        produk.stock += self.jumlah
        produk.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produk.product_name} - {self.jumlah} - {self.tanggal_terima}"

    class Meta:
        verbose_name_plural = "Penerimaan Barang"
        
class RiwayatHarga(models.Model):
    # Model untuk mencatat perubahan harga produk
    produk = models.ForeignKey(Product, on_delete=models.CASCADE)
    harga_lama = models.DecimalField(max_digits=10, decimal_places=2)
    harga_baru = models.DecimalField(max_digits=10, decimal_places=2)
    tanggal_ubah = models.DateTimeField(auto_now_add=True)
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return f"{self.produk.product_name} - Rp {self.harga_lama} → Rp {self.harga_baru}"

    class Meta:
        verbose_name_plural = "Riwayat Harga"