from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Planta, Comentario
from .forms import PlantaForm, ComentarioForm

def index(request):
    return render(request, 'plantas/index.html', {'nome': 'Jardineiro'})

def listar_plantas(request):
    plantas = Planta.objects.all().prefetch_related('comentarios')
    return render(request, 'plantas/lista_plantas.html', {'plantas': plantas})

def detalhe_planta(request, pk):
    planta = get_object_or_404(Planta.objects.prefetch_related('comentarios'), pk=pk)
    return render(request, 'plantas/detalhe_planta.html', {'planta': planta})

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
    
    return render(request, 'plantas/form_planta.html', {'form': form, 'titulo': 'Nova Planta'})

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
    
    return render(request, 'plantas/form_planta.html', {'form': form, 'titulo': 'Editar Planta'})

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