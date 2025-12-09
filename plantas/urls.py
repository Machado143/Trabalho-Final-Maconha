from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    # =============================
    # PÁGINA INICIAL
    # =============================
    path('', views.listar_plantas, name='index'),

    # =============================
    # PLANTAS
    # =============================
    path('plantas/', views.listar_plantas, name='listar_plantas'),
    path('plantas/criar/', views.criar_planta, name='criar_planta'),
    path('plantas/<int:pk>/', views.detalhe_planta, name='detalhe_planta'),
    path('plantas/<int:pk>/editar/', views.editar_planta, name='editar_planta'),
    path('plantas/<int:pk>/excluir/', views.excluir_planta, name='excluir_planta'),

    # Interações
    path('plantas/<int:planta_pk>/like/', views.toggle_like, name='toggle_like'),
    path('plantas/<int:planta_pk>/favorito/', views.toggle_favorito, name='toggle_favorito'),

    # Comentários
    path('plantas/<int:planta_pk>/comentarios/criar/', views.criar_comentario, name='criar_comentario'),

    # =============================
    # PERFIL
    # =============================
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/<str:username>/', views.ver_perfil, name='ver_perfil'),
    path('perfil/<str:username>/seguir/', views.toggle_seguir, name='toggle_seguir'),

    # =============================
    # COLEÇÕES ✅ (corrigido)
    # =============================
    path('colecoes/', views.colecoes_usuario, name='colecoes'),
    path('colecoes/criar/', views.criar_colecao, name='criar_colecao'),
    path('colecoes/<int:colecao_id>/', views.ver_colecao, name='ver_colecao'),

    # =============================
    # DIÁRIO
    # =============================
    path('plantas/<int:planta_pk>/diario/', views.diario_planta, name='diario_planta'),
    path('plantas/<int:planta_pk>/diario/adicionar/', views.adicionar_entrada_diario, name='adicionar_entrada_diario'),

    # =============================
    # DASHBOARD
    # =============================
    path('dashboard/', views.dashboard_estatisticas, name='dashboard_estatisticas'),

    # =============================
    # DENÚNCIA
    # =============================
    path('denuncia/<str:tipo>/<int:obj_id>/', views.criar_denuncia, name='criar_denuncia'),

    # =============================
    # BUSCA
    # =============================
    path('buscar/', views.buscar, name='buscar'),

    # =============================
    # AUTENTICAÇÃO
    # =============================
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    # =============================
    # API
    # =============================
    path('api/', include(router.urls)),

    # =============================
    # NOTIFICAÇÕES
    # =============================
    path('notificacoes/', views.listar_notificacoes, name='listar_notificacoes'),

    # =============================
    # FEED ✅ (corrigido)
    # =============================
    path('feed/', views.feed_atividades, name='feed'),

    # =============================
    # RANKING ✅ (corrigido)
    # =============================
    path('ranking/', views.ranking_jardineiros, name='ranking'),

    # =============================
    # LEMBRETES
    # =============================
    path('lembretes/', views.listar_lembretes, name='listar_lembretes'),
    path('lembretes/criar/', views.criar_lembrete, name='criar_lembrete'),
    path('lembretes/<int:planta_pk>/criar/', views.criar_lembrete, name='criar_lembrete_planta'),
    path('lembretes/<int:lembrete_pk>/feito/', views.marcar_lembrete_feito, name='marcar_lembrete_feito'),

    # =============================
    # MENSAGENS
    # =============================
    path('mensagens/', views.listar_mensagens, name='listar_mensagens'),
    path('mensagens/enviar/', views.enviar_mensagem, name='enviar_mensagem'),
    path('mensagens/enviar/<str:username>/', views.enviar_mensagem, name='enviar_mensagem_usuario'),
    path('mensagens/<int:mensagem_pk>/', views.ver_mensagem, name='ver_mensagem'),

    # =============================
    # ENQUETES
    # =============================
    path('enquetes/', views.listar_enquetes, name='listar_enquetes'),
    path('enquetes/criar/', views.criar_enquete, name='criar_enquete'),
    path('enquetes/<int:enquete_pk>/votar/', views.votar_enquete, name='votar_enquete'),
]
