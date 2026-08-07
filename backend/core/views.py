from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
)

User = get_user_model()


def set_jwt_cookies(response):
    if response.status_code == 200:
        access_token = response.data.get('access')
        refres_token = response.data.get('refresh')

        if access_token:
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=access_token,
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                httponly=True,
                samesite='Lax'
            )

        if refres_token:
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=refres_token,
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                httponly=True,
                samesite='Lax'
            )

        response.data.pop('access', None)
        response.data.pop('refresh', None)
        response.data['message'] = 'Login exitoso'

@extend_schema_view(
    post=extend_schema(
        summary="Iniciar sesión (Login)",
        description="Autentica al usuario. Los tokens JWT no se devuelven en el JSON, sino que se guardan en cookies HTTP-only de forma segura.",
        responses={200: OpenApiTypes.OBJECT},
    )
)
class CookieTokenObtainPairView(TokenObtainPairView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        set_jwt_cookies(response)

        return response

@extend_schema_view(
    post=extend_schema(
        summary="Refrescar Token JWT",
        description="Utiliza la cookie del refresh_token para emitir y guardar un nuevo access_token en las cookies.",
        responses={200: OpenApiTypes.OBJECT},
    )
)
class CookieTokenRefreshView(TokenRefreshView):
     def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])

        if refresh_token and 'refresh' not in request.data:
            data= request.data.copy()
            data['refresh'] = refresh_token
            request._full_data = data

        response = super().post(request, *args, **kwargs)
        set_jwt_cookies(response)
        return response

class LogoutView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        summary="Cerrar sesión (Logout)",
        description="Destruye las cookies que contienen los tokens de acceso y refresco del sistema.",
        request=None,
        responses={200: OpenApiTypes.OBJECT},
    )
    def post(self, request):
        response = Response({"mensaje": "Seccion cerrada"})

        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        return response

class PerfilUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Ver mi perfil",
        description="Devuelve los atributos básicos e información del usuario autenticado.",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'rol': request.user.rol,
            'departamento_id': request.user.departamento_id,
            'departamento_nombre': request.user.departamento.nombre if request.user.departamento else None,
    })

@extend_schema_view(
    post=extend_schema(
        summary='Registro de un nuevo cliente',
        description='Crea una cuenta con el rol de Cliente'
    )
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
