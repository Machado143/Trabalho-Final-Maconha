from django import template

register = template.Library()

@register.simple_tag
def notificacoes_nao_lidas(usuario):
    return usuario.notificacoes.filter(lida=False).count()