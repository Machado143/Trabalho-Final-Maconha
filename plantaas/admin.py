from django.contrib import admin
from .models import Planta


@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    """
    Configuração da interface administrativa para o model Planta
    """
    list_display = [
        'nome_popular',
        'nome_cientifico',
        'dificuldade',
        'necessidade_agua',
        'necessidade_luz',
        'toxica',
        'data_cadastro'
    ]
    
    list_filter = [
        'dificuldade',
        'necessidade_agua',
        'necessidade_luz',
        'toxica',
        'data_cadastro'
    ]
    
    search_fields = [
        'nome_popular',
        'nome_cientifico',
        'familia',
        'descricao'
    ]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome_popular', 'nome_cientifico', 'familia')
        }),
        ('Requisitos de Cultivo', {
            'fields': (
                'dificuldade',
                'necessidade_agua',
                'necessidade_luz',
                'temperatura_minima',
                'temperatura_maxima'
            )
        }),
        ('Detalhes e Cuidados', {
            'fields': ('descricao', 'dicas_cultivo', 'toxica')
        }),
        ('Metadados', {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['data_cadastro', 'data_atualizacao']
    
    date_hierarchy = 'data_cadastro'
    
    ordering = ['nome_popular']