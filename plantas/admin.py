from django.contrib import admin
from .models import Planta, DicaCultivo, Categoria

class DicaCultivoInline(admin.TabularInline):
    model = DicaCultivo
    extra = 1

@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie', 'dificuldade', 'autor', 'criado_em', 'total_dicas')
    list_filter = ('dificuldade', 'criado_em')
    search_fields = ('nome', 'especie')
    inlines = [DicaCultivoInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(autor=request.user)

@admin.register(DicaCultivo)
class DicaCultivoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'planta', 'estacao', 'criado_em')
    list_filter = ('estacao', 'criado_em')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')