from django.conf import settings
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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

class CookieTokenObtainPairView(TokenObtainPairView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        set_jwt_cookies(response)

        return response

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

    def post(self, request):
        response = Response({"mensaje": "Seccion cerrada"})

        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        return response

class PerfilUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'rol': request.user.rol,
            'departamento_id': request.user.departamento_id,
            'departamento_nombre': request.user.departamento.nombre if request.user.departamento else None,
        })

