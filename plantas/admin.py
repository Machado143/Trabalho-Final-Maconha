from django.contrib import admin
from .models import (
    Planta, Comentario, Categoria, UserProfile, 
    LikePlanta, FavoritoPlanta, Seguir, Denuncia, 
    Badge, UserBadge  # ✅ Importações corretas
)

# Registro dos modelos existentes
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

# Registro dos NOVOS modelos
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nivel_experiencia', 'localizacao', 'criado_em')
    search_fields = ('user__username', 'bio', 'localizacao')
    list_filter = ('nivel_experiencia', 'criado_em')

@admin.register(LikePlanta)
class LikePlantaAdmin(admin.ModelAdmin):
    list_display = ('planta', 'usuario', 'criado_em')
    search_fields = ('planta__nome', 'usuario__username')

@admin.register(FavoritoPlanta)
class FavoritoPlantaAdmin(admin.ModelAdmin):
    list_display = ('planta', 'usuario', 'criado_em')
    search_fields = ('planta__nome', 'usuario__username')

@admin.register(Seguir)
class SeguirAdmin(admin.ModelAdmin):
    list_display = ('seguidor', 'seguindo', 'criado_em')
    search_fields = ('seguidor__username', 'seguindo__username')

@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('denunciador', 'categoria', 'criada_em', 'resolvida')
    list_filter = ('categoria', 'resolvida', 'criada_em')
    search_fields = ('denunciador__username', 'descricao')
    actions = ['marcar_resolvida']
    
    def marcar_resolvida(self, request, queryset):
        queryset.update(resolvida=True)
    marcar_resolvida.short_description = "Marcar denúncias como resolvidas"

# ✅ CORREÇÃO: Registro dos modelos de Badge
@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'icone', 'regra', 'pontos')
    search_fields = ('nome', 'descricao')

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'badge', 'concedida_em')
    search_fields = ('usuario__username', 'badge__nome')
    list_filter = ('badge', 'concedida_em')