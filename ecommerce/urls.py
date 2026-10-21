from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView  # <--- 1. Tambahkan baris ini

admin.site.site_header = "Ecommerce Admin"
admin.site.site_title = "Ecommerce Admin Panel"
admin.site.index_title = "Selamat Datang"

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # <--- 2. Ubah baris ini agar root langsung ke login
    path('', RedirectView.as_view(url='/admin/login/', permanent=False)),
    
    path('api/', include('products.urls')),
    path('api/accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)