from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models.functions import TruncMonth
from django.template.loader import render_to_string
from django.contrib.auth.models import User

# Models
from .models import (
    Planta, Comentario, LikePlanta, FavoritoPlanta, Seguir, 
    UserProfile, Denuncia, Colecao, DiarioPlanta, Lembrete, 
    Mensagem, Enquete, OpcaoEnquete, VotoEnquete
)

# Forms
from .forms import (
    PlantaForm, ComentarioForm, UserProfileForm, DenunciaForm,
    ColecaoForm, DiarioPlantaForm, LembreteForm, MensagemForm, 
    EnqueteForm
)

# REST Framework
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# ===== VIEWS PRINCIPAIS =====

def index(request):
    """Página inicial"""
    return render(request, 'plantas/index.html', {'nome': 'Jardineiro'})

def listar_plantas(request):
    """Listar todas as plantas"""
    plantas = Planta.objects.all().order_by('-criado_em').prefetch_related('comentarios', 'likes', 'favoritado_por')
    return render(request, 'plantas/lista_plantas.html', {'plantas': plantas})

def detalhe_planta(request, pk):
    """Detalhes de uma planta específica"""
    planta = get_object_or_404(Planta.objects.prefetch_related('comentarios', 'likes', 'favoritado_por'), pk=pk)
    return render(request, 'plantas/detalhe_planta.html', {'planta': planta})

# ===== CRUD DE PLANTAS =====

@login_required
def criar_planta(request):
    """Criar nova planta"""
    if request.method == 'POST':
        form = PlantaForm(request.POST, request.FILES)
        if form.is_valid():
            planta = form.save(commit=False)
            planta.autor = request.user
            planta.save()
            messages.success(request, 'Planta cadastrada com sucesso! 🌱')
            return redirect('detalhe_planta', pk=planta.pk)
    else:
        form = PlantaForm()
    
    return render(request, 'plantas/form_planta.html', {
        'form': form, 
        'titulo': 'Nova Planta',
        'planta': None
    })

@login_required
def editar_planta(request, pk):
    """Editar planta existente"""
    planta = get_object_or_404(Planta, pk=pk, autor=request.user)
    if request.method == 'POST':
        form = PlantaForm(request.POST, request.FILES, instance=planta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Planta atualizada! ✨')
            return redirect('detalhe_planta', pk=planta.pk)
    else:
        form = PlantaForm(instance=planta)
    
    return render(request, 'plantas/form_planta.html', {
        'form': form, 
        'titulo': 'Editar Planta',
        'planta': planta
    })

@login_required
def excluir_planta(request, pk):
    """Excluir planta"""
    planta = get_object_or_404(Planta, pk=pk, autor=request.user)
    if request.method == 'POST':
        planta.delete()
        messages.success(request, 'Planta excluída! 🗑️')
        return redirect('listar_plantas')
    return render(request, 'plantas/confirmar_exclusao.html', {'planta': planta})

# ===== AUTENTICAÇÃO =====

def signup(request):
    """Cadastro de novo usuário"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso! 🎉')
            return redirect('listar_plantas')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

# ===== INTERAÇÕES SOCIAIS =====

@login_required
@require_POST
def toggle_like(request, planta_pk):
    """Like/Unlike em planta"""
    planta = get_object_or_404(Planta, pk=planta_pk)
    like, created = LikePlanta.objects.get_or_create(planta=planta, usuario=request.user)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': planta.likes.count()
        })
    
    return redirect(request.META.get('HTTP_REFERER', 'listar_plantas'))

@login_required
@require_POST
def toggle_favorito(request, planta_pk):
    """Favoritar/Desfavoritar planta"""
    planta = get_object_or_404(Planta, pk=planta_pk)
    favorito, created = FavoritoPlanta.objects.get_or_create(planta=planta, usuario=request.user)
    
    if not created:
        favorito.delete()
        favoritado = False
    else:
        favoritado = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'favoritado': favoritado,
            'total_favoritos': planta.favoritado_por.count()
        })
    
    return redirect(request.META.get('HTTP_REFERER', 'listar_plantas'))

@login_required
@require_POST
def toggle_seguir(request, username):
    """Seguir/Deixar de seguir usuário"""
    usuario_target = get_object_or_404(User, username=username)
    
    if usuario_target == request.user:
        messages.error(request, "Você não pode seguir a si mesmo! 🤨")
        return redirect('ver_perfil', username=username)
    
    seguir, created = Seguir.objects.get_or_create(seguidor=request.user, seguindo=usuario_target)
    
    if not created:
        seguir.delete()
        messages.success(request, f'Você deixou de seguir {username} 👋')
    else:
        messages.success(request, f'Você está seguindo {username} 👥')
    
    return redirect('ver_perfil', username=username)

@login_required
def criar_comentario(request, planta_pk):
    """Criar comentário em planta"""
    planta = get_object_or_404(Planta, pk=planta_pk)
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.planta = planta
            comentario.autor = request.user
            comentario.save()
            messages.success(request, 'Comentário adicionado! 💬')
            return redirect('detalhe_planta', pk=planta.pk)
    else:
        form = ComentarioForm()
    
    return render(request, 'plantas/form_comentario.html', {
        'form': form, 
        'planta': planta,
        'titulo': f'Comentar sobre {planta.nome}'
    })

# ===== PERFIL DE USUÁRIO =====

def ver_perfil(request, username):
    """Visualizar perfil de usuário"""
    usuario = get_object_or_404(User, username=username)
    plantas = usuario.planta_set.all().order_by('-criado_em')

    # Estatísticas
    total_postagens = usuario.planta_set.count()
    total_seguidores = usuario.seguidores.count()
    total_seguindo = usuario.seguindo.count()
    esta_seguindo = False
    
    if request.user.is_authenticated:
        esta_seguindo = Seguir.objects.filter(seguidor=request.user, seguindo=usuario).exists()

    context = {
        'usuario_perfil': usuario,
        'plantas': plantas,
        'esta_seguindo': esta_seguindo,
        'total_postagens': total_postagens,
        'total_seguidores': total_seguidores,
        'total_seguindo': total_seguindo,
    }
    return render(request, 'plantas/perfil.html', context)

@login_required
def editar_perfil(request):
    """Editar perfil do usuário"""
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Perfil atualizado com sucesso! ✨')
            return redirect('ver_perfil', username=request.user.username)
    else:
        profile_form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'plantas/editar_perfil.html', {
        'profile_form': profile_form
    })

# ===== SISTEMA DE COLEÇÕES =====

@login_required
def colecoes_usuario(request, username=None):
    """Listar coleções do usuário"""
    if username:
        usuario = get_object_or_404(User, username=username)
    else:
        usuario = request.user
    
    # Criar coleção padrão "Favoritos" se não existir
    colecao_favoritos, _ = Colecao.objects.get_or_create(
        usuario=usuario,
        nome="Favoritos",
        defaults={'descricao': 'Plantas que eu favoritei', 'publica': True}
    )
    
    # Atualizar favoritos
    plantas_favoritas = FavoritoPlanta.objects.filter(usuario=usuario).values_list('planta', flat=True)
    colecao_favoritos.plantas.set(plantas_favoritas)
    
    # Buscar coleções
    if usuario == request.user:
        colecoes = Colecao.objects.filter(usuario=usuario).prefetch_related('plantas')
    else:
        colecoes = Colecao.objects.filter(usuario=usuario, publica=True).prefetch_related('plantas')
    
    context = {
        'usuario_perfil': usuario,
        'colecoes': colecoes,
        'pode_editar': usuario == request.user
    }
    return render(request, 'plantas/colecoes.html', context)

@login_required
def criar_colecao(request):
    """Criar nova coleção"""
    if request.method == 'POST':
        form = ColecaoForm(request.POST)
        if form.is_valid():
            colecao = form.save(commit=False)
            colecao.usuario = request.user
            colecao.save()
            form.save_m2m()
            messages.success(request, f'Coleção "{colecao.nome}" criada com sucesso! 🌿')
            return redirect('colecoes_usuario')
    else:
        form = ColecaoForm()
    
    return render(request, 'plantas/form_colecao.html', {
        'form': form,
        'titulo': 'Nova Coleção'
    })

@login_required
def ver_colecao(request, colecao_id):
    """Visualizar coleção específica"""
    colecao = get_object_or_404(Colecao, pk=colecao_id)
    
    # Verificar permissão
    if not colecao.publica and colecao.usuario != request.user:
        messages.error(request, 'Esta coleção é privada. 🔒')
        return redirect('colecoes_usuario')
    
    context = {
        'colecao': colecao,
        'pode_editar': colecao.usuario == request.user
    }
    return render(request, 'plantas/ver_colecao.html', context)

# ===== DIÁRIO DE PLANTAS =====

@login_required
def diario_planta(request, planta_pk):
    """Diário de cultivo da planta"""
    planta = get_object_or_404(Planta, pk=planta_pk)
    if planta.autor != request.user:
        messages.error(request, 'Você não tem permissão para ver o diário desta planta. 🔒')
        return redirect('detalhe_planta', pk=planta.pk)

    entradas = DiarioPlanta.objects.filter(planta=planta).order_by('-data')
    lembretes = Lembrete.objects.filter(planta=planta, ativo=True).order_by('proxima_data')

    context = {
        'planta': planta,
        'entradas': entradas,
        'lembretes': lembretes,
    }
    return render(request, 'plantas/diario_planta.html', context)

@login_required
def adicionar_entrada_diario(request, planta_pk):
    """Adicionar entrada no diário"""
    planta = get_object_or_404(Planta, pk=planta_pk)
    if planta.autor != request.user:
        messages.error(request, 'Você não tem permissão para adicionar entradas nesta planta. 🔒')
        return redirect('detalhe_planta', pk=planta.pk)

    if request.method == 'POST':
        form = DiarioPlantaForm(request.POST, request.FILES)
        if form.is_valid():
            entrada = form.save(commit=False)
            entrada.planta = planta
            entrada.usuario = request.user
            entrada.save()
            messages.success(request, 'Entrada adicionada ao diário! 📔')
            return redirect('diario_planta', planta_pk=planta.pk)
    else:
        form = DiarioPlantaForm()

    return render(request, 'plantas/form_diario.html', {
        'form': form,
        'planta': planta,
        'titulo': f'Nova entrada no diário de {planta.nome}'
    })

# ===== SISTEMA DE LEMBRETES =====

@login_required
def listar_lembretes(request):
    """Listar lembretes do usuário"""
    lembretes = Lembrete.objects.filter(usuario=request.user, ativo=True).order_by('proxima_data')
    lembretes_vencidos = lembretes.filter(proxima_data__lt=timezone.now())

    context = {
        'lembretes': lembretes,
        'lembretes_vencidos': lembretes_vencidos,
    }
    return render(request, 'plantas/lembretes.html', context)

@login_required
def criar_lembrete(request, planta_pk=None):
    """Criar novo lembrete"""
    planta = None
    if planta_pk:
        planta = get_object_or_404(Planta, pk=planta_pk)
        if planta.autor != request.user:
            messages.error(request, 'Você não tem permissão para criar lembretes nesta planta. 🔒')
            return redirect('detalhe_planta', pk=planta.pk)

    if request.method == 'POST':
        form = LembreteForm(request.POST)
        if form.is_valid():
            lembrete = form.save(commit=False)
            lembrete.usuario = request.user
            if planta:
                lembrete.planta = planta
            lembrete.save()
            messages.success(request, 'Lembrete criado com sucesso! ⏰')
            return redirect('listar_lembretes')
    else:
        form = LembreteForm()
        if planta:
            form.fields['planta'].initial = planta

    return render(request, 'plantas/form_lembrete.html', {
        'form': form,
        'planta': planta,
        'titulo': 'Novo Lembrete'
    })

@login_required
@require_POST
def marcar_lembrete_feito(request, lembrete_pk):
    """Marcar lembrete como concluído"""
    lembrete = get_object_or_404(Lembrete, pk=lembrete_pk, usuario=request.user)
    lembrete.marcar_feito()
    messages.success(request, 'Lembrete marcado como concluído! ✅')
    return redirect('listar_lembretes')

# ===== SISTEMA DE MENSAGENS =====

@login_required
def listar_mensagens(request):
    """Listar mensagens recebidas"""
    mensagens = Mensagem.objects.filter(destinatario=request.user).order_by('-criada_em')
    nao_lidas = mensagens.filter(lida=False)

    context = {
        'mensagens': mensagens,
        'total_nao_lidas': nao_lidas.count(),
    }
    return render(request, 'plantas/mensagens.html', context)

@login_required
def enviar_mensagem(request, username=None):
    """Enviar mensagem"""
    destinatario = None
    if username:
        destinatario = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = MensagemForm(request.POST)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.remetente = request.user
            if destinatario:
                mensagem.destinatario = destinatario
            mensagem.save()
            messages.success(request, 'Mensagem enviada com sucesso! 📨')
            return redirect('listar_mensagens')
    else:
        form = MensagemForm()
        if destinatario:
            form.fields['destinatario'].initial = destinatario

    return render(request, 'plantas/form_mensagem.html', {
        'form': form,
        'destinatario': destinatario,
        'titulo': f'Enviar mensagem para {destinatario.username}' if destinatario else 'Nova Mensagem'
    })

@login_required
def ver_mensagem(request, mensagem_pk):
    """Ver detalhes da mensagem"""
    mensagem = get_object_or_404(Mensagem, pk=mensagem_pk, destinatario=request.user)

    if not mensagem.lida:
        mensagem.lida = True
        mensagem.save()

    return render(request, 'plantas/ver_mensagem.html', {
        'mensagem': mensagem,
    })

# ===== SISTEMA DE ENQUETES =====

@login_required
def listar_enquetes(request):
    """Listar enquetes ativas"""
    enquetes = Enquete.objects.filter(ativa=True).order_by('-criada_em')
    enquetes_participadas = VotoEnquete.objects.filter(usuario=request.user).values_list('opcao__enquete', flat=True)

    context = {
        'enquetes': enquetes,
        'enquetes_participadas': enquetes_participadas,
    }
    return render(request, 'plantas/enquetes.html', context)

@login_required
def criar_enquete(request):
    """Criar nova enquete"""
    if request.method == 'POST':
        form = EnqueteForm(request.POST)
        if form.is_valid():
            enquete = form.save(commit=False)
            enquete.autor = request.user
            enquete.save()

            # Criar opções
            opcao_texts = request.POST.getlist('opcoes')
            for texto in opcao_texts:
                if texto.strip():
                    OpcaoEnquete.objects.create(enquete=enquete, texto=texto.strip())

            messages.success(request, 'Enquete criada com sucesso! 📊')
            return redirect('listar_enquetes')
    else:
        form = EnqueteForm()

    return render(request, 'plantas/form_enquete.html', {
        'form': form,
        'titulo': 'Nova Enquete'
    })

@login_required
@require_POST
def votar_enquete(request, enquete_pk):
    """Votar em enquete"""
    enquete = get_object_or_404(Enquete, pk=enquete_pk, ativa=True)
    opcao_pk = request.POST.get('opcao')

    if not opcao_pk:
        messages.error(request, 'Selecione uma opção para votar.')
        return redirect('listar_enquetes')

    opcao = get_object_or_404(OpcaoEnquete, pk=opcao_pk, enquete=enquete)

    # Verificar se já votou
    if VotoEnquete.objects.filter(usuario=request.user, opcao__enquete=enquete).exists():
        messages.error(request, 'Você já votou nesta enquete.')
        return redirect('listar_enquetes')

    # Criar voto
    VotoEnquete.objects.create(usuario=request.user, opcao=opcao)
    messages.success(request, 'Voto registrado com sucesso! ✓')

    return redirect('listar_enquetes')

# ===== FEED E RANKING =====

@login_required
def feed_atividades(request):
    """Feed de atividades do usuário"""
    
    # Usuários que o user segue
    usuarios_seguindo = request.user.seguindo.values_list('seguindo', flat=True)
    
    # Plantas recentes de quem segue + próprias
    plantas_feed = Planta.objects.filter(
        Q(autor__in=usuarios_seguindo) | Q(autor=request.user)
    ).select_related('autor', 'autor__profile').prefetch_related(
        'likes', 'comentarios', 'favoritado_por'
    ).order_by('-criado_em')[:20]
    
    # Comentários recentes de quem segue
    comentarios_recentes = Comentario.objects.filter(
        autor__in=usuarios_seguindo
    ).select_related('autor', 'planta', 'autor__profile').order_by('-criado_em')[:10]
    
    # Estatísticas
    estatisticas = {
        'total_seguindo': request.user.seguindo.count(),
        'total_seguidores': request.user.seguidores.count(),
        'total_plantas': request.user.planta_set.count(),
        'total_likes_recebidos': LikePlanta.objects.filter(planta__autor=request.user).count(),
        'nivel_experiencia': request.user.profile.get_nivel_experiencia_display(),
    }
    
    context = {
        'plantas_feed': plantas_feed,
        'comentarios_recentes': comentarios_recentes,
        'estatisticas': estatisticas,
    }
    
    return render(request, 'plantas/feed.html', context)

@login_required
def ranking_jardineiros(request):
    """Ranking de jardineiros por pontuação"""
    
    usuarios_com_pontos = []
    
    for usuario in User.objects.all():
        pontos = 0
        
        # Pontuação
        pontos += usuario.planta_set.count() * 10
        pontos += LikePlanta.objects.filter(planta__autor=usuario).count() * 5
        pontos += usuario.comentario_set.count() * 3
        pontos += usuario.seguidores.count() * 15
        pontos += sum([ub.badge.pontos for ub in usuario.badges.all()])
        
        usuarios_com_pontos.append({
            'usuario': usuario,
            'pontos': pontos,
            'total_plantas': usuario.planta_set.count(),
            'total_likes': LikePlanta.objects.filter(planta__autor=usuario).count(),
            'total_seguidores': usuario.seguidores.count(),
            'badges': usuario.badges.all()[:5]
        })
    
    # Ordenar por pontos
    usuarios_com_pontos.sort(key=lambda x: x['pontos'], reverse=True)
    
    # Adicionar posição
    for idx, usuario_data in enumerate(usuarios_com_pontos, 1):
        usuario_data['posicao'] = idx
    
    # Paginação
    paginator = Paginator(usuarios_com_pontos, 20)
    page = request.GET.get('page', 1)
    usuarios_paginados = paginator.get_page(page)
    
    context = {
        'usuarios_ranking': usuarios_paginados,
        'minha_posicao': next(
            (u['posicao'] for u in usuarios_com_pontos if u['usuario'] == request.user),
            None
        )
    }
    
    return render(request, 'plantas/ranking.html', context)

# ===== DASHBOARD E ESTATÍSTICAS =====

@login_required
def dashboard_estatisticas(request):
    """Dashboard com estatísticas do usuário"""
    
    # Estatísticas gerais
    total_plantas = request.user.planta_set.count()
    total_comentarios = request.user.comentario_set.count()
    total_likes_recebidos = LikePlanta.objects.filter(planta__autor=request.user).count()
    total_likes_dados = LikePlanta.objects.filter(usuario=request.user).count()
    
    # Plantas por dificuldade
    plantas_por_dificuldade = request.user.planta_set.values('dificuldade').annotate(
        total=Count('id')
    ).order_by('dificuldade')
    
    # Evolução temporal (últimos 12 meses)
    hoje = timezone.now()
    doze_meses_atras = hoje - timedelta(days=365)
    
    plantas_por_mes = request.user.planta_set.filter(
        criado_em__gte=doze_meses_atras
    ).annotate(
        mes=TruncMonth('criado_em')
    ).values('mes').annotate(
        total=Count('id')
    ).order_by('mes')
    
    # Top 5 plantas mais curtidas
    plantas_mais_curtidas = request.user.planta_set.annotate(
        total_likes=Count('likes')
    ).order_by('-total_likes')[:5]
    
    # Badges conquistadas recentemente
    badges_recentes = request.user.badges.order_by('-concedida_em')[:8]
    
    # Taxa de engajamento
    if total_plantas > 0:
        taxa_engajamento = (total_likes_recebidos + total_comentarios) / total_plantas
    else:
        taxa_engajamento = 0
    
    context = {
        'total_plantas': total_plantas,
        'total_comentarios': total_comentarios,
        'total_likes_recebidos': total_likes_recebidos,
        'total_likes_dados': total_likes_dados,
        'plantas_por_dificuldade': plantas_por_dificuldade,
        'plantas_por_mes': plantas_por_mes,
        'plantas_mais_curtidas': plantas_mais_curtidas,
        'badges_recentes': badges_recentes,
        'taxa_engajamento': round(taxa_engajamento, 2),
        'total_seguidores': request.user.seguidores.count(),
        'total_seguindo': request.user.seguindo.count(),
    }
    
    return render(request, 'plantas/dashboard.html', context)

# ===== SISTEMA DE DENÚNCIAS =====

@login_required
def criar_denuncia(request, tipo, obj_id):
    """Criar denúncia"""
    context = {'tipo': tipo}
    
    if tipo == 'planta':
        obj = get_object_or_404(Planta, pk=obj_id)
        context['obj'] = obj
    elif tipo == 'comentario':
        obj = get_object_or_404(Comentario, pk=obj_id)
        context['obj'] = obj
    elif tipo == 'perfil':
        obj = get_object_or_404(User, pk=obj_id)
        context['obj'] = obj
    else:
        raise Http404("Tipo de denúncia inválido")
    
    if request.method == 'POST':
        form = DenunciaForm(request.POST)
        if form.is_valid():
            denuncia = form.save(commit=False)
            denuncia.denunciador = request.user
            
            if tipo == 'planta':
                denuncia.planta = obj
            elif tipo == 'comentario':
                denuncia.comentario = obj
            elif tipo == 'perfil':
                denuncia.perfil_reportado = obj
            
            denuncia.save()
            messages.success(request, 'Denúncia enviada. Obrigado por ajudar a manter a comunidade segura! 🚨')
            return redirect('listar_plantas')
    else:
        form = DenunciaForm()
    
    context['form'] = form
    return render(request, 'plantas/form_denuncia.html', context)

# ===== SISTEMA DE BUSCA =====

def buscar(request):
    """Busca inteligente"""
    query = request.GET.get('q', '')
    resultado_plantas = []
    resultado_usuarios = []
    
    if query:
        resultado_plantas = Planta.objects.filter(
            Q(nome__icontains=query) |
            Q(especie__icontains=query) |
            Q(descricao__icontains=query) |
            Q(autor__username__icontains=query)
        ).distinct().prefetch_related('likes')
        
        resultado_usuarios = User.objects.filter(
            Q(username__icontains=query) |
            Q(profile__bio__icontains=query)
        ).distinct()
    
    context = {
        'query': query,
        'plantas': resultado_plantas,
        'usuarios': resultado_usuarios,
    }
    return render(request, 'plantas/busca.html', context)

# ===== NOTIFICAÇÕES =====

@login_required
def listar_notificacoes(request):
    """Listar notificações do usuário"""
    notificacoes = request.user.notificacoes.all()
    nao_lidas = notificacoes.filter(lida=False)

    # Marcar como lida ao abrir
    if nao_lidas.exists():
        nao_lidas.update(lida=True)

    return render(request, 'plantas/notificacoes.html', {
        'notificacoes': notificacoes,
        'total_nao_lidas': nao_lidas.count()
    })

