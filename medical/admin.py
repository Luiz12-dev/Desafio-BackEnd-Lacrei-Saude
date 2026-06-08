from django.contrib import admin
from .models import Profissional, Consulta


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('nome_social', 'profissao', 'contato', 'criado_em')
    search_fields = ('nome_social', 'profissao')
    list_filter = ('profissao',)
    ordering = ('-criado_em',)


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('id', 'profissional', 'data', 'criado_em')
    list_filter = ('profissional',)
    ordering = ('-data',)
