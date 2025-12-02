from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Planta, Comentario, LikePlanta, Badge, UserBadge
from .models import Notificacao, LikePlanta, Comentario, Seguir, UserBadge
from .models import UserProfile


def conceder_badge(usuario, regra_nome):
    """Função auxiliar para conceder badge"""
    badge = Badge.objects.filter(regra=regra_nome).first()
    if badge and not UserBadge.objects.filter(usuario=usuario, badge=badge).exists():
        UserBadge.objects.create(usuario=usuario, badge=badge)
        # Pode adicionar notificação aqui futuramente
        print(f"🏆 Badge concedida: {badge.nome} para {usuario.username}")

# BADGE: Primeira Planta
@receiver(post_save, sender=Planta)
def badge_primeira_planta(sender, instance, created, **kwargs):
    if created and instance.autor.planta_set.count() == 1:
        conceder_badge(instance.autor, 'primeira_planta')

# BADGE: 5 Plantas
@receiver(post_save, sender=Planta)
def badge_cinco_plantas(sender, instance, created, **kwargs):
    if created and instance.autor.planta_set.count() == 5:
        conceder_badge(instance.autor, '5_postagens')

# BADGE: 10 Plantas
@receiver(post_save, sender=Planta)
def badge_dez_plantas(sender, instance, created, **kwargs):
    if created and instance.autor.planta_set.count() == 10:
        conceder_badge(instance.autor, '10_postagens')

# BADGE: Primeiro Comentário
@receiver(post_save, sender=Comentario)
def badge_primeiro_comentario(sender, instance, created, **kwargs):
    if created and instance.autor.comentario_set.count() == 1:
        conceder_badge(instance.autor, 'primeiro_comentario')

# BADGE: 5 Comentários
@receiver(post_save, sender=Comentario)
def badge_cinco_comentarios(sender, instance, created, **kwargs):
    if created and instance.autor.comentario_set.count() == 5:
        conceder_badge(instance.autor, '5_comentarios')

# BADGE: 10 Likes Recebidos
@receiver(post_save, sender=LikePlanta)
def badge_dez_likes_recebidos(sender, instance, created, **kwargs):
    if created:
        autor = instance.planta.autor
        total_likes = LikePlanta.objects.filter(planta__autor=autor).count()
        if total_likes == 10:
            conceder_badge(autor, '10_likes_recebidos')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

# Notificação: Nova curtida
@receiver(post_save, sender=LikePlanta)
def notificar_like(sender, instance, created, **kwargs):
    if created:
        Notificacao.objects.create(
            usuario=instance.planta.autor,
            tipo='LIKE',
            mensagem=f"{instance.usuario.username} curtiu sua planta '{instance.planta.nome}'.",
            dados_json={'planta_id': instance.planta.pk, 'usuario_id': instance.usuario.pk}
        )

# Notificação: Novo comentário
@receiver(post_save, sender=Comentario)
def notificar_comentario(sender, instance, created, **kwargs):
    if created:
        Notificacao.objects.create(
            usuario=instance.planta.autor,
            tipo='COMENTARIO',
            mensagem=f"{instance.autor.username} comentou em '{instance.planta.nome}'.",
            dados_json={'planta_id': instance.planta.pk, 'usuario_id': instance.autor.pk}
        )

# Notificação: Novo seguidor
@receiver(post_save, sender=Seguir)
def notificar_seguir(sender, instance, created, **kwargs):
    if created:
        Notificacao.objects.create(
            usuario=instance.seguindo,
            tipo='SEGUIR',
            mensagem=f"{instance.seguidor.username} começou a te seguir.",
            dados_json={'usuario_id': instance.seguidor.pk}
        )

# Notificação: Nova conquista (badge)
@receiver(post_save, sender=UserBadge)
def notificar_badge(sender, instance, created, **kwargs):
    if created:
        Notificacao.objects.create(
            usuario=instance.usuario,
            tipo='BADGE',
            mensagem=f"Você ganhou a conquista: {instance.badge.nome}!",
            dados_json={'badge_id': instance.badge.pk}
        )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # Se não existir, cria
        UserProfile.objects.get_or_create(user=instance)