from django.db import models
import uuid

class Profissional(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    nome_social = models.CharField(max_length=255)
    profissao = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    contato = models.CharField(max_length=100)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome_social} - {self.profissao}"
    
class Consulta(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    data = models.DateTimeField()

    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.CASCADE,
        related_name='consultas'
    )

    criado_em = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        data_formatada = self.data.strftime('%d/%m/%Y %H:%M')
        return f"Consulta em {data_formatada} com {self.profissional.nome_social}"
