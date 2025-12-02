from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Planta, Comentario
from .forms import PlantaForm, ComentarioForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import DenunciaForm
from django.contrib.auth.models import User
from .models import LikePlanta, FavoritoPlanta, Seguir
from .forms import UserProfileForm
from django.http import Http404
from django.db.models import Count
from django.db.models import Prefetch
from .models import UserProfile
from .models import Denuncia
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



def index(request):
    return render(request, 'plantas/index.html', {'nome': 'Jardineiro'})

def listar_plantas(request):
    plantas = Planta.objects.all().order_by('id').prefetch_related('comentarios')
    return render(request, 'plantas/lista_plantas.html', {'plantas': plantas})

def detalhe_planta(request, pk):
    planta = get_object_or_404(Planta.objects.prefetch_related('comentarios'), pk=pk)
    return render(request, 'plantas/detalhe_planta.html', {'planta': planta})

# CORRIGIR: plantas/views.py

@login_required
def criar_planta(request):
    if request.method == 'POST':
        form = PlantaForm(request.POST, request.FILES)
        if form.is_valid():
            planta = form.save(commit=False)
            planta.autor = request.user
            planta.save()
            messages.success(request, 'Planta cadastrada com sucesso!')
            return redirect('listar_plantas')
    else:
        form = PlantaForm()
    
    # ADICIONADO: passar planta como None quando criando
    return render(request, 'plantas/form_planta.html', {
        'form': form, 
        'titulo': 'Nova Planta',
        'planta': None  # ← ADICIONAR ISTO
    })

@login_required
def editar_planta(request, pk):
    planta = get_object_or_404(Planta, pk=pk, autor=request.user)
    if request.method == 'POST':
        form = PlantaForm(request.POST, request.FILES, instance=planta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Planta atualizada!')
            return redirect('detalhe_planta', pk=planta.pk)
    else:
        form = PlantaForm(instance=planta)
    
    # JÁ passa planta normalmente
    return render(request, 'plantas/form_planta.html', {
        'form': form, 
        'titulo': 'Editar Planta',
        'planta': planta  # ← JÁ EXISTE
    })
@login_required
def excluir_planta(request, pk):
    planta = get_object_or_404(Planta, pk=pk, autor=request.user)
    if request.method == 'POST':
        planta.delete()
        messages.success(request, 'Planta excluída!')
        return redirect('listar_plantas')
    return render(request, 'plantas/confirmar_exclusao.html', {'planta': planta})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('listar_plantas')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def criar_comentario(request, planta_pk):
    planta = get_object_or_404(Planta, pk=planta_pk)
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.planta = planta
            comentario.autor = request.user
            comentario.save()
            messages.success(request, 'Comentário adicionado!')
            return redirect('detalhe_planta', pk=planta.pk)
    else:
        form = ComentarioForm()
    
    return render(request, 'plantas/form_comentario.html', {
        'form': form, 
        'planta': planta,
        'titulo': f'Comentar sobre {planta.nome}'
    })

@login_required
@require_POST
def toggle_like(request, planta_pk):
    """Like/Unlike via AJAX ou POST tradicional"""
    planta = get_object_or_404(Planta, pk=planta_pk)
    like, created = LikePlanta.objects.get_or_create(planta=planta, usuario=request.user)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    # Para AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': planta.likes.count()
        })
    
    # Para POST tradicional
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
    """Seguir/Deixar de seguir um usuário"""
    usuario_target = get_object_or_404(User, username=username)
    
    if usuario_target == request.user:
        messages.error(request, "Você não pode seguir a si mesmo!")
        return redirect('ver_perfil', username=username)
    
    seguir, created = Seguir.objects.get_or_create(seguidor=request.user, seguindo=usuario_target)
    
    if not created:
        seguir.delete()
        messages.success(request, f'Você deixou de seguir {username}')
    else:
        messages.success(request, f'Você está seguindo {username}')
    
    return redirect('ver_perfil', username=username)

def ver_perfil(request, username):
    """Visualizar perfil de um usuário"""
    usuario = get_object_or_404(User, username=username)
    plantas = usuario.planta_set.all().order_by('-criado_em')
    
    # Verificar se o usuário logado segue este perfil
    esta_seguindo = False
    if request.user.is_authenticated:
        esta_seguindo = Seguir.objects.filter(seguidor=request.user, seguindo=usuario).exists()
    
    context = {
        'usuario_perfil': usuario,
        'plantas': plantas,
        'esta_seguindo': esta_seguindo,
        'total_seguidores': usuario.seguidores.count(),
        'total_seguindo': usuario.seguindo.count(),
    }
    return render(request, 'plantas/perfil.html', context)

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('ver_perfil', username=request.user.username)
    else:
        profile_form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'plantas/editar_perfil.html', {
        'profile_form': profile_form
    })
@login_required
def criar_denuncia(request, tipo, obj_id):
    """
    Criar denúncia: tipo pode ser 'planta', 'comentario' ou 'perfil'
    """
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
            messages.success(request, 'Denúncia enviada. Obrigado por ajudar a manter a comunidade segura!')
            return redirect('listar_plantas')
    else:
        form = DenunciaForm()
    
    context['form'] = form
    return render(request, 'plantas/form_denuncia.html', context)

def buscar(request):
    """Busca inteligente em plantas e usuários"""
    query = request.GET.get('q', '')
    resultado_plantas = []
    resultado_usuarios = []
    
    if query:
        # Busca em nome, espécie, descrição da planta
        resultado_plantas = Planta.objects.filter(
            Q(nome__icontains=query) |
            Q(especie__icontains=query) |
            Q(descricao__icontains=query) |
            Q(autor__username__icontains=query)
        ).distinct().prefetch_related('likes')
        
        # Busca em nome de usuário e bio do perfil
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

@login_required
def listar_notificacoes(request):
    notificacoes = request.user.notificacoes.all()
    nao_lidas = notificacoes.filter(lida=False)

    # Marcar como lida ao abrir
    if nao_lidas.exists():
        nao_lidas.update(lida=True)

    return render(request, 'plantas/notificacoes.html', {
        'notificacoes': notificacoes,
        'total_nao_lidas': nao_lidas.count()
    })  