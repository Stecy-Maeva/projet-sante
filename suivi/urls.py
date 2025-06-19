# suivi/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import (DonneeSanteeViewSet, home, register_page, login_page,
                    api_register, api_login)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import dashboard, ajouter_donnees, analyse_donnees



router = routers.DefaultRouter()
router.register(r'sante', DonneeSanteeViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path("api/register/", api_register, name="api_register"),
    path("api/login/", api_login, name="api_login"),
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("dashboard/", dashboard, name="dashboard"),
    path("ajouter/", ajouter_donnees, name="ajouter"),
    path("analyse/", analyse_donnees, name="analyse"),
]
