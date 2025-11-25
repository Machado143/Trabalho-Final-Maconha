from rest_framework import serializers
from .models import Planta, Comentario

class ComentarioSerializer(serializers.ModelSerializer):
    autor_nome = serializers.CharField(source='autor.username', read_only=True)
    
    class Meta:
        model = Comentario
        fields = ['id', 'autor', 'autor_nome', 'conteudo', 'criado_em']

class PlantaSerializer(serializers.ModelSerializer):
    comentarios = ComentarioSerializer(many=True, read_only=True)
    autor_nome = serializers.CharField(source='autor.username', read_only=True)
    
    class Meta:
        model = Planta
        fields = ['id', 'nome', 'especie', 'dificuldade', 'necessidade_agua', 
                 'necessidade_luz', 'descricao', 'imagem', 'autor_nome', 'criado_em', 'comentarios']