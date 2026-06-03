from rest_framework import serializers
from django.utils import timezone
from .models import Profissional, Consulta

class ProfissionalSerializer(serializers.ModelSerializer):

    class Meta:
            model = Profissional
            fields = '__all__'
    
    def validate_nome_social(self, value):
          nome_sanitizado = value.strip()
          if not nome_sanitizado:
                raise serializers.ValidationError("O nome social não pode estar em branco.")
          
          if '<' in nome_sanitizado or '>' in nome_sanitizado:
                raise serializers.ValidationError("Caracteres inválidos detectados.")
          
          return nome_sanitizado
    
    def validate_contato(self,value):
          contato_sanitizado = value.strip()
          if not contato_sanitizado:
                raise serializers.ValidationError("O contato é obrigatório.")
          return contato_sanitizado
    
class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = '__all__'

    def validate_data(self,value):
        if value < timezone.now():
            raise serializers.ValidationError("A data de consulta não pode estar no passado.")
        return value
        
