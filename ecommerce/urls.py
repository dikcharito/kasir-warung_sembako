from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

admin.site.site_header = "Ecommerce Admin"
admin.site.site_title = "Ecommerce Admin Panel"
admin.site.index_title = "Selamat Datang"

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Lempar root (/) otomatis ke halaman produk utama
    path('', RedirectView.as_view(url='/products/', permanent=False)),
    
    # Cukup pakai path kosong ('') di sini agar struktur asli di products/urls.py tidak kedobelan
    path('', include('products.urls')),
    
    # API endpoints
    path('api/', include('products.urls')),
    path('api/accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)