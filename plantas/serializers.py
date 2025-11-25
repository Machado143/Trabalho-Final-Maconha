from rest_framework import serializers
from .models import Planta, DicaCultivo

class DicaCultivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DicaCultivo
        fields = '__all__'

class PlantaSerializer(serializers.ModelSerializer):
    dicas = DicaCultivoSerializer(many=True, read_only=True)
    autor_nome = serializers.CharField(source='autor.username', read_only=True)
    
    class Meta:
        model = Planta
        fields = ['id', 'nome', 'especie', 'dificuldade', 'necessidade_agua', 
                 'necessidade_luz', 'descricao', 'imagem', 'autor_nome', 'criado_em', 'dicas']
