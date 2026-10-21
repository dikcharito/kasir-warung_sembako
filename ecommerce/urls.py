from django.contrib import admin
from django.urls import path, include
from django.conf import settings               # <--- 1. PASTIKAN BARIS INI ADA
from django.conf.urls.static import static     # <--- 2. PASTIKAN BARIS INI ADA

admin.site.site_header = "Ecommerce Admin"
admin.site.site_title = "Ecommerce Admin Panel"
admin.site.index_title = "Selamat Datang"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('api/', include('products.urls')),
    path('api/accounts/', include('accounts.urls')),
    #path('api/', include('cart.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)