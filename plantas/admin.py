from django.contrib import admin
from .models import Planta, Comentario, Categoria

@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie', 'dificuldade', 'autor', 'criado_em')
    list_filter = ('dificuldade', 'criado_em')
    search_fields = ('nome', 'especie')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(autor=request.user)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('planta', 'autor', 'criado_em', 'conteudo_resumido')
    list_filter = ('criado_em', 'planta')
    search_fields = ('conteudo', 'autor__username', 'planta__nome')
    
    def conteudo_resumido(self, obj):
        return obj.conteudo[:50] + "..."
    conteudo_resumido.short_description = 'Comentário'

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')