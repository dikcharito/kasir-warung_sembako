from django.contrib import admin
from django.utils.html import format_html
from .models import *

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['preview_gambar']
    ordering = ['product_name']

    def preview_gambar(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:150px;border-radius:8px;display:block"/>',
                obj.image.url
            )
        return "Belum ada gambar"

    preview_gambar.short_description = "Preview Gambar"

    class Media:
        js = ('admin/js/preview_gambar.js',)


class PenerimaanBarangAdmin(admin.ModelAdmin):
    readonly_fields = ['hpp_saat_ini']
    fields = ['produk', 'jumlah', 'hpp_saat_ini', 'harga_beli', 'tanggal_terima', 'keterangan']

    def hpp_saat_ini(self, obj):
        if obj and obj.produk:
            return format_html(
                '<strong style="color:#4CAF50;font-size:16px">Rp {}</strong>',
                f"{obj.produk.hpp:,.0f}"
            )
        return "Pilih produk dulu"

    hpp_saat_ini.short_description = "HPP Saat Ini"

    class Media:
        js = ('admin/js/hpp_preview.js',)


admin.site.register(PenerimaanBarang, PenerimaanBarangAdmin)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(QuantityVariant)
admin.site.register(ColorVariant)
admin.site.register(SizeVariant)
admin.site.register(ProductImages)
admin.site.register(Pelanggan)
admin.site.register(Transaksi)
admin.site.register(DetailTransaksi)
admin.site.register(RiwayatHarga)