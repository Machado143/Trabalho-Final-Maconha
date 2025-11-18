from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Planta(models.Model):
    """
    Model para representar uma planta no catálogo Pai do Verde.
    """
    DIFICULDADE_CHOICES = [
        ('facil', 'Fácil'),
        ('media', 'Média'),
        ('dificil', 'Difícil'),
    ]
    
    NECESSIDADE_AGUA_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
    ]
    
    NECESSIDADE_LUZ_CHOICES = [
        ('sombra', 'Sombra'),
        ('meia_sombra', 'Meia Sombra'),
        ('sol_pleno', 'Sol Pleno'),
    ]
    
    nome_popular = models.CharField(
        max_length=200,
        verbose_name="Nome Popular",
        help_text="Nome popular da planta"
    )
    
    nome_cientifico = models.CharField(
        max_length=200,
        verbose_name="Nome Científico",
        blank=True,
        null=True,
        help_text="Nome científico da planta (opcional)"
    )
    
    familia = models.CharField(
        max_length=100,
        verbose_name="Família",
        blank=True,
        null=True
    )
    
    dificuldade = models.CharField(
        max_length=10,
        choices=DIFICULDADE_CHOICES,
        default='media',
        verbose_name="Dificuldade de Cultivo"
    )
    
    necessidade_agua = models.CharField(
        max_length=10,
        choices=NECESSIDADE_AGUA_CHOICES,
        default='media',
        verbose_name="Necessidade de Água"
    )
    
    necessidade_luz = models.CharField(
        max_length=15,
        choices=NECESSIDADE_LUZ_CHOICES,
        default='meia_sombra',
        verbose_name="Necessidade de Luz"
    )
    
    temperatura_minima = models.IntegerField(
        verbose_name="Temperatura Mínima (°C)",
        validators=[MinValueValidator(-10), MaxValueValidator(50)],
        blank=True,
        null=True
    )
    
    temperatura_maxima = models.IntegerField(
        verbose_name="Temperatura Máxima (°C)",
        validators=[MinValueValidator(-10), MaxValueValidator(50)],
        blank=True,
        null=True
    )
    
    descricao = models.TextField(
        verbose_name="Descrição",
        blank=True,
        null=True,
        help_text="Descrição geral da planta"
    )
    
    dicas_cultivo = models.TextField(
        verbose_name="Dicas de Cultivo",
        blank=True,
        null=True,
        help_text="Dicas específicas para o cultivo"
    )
    
    toxica = models.BooleanField(
        default=False,
        verbose_name="Tóxica",
        help_text="Marque se a planta é tóxica para humanos ou animais"
    )
    
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    
    class Meta:
        verbose_name = "Planta"
        verbose_name_plural = "Plantas"
        ordering = ['nome_popular']
    
    def __str__(self):
        if self.nome_cientifico:
            return f"{self.nome_popular} ({self.nome_cientifico})"
        return self.nome_popular
    
    def get_dificuldade_display_emoji(self):
        """Retorna um emoji representando a dificuldade"""
        emojis = {
            'facil': '🌱',
            'media': '🌿',
            'dificil': '🌳'
        }
        return emojis.get(self.dificuldade, '❓')
    
    def get_necessidade_agua_display_emoji(self):
        """Retorna um emoji representando a necessidade de água"""
        emojis = {
            'baixa': '💧',
            'media': '💧💧',
            'alta': '💧💧💧'
        }
        return emojis.get(self.necessidade_agua, '❓')