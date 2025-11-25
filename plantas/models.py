from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

class Planta(models.Model):
    DIFICULDADE_CHOICES = [
        ('F', 'Fácil'),
        ('M', 'Média'),
        ('D', 'Difícil'),
    ]
    
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=100)
    dificuldade = models.CharField(max_length=1, choices=DIFICULDADE_CHOICES)
    necessidade_agua = models.CharField(max_length=50, verbose_name='Necessidade de Água')
    necessidade_luz = models.CharField(max_length=50, verbose_name='Necessidade de Luz')
    descricao = models.TextField(verbose_name='Descrição')
    imagem = models.ImageField(upload_to='plantas/', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} ({self.especie})"
    
    def total_dicas(self):
        return self.dicas.count()

class DicaCultivo(models.Model):
    ESTACAO_CHOICES = [
        ('PRI', 'Primavera'),
        ('VER', 'Verão'),
        ('OUT', 'Outono'),
        ('INV', 'Inverno'),
    ]
    
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='dicas')
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    estacao = models.CharField(max_length=3, choices=ESTACAO_CHOICES, verbose_name='Estação')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.planta.nome}"