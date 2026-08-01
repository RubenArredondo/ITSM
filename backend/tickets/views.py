from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import timedelta
from django.utils import timezone
from .models import Ticket
from .serializers import TicketSerializer
from django.db.models import Q


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

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
        serializer.save(fecha_vencimiento_sla=fecha_vencimiento)

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

