import logging
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Profissional, Consulta
from .serializers import ProfissionalSerializer, ConsultaSerializer

logger = logging.getLogger('lacrei.access')


class ProfissionalViewSet(viewsets.ModelViewSet):

    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(
            "Profissional criado: id=%s, nome_social=%s",
            instance.id, instance.nome_social,
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info("Profissional atualizado: id=%s", instance.id)

    def perform_destroy(self, instance):
        logger.info(
            "Profissional removido: id=%s, nome_social=%s",
            instance.id, instance.nome_social,
        )
        instance.delete()

    @action(detail=True, methods=['get'])
    def consultas(self, request, pk=None):
        profissional = self.get_object()
        consultas = Consulta.objects.filter(profissional=profissional)
        logger.info(
            "Busca de consultas do profissional id=%s — %d resultado(s)",
            pk, consultas.count(),
        )
        serializer = ConsultaSerializer(consultas, many=True)
        return Response(serializer.data)


class ConsultaViewSet(viewsets.ModelViewSet):

    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(
            "Consulta criada: id=%s, profissional=%s",
            instance.id, instance.profissional_id,
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info("Consulta atualizada: id=%s", instance.id)

    def perform_destroy(self, instance):
        logger.info("Consulta removida: id=%s", instance.id)
        instance.delete()