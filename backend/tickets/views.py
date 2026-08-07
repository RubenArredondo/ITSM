from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from datetime import timedelta
from django.utils import timezone
from .models import Ticket
from .serializers import TicketSerializer, ComentarioSerializer
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db import transaction


User = get_user_model()

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.select_related(
            'solicitante', 'agente_asignado', 'departamento'
        )

        if user.rol == User.Rol.CLIENTE:
            return queryset.filter(solicitante=user)

        return queryset.filter(departamento=user.departamento)


    HORAS_SLA = {
        Ticket.Prioridad.BAJA: 72,  # 72 horas
        Ticket.Prioridad.MEDIA: 48,  # 48 horas
        Ticket.Prioridad.ALTA: 24,   # 24 horas
        Ticket.Prioridad.CRITICA: 4, # 4 horas
    }

    def perform_create(self, serializer):
        prioridad = serializer.validated_data.get('prioridad', Ticket.Prioridad.BAJA)
        horas = self.HORAS_SLA[prioridad]
        fecha_vencimiento = timezone.now() + timedelta(hours=horas)
        serializer.save(
            solicitante = self.request.user,
            fecha_vencimiento_sla=fecha_vencimiento,
        )
    # Documentacion Swagger
    @extend_schema(
            summary = 'Tickets del departamento que vencen en 2 hrs',
            responses = {200: TicketSerializer(many=True)},
    )
    @action(detail=False, methods=['get'])
    def urgencias(self, request):
        limite = timezone.now() +timedelta(hours=2)
        filtro = (
            ~Q(estado__in=[Ticket.Estado.CERRADO, Ticket.Estado.RESUELTO])
            & Q(fecha_vencimiento_sla__lte= limite)
            & Q(fecha_vencimiento_sla__isnull=False)
        )
        if request.user.departamento_id:
            filtro &= Q(departamento=request.user.departamento)

        tickets = self.get_queryset().filter(filtro).order_by('fecha_vencimiento_sla')
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)

    # Documentacion Swagger
    @extend_schema(
        summary = 'Historial de comentarios del ticket (GET) o agregar uno nuevo (POST)',
        request = ComentarioSerializer,
        responses = {200: ComentarioSerializer(many=True)},
    )
    @action(detail=True, methods=['get', 'post'])
    def comentarios(self, request, pk=None):
        ticket = self.get_object()

        if request.method == 'POST':
            serializer = ComentarioSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            with transaction.atomic():
                serializer.save(ticket=ticket, autor=request.user)

                if request.user.rol == User.Rol.CLIENTE and ticket.estado in [
                    Ticket.Estado.ESPERANDO_CLIENTE,
                    Ticket.Estado.RESUELTO,
                ]:
                    ticket.estado = Ticket.Estado.EN_REVISION
                    ticket.save()

            return Response(serializer.data)

        serializer = ComentarioSerializer(ticket.comentarios.all(), many=True)
        return Response(serializer.data)
