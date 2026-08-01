from rest_framework import serializers
from .models import Ticket, ComentarioTicket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['solicitante', 'fecha_vencimiento_sla', 'fecha_creacion', 'fecha_actualizacion']

    def validate(self, data):
        if self.instance is not None:
            estado_actual = self.instance.estado
            nuevo_estado = data.get('estado', estado_actual)

            if estado_actual == Ticket.Estado.NUEVO and nuevo_estado not in [
                Ticket.Estado.NUEVO,
                Ticket.Estado.EN_REVISION
            ]:
                raise serializers.ValidationError({
                    'estado': (f'No se puede pasar de nuevo a {nuevo_estado} directamente.')
                })

            if nuevo_estado == Ticket.Estado.CERRADO and estado_actual != Ticket.Estado.RESUELTO:
                raise serializers.ValidationError({
                'estado': (
                    f'No se puede cerrar un ticket en estado {estado_actual}. '
                    'Debe estar RESUELTO antes de cerrarse.'
                )
            })
        return data

class ComentarioSerializer(serializers.ModelSerializer):
    autor_username = serializers.CharField(source='autor.username', read_only=True)

    class Meta:
        model = ComentarioTicket
        fields = ['id', 'ticket', 'autor', 'autor_username', 'texto', 'fecha_creacion']
        read_only_fields = ['ticket', 'autor', 'fecha_creacion']
