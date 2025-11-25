from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('plantas.urls')),  # Inclui todas as URLs do app plantas
]