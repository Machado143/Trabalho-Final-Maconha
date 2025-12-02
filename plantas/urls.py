from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, viewsets
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'api/plantas', viewsets.PlantaViewSet)

urlpatterns = [
    # URLs principais
    path('', views.listar_plantas, name='index'),
    path('plantas/', views.listar_plantas, name='listar_plantas'),
    path('plantas/criar/', views.criar_planta, name='criar_planta'),
    path('plantas/<int:pk>/', views.detalhe_planta, name='detalhe_planta'),
    path('plantas/<int:pk>/editar/', views.editar_planta, name='editar_planta'),
    path('plantas/<int:pk>/excluir/', views.excluir_planta, name='excluir_planta'),
    
    # URLs de interação
    path('plantas/<int:planta_pk>/like/', views.toggle_like, name='toggle_like'),
    path('plantas/<int:planta_pk>/favorito/', views.toggle_favorito, name='toggle_favorito'),
    
    # URLs de comentários
    path('plantas/<int:planta_pk>/comentarios/criar/', views.criar_comentario, name='criar_comentario'),
    
    # URLs de perfil
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/<str:username>/', views.ver_perfil, name='ver_perfil'),
    path('perfil/<str:username>/seguir/', views.toggle_seguir, name='toggle_seguir'),
    
    # URLs de denúncia
    path('denuncia/<str:tipo>/<int:obj_id>/', views.criar_denuncia, name='criar_denuncia'),
    
    # URLs de busca
    path('buscar/', views.buscar, name='buscar'),
    
    # URLs de autenticação
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    
    # URLs da API
    path('', include(router.urls)),

    # Notificações
    path('notificacoes/', views.listar_notificacoes, name='listar_notificacoes'),

]