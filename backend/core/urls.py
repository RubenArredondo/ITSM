from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core.views import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    LogoutView,
    PerfilUsuarioView,
    RegisterView,
)
urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refres_pair'),
    path('api/logout/', LogoutView.as_view(), name='auth_logout'),
    path('api/me/', PerfilUsuarioView.as_view(), name='user_perfil'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/', include('tickets.urls')),
]
