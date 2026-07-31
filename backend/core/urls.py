from django.contrib import admin
from django.urls import path, include
from core.views import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    LogoutView,
    PerfilUsuarioView
)
urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refres_pair'),
    path('api/logout/', LogoutView.as_view(), name='auth_logout'),
    path('api/me/', PerfilUsuarioView.as_view(), name='user_perfil'),
    path('api/', include('tickets.urls')),
]
