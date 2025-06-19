# projet_sante/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # On inclut les URLs de notre application
    path('', include('suivi.urls')),
]
