from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

class Planta(models.Model):
    DIFICULDADE_CHOICES = [
        ('F', 'Fácil'), ('M', 'Média'), ('D', 'Difícil'),
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

class Comentario(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField(verbose_name='Comentário')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

    def __str__(self):
        return f"Comentário de {self.autor.username} em {self.planta.nome}"

# PERFIL DO USUÁRIO
class UserProfile(models.Model):
    EXPERIENCIA_CHOICES = [
        ('INICIANTE', '🌱 Iniciante'),
        ('INTERMEDIARIO', '🌿 Intermediário'),
        ('AVANCADO', '🌳 Avançado'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Foto de Perfil')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Bio')
    localizacao = models.CharField(max_length=100, blank=True, verbose_name='Cidade/Estado')
    nivel_experiencia = models.CharField(max_length=15, choices=EXPERIENCIA_CHOICES, default='INICIANTE')
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Perfil de {self.user.username}'
    
    def get_total_posts(self):
        return self.user.planta_set.count()
    
    def get_total_likes_recebidos(self):
        return LikePlanta.objects.filter(planta__autor=self.user).count()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# SISTEMA DE LIKES
class LikePlanta(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='likes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('planta', 'usuario')
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
    
    def __str__(self):
        return f'{self.usuario.username} curtiu {self.planta.nome}'

# SISTEMA DE FAVORITOS
class FavoritoPlanta(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='favoritado_por')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('planta', 'usuario')
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
    
    def __str__(self):
        return f'{self.usuario.username} favoritou {self.planta.nome}'

# SISTEMA DE SEGUIR (REMOVIDA A DUPLICAÇÃO)
class Seguir(models.Model):
    seguidor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguindo')
    seguindo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguidores')
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('seguidor', 'seguindo')
        verbose_name = 'Seguir'
        verbose_name_plural = 'Seguidores'
    
    def __str__(self):
        return f'{self.seguidor.username} segue {self.seguindo.username}'
    
    def save(self, *args, **kwargs):
        if self.seguidor == self.seguindo:
            raise ValueError("Um usuário não pode seguir a si mesmo")
        super().save(*args, **kwargs)

# SISTEMA DE DENÚNCIA
class Denuncia(models.Model):
    CATEGORIA_CHOICES = [
        ('CONTEUDO_INADIPROPRIO', 'Conteúdo impróprio'),
        ('INFORMACAO_FALSA', 'Informação falsa'),
        ('SPAM', 'Spam'),
        ('COPYRIGHT', 'Violação de copyright'),
        ('FOTO_PERFIL', 'Foto de perfil inadequada'),
    ]
    
    denunciador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='denuncias_feitas')
    categoria = models.CharField(max_length=25, choices=CATEGORIA_CHOICES)
    descricao = models.TextField(blank=True, verbose_name='Descrição detalhada')
    
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, null=True, blank=True)
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, null=True, blank=True)
    perfil_reportado = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='denuncias_recebidas')
    
    criada_em = models.DateTimeField(auto_now_add=True)
    resolvida = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Denúncia'
        verbose_name_plural = 'Denúncias'
    
    def __str__(self):
        return f'Denúncia {self.categoria} por {self.denunciador.username}'

# SISTEMA DE BADGES/CONQUISTAS
class Badge(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField()
    icone = models.CharField(max_length=5, default='🏆')
    regra = models.CharField(max_length=50, help_text="Ex: '5_postagens', '10_likes', 'primeira_planta'")
    pontos = models.IntegerField(default=10)
    
    def __str__(self):
        return f'{self.icone} {self.nome}'

class UserBadge(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    concedida_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'badge')
    
    def __str__(self):
        return f'{self.usuario.username} - {self.badge.nome}'

class Notificacao(models.Model):
    TIPO_CHOICES = [
        ('SEGUIR', 'Novo seguidor'),
        ('LIKE', 'Sua planta foi curtida'),
        ('COMENTARIO', 'Novo comentário na sua planta'),
        ('BADGE', 'Você ganhou uma conquista'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    mensagem = models.CharField(max_length=255)
    dados_json = models.JSONField(default=dict, blank=True)  # Ex: {"planta_id": 1, "usuario_id": 2}
    lida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-lida', '-criada_em']
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'

    def __str__(self):
        return f"{self.tipo} para {self.usuario.username}"