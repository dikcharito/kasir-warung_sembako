from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView  # <--- Wajib di-import

admin.site.site_header = "Ecommerce Admin"
admin.site.site_title = "Ecommerce Admin Panel"
admin.site.index_title = "Selamat Datang"

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Otomatis lempar pengunjung dari URL utama (/) ke halaman produk/kasir
    path('', RedirectView.as_view(url='/products/', permanent=False)),
    
    path('products/', include('products.urls')),
    
    # Endpoint API kamu tetap aman di jalurnya masing-masing:
    path('api/', include('products.urls')),
    path('api/accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)