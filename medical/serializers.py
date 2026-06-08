import re
from rest_framework import serializers
from django.utils import timezone
from .models import Profissional, Consulta


def sanitizar_texto(valor, nome_campo):
    texto = valor.strip()
    if not texto:
        raise serializers.ValidationError(
            f"O campo {nome_campo} não pode estar em branco."
        )

    padroes_perigosos = [
        r'<\s*script',
        r'javascript\s*:',
        r'on\w+\s*=',      
        r'<\s*iframe',
        r'<\s*object',
        r'<\s*embed',
    ]
    for padrao in padroes_perigosos:
        if re.search(padrao, texto, re.IGNORECASE):
            raise serializers.ValidationError(
                f"Conteúdo potencialmente malicioso detectado "
                f"no campo {nome_campo}."
            )

    texto_limpo = re.sub(r'<[^>]*>', '', texto)

    return texto_limpo


class ProfissionalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profissional
        fields = '__all__'

    def validate_nome_social(self, value):
        return sanitizar_texto(value, 'nome social')

    def validate_profissao(self, value):
        return sanitizar_texto(value, 'profissão')

    def validate_endereco(self, value):
        return sanitizar_texto(value, 'endereço')

    def validate_contato(self, value):
        contato = value.strip()
        if not contato:
            raise serializers.ValidationError("O contato é obrigatório.")

        contato = re.sub(r'<[^>]*>', '', contato)

        if not re.match(r'^[\w\s@.\-+()/]+$', contato):
            raise serializers.ValidationError(
                "Formato de contato inválido. "
                "Use apenas letras, números e caracteres básicos."
            )

        return contato


class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = '__all__'

    def validate_data(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "A data de consulta não pode estar no passado."
            )
        return value
