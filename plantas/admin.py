from django.contrib import admin
from .models import (
    Planta, Comentario, Categoria, UserProfile,
    LikePlanta, FavoritoPlanta, Seguir, Denuncia,
    Badge, UserBadge, Notificacao, Colecao, DiarioPlanta,
    Lembrete, Mensagem, Enquete, OpcaoEnquete, VotoEnquete,
    Conquista, UsuarioConquista
)
from django.utils.html import format_html

admin.site.site_header = "🌿 Pai do Verde - Administração"
admin.site.site_title = "Pai do Verde Admin"
admin.site.index_title = "Painel de Controle"

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

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'mensagem_resumida', 'lida', 'criada_em')
    list_filter = ('tipo', 'lida', 'criada_em')
    search_fields = ('usuario__username', 'mensagem')
    date_hierarchy = 'criada_em'
    actions = ['marcar_como_lida']

    def mensagem_resumida(self, obj):
        return obj.mensagem[:50] + "..." if len(obj.mensagem) > 50 else obj.mensagem
    mensagem_resumida.short_description = 'Mensagem'

    def marcar_como_lida(self, request, queryset):
        queryset.update(lida=True)
        self.message_user(request, f'{queryset.count()} notificações marcadas como lidas.')
    marcar_como_lida.short_description = "✅ Marcar como lida"

@admin.register(Colecao)
class ColecaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'total_plantas_display', 'publica', 'criada_em')
    list_filter = ('publica', 'criada_em')
    search_fields = ('nome', 'usuario__username', 'descricao')
    filter_horizontal = ('plantas',)

    def total_plantas_display(self, obj):
        return obj.plantas.count()
    total_plantas_display.short_description = '🌱 Plantas'

@admin.register(DiarioPlanta)
class DiarioPlantaAdmin(admin.ModelAdmin):
    list_display = ('planta', 'usuario', 'data', 'titulo', 'regou', 'fertilizou')
    list_filter = ('data', 'regou', 'fertilizou')
    search_fields = ('planta__nome', 'usuario__username', 'titulo', 'anotacao')
    date_hierarchy = 'data'

@admin.register(Lembrete)
class LembreteAdmin(admin.ModelAdmin):
    list_display = ('planta', 'usuario', 'tipo', 'proxima_data', 'ativo', 'frequencia')
    list_filter = ('tipo', 'frequencia', 'ativo', 'proxima_data')
    search_fields = ('planta__nome', 'usuario__username', 'notas')
    actions = ['marcar_ativo', 'marcar_inativo']

    def marcar_ativo(self, request, queryset):
        queryset.update(ativo=True)
    marcar_ativo.short_description = "✅ Ativar lembretes"

    def marcar_inativo(self, request, queryset):
        queryset.update(ativo=False)
    marcar_inativo.short_description = "❌ Desativar lembretes"

@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('remetente', 'destinatario', 'assunto_display', 'lida', 'criada_em')
    list_filter = ('lida', 'criada_em')
    search_fields = ('remetente__username', 'destinatario__username', 'assunto', 'conteudo')
    date_hierarchy = 'criada_em'

    def assunto_display(self, obj):
        return obj.assunto if obj.assunto else '(sem assunto)'
    assunto_display.short_description = 'Assunto'

class OpcaoEnqueteInline(admin.TabularInline):
    model = OpcaoEnquete
    extra = 2
    fields = ('texto', 'ordem')

@admin.register(Enquete)
class EnqueteAdmin(admin.ModelAdmin):
    list_display = ('pergunta', 'autor', 'total_votos_display', 'ativa', 'data_fim')
    list_filter = ('ativa', 'data_inicio', 'data_fim')
    search_fields = ('pergunta', 'descricao', 'autor__username')
    inlines = [OpcaoEnqueteInline]

    def total_votos_display(self, obj):
        return obj.total_votos()
    total_votos_display.short_description = '🗳️ Votos'

@admin.register(VotoEnquete)
class VotoEnqueteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'opcao', 'enquete_display', 'criado_em')
    list_filter = ('criado_em',)
    search_fields = ('usuario__username', 'opcao__texto', 'opcao__enquete__pergunta')

    def enquete_display(self, obj):
        return obj.opcao.enquete.pergunta
    enquete_display.short_description = 'Enquete'

@admin.register(Conquista)
class ConquistaAdmin(admin.ModelAdmin):
    list_display = ('icone', 'nome', 'tipo', 'pontos', 'rara', 'total_desbloqueadas')
    list_filter = ('tipo', 'rara')
    search_fields = ('nome', 'descricao')

    def total_desbloqueadas(self, obj):
        return obj.usuarioconquista_set.count()
    total_desbloqueadas.short_description = '🎯 Desbloques'

@admin.register(UsuarioConquista)
class UsuarioConquistaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'conquista', 'desbloqueada_em')
    list_filter = ('conquista__tipo', 'desbloqueada_em')
    search_fields = ('usuario__username', 'conquista__nome')
