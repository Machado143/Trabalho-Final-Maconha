from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'plantas/index.html', {'nome': 'Jardineiro'})

def listar_plantas(request):
    plantas = Planta.objects.all().prefetch_related('dicas')
    return render(request, 'plantas/lista_plantas.html', {'plantas': plantas})