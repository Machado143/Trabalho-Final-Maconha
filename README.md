# GreenThumb - Catálogo de Plantas 🌱

Sistema CRUD completo para gerenciamento de catálogo de plantas com dicas de cultivo.

## 📋 Descrição

O **GreenThumb** é uma aplicação Django que permite cadastrar, visualizar, atualizar e remover plantas de um catálogo. Cada planta contém informações detalhadas sobre cuidados necessários como:
- Nível de dificuldade
- Necessidade de luz
- Frequência de rega
- Faixa de temperatura ideal
- Tipo de solo
- Toxicidade para pets
- Dicas de cultivo

## 🚀 Estrutura do Projeto

```
greenthumb/
├── plantas/                  # App principal
│   ├── models.py            # Model Planta com todos os campos
│   ├── views.py             # Views do CRUD completo
│   ├── forms.py             # Formulários para criar/editar
│   ├── urls.py              # Rotas da aplicação
│   ├── admin.py             # Interface administrativa
│   ├── tests.py             # Testes unitários completos
│   └── templates/
│       └── plantas/
│           ├── listar_plantas.html
│           ├── detalhe_planta.html
│           ├── form_planta.html
│           └── deletar_planta.html
└── greenthumb/              # Configurações do projeto
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## 🛠️ Instalação e Configuração

### 1. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 2. Instalar Django
```bash
pip install django
```

### 3. Criar o projeto Django
```bash
django-admin startproject greenthumb .
python manage.py startapp plantas
```

### 4. Configurar settings.py
Adicione 'plantas' em INSTALLED_APPS:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'plantas',  # Adicionar esta linha
]
```

### 5. Copiar os arquivos fornecidos
- Copie o conteúdo de `models.py` para `plantas/models.py`
- Copie o conteúdo de `tests.py` para `plantas/tests.py`
- Copie o conteúdo de `views.py` para `plantas/views.py`
- Copie o conteúdo de `forms.py` para `plantas/forms.py`
- Copie o conteúdo de `urls.py` para `plantas/urls.py`
- Copie o conteúdo de `admin.py` para `plantas/admin.py`

### 6. Configurar URLs principais
Edite `greenthumb/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('plantas.urls')),
]
```

### 7. Criar migrações e banco de dados
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Criar superusuário (para acessar o admin)
```bash
python manage.py createsuperuser
```

### 9. Executar o servidor
```bash
python manage.py runserver
```

## ✅ Executar os Testes

Execute todos os testes do model:
```bash
python manage.py test plantas
```

Execute um teste específico:
```bash
python manage.py test plantas.tests.PlantaModelTest.test_criacao_planta
```

Execute com verbosidade:
```bash
python manage.py test plantas --verbosity=2
```

## 📊 Funcionalidades CRUD

### CREATE (Criar)
- **URL:** `/planta/nova/`
- **View:** `criar_planta`
- **Método:** POST
- Formulário completo para cadastrar nova planta

### READ (Ler)
- **Listar todas:** `/`
- **Ver detalhes:** `/planta/<id>/`
- **Views:** `listar_plantas`, `detalhe_planta`
- Filtros por dificuldade e necessidade de luz

### UPDATE (Atualizar)
- **URL:** `/planta/<id>/editar/`
- **View:** `editar_planta`
- **Método:** POST
- Formulário pré-preenchido com dados da planta

### DELETE (Deletar)
- **URL:** `/planta/<id>/deletar/`
- **View:** `deletar_planta`
- **Método:** POST
- Usa soft delete (marca como inativa)

## 🧪 Cobertura dos Testes

Os testes incluem:
- ✅ Criação de plantas
- ✅ Validação de campos obrigatórios
- ✅ Validação de temperatura (min/max)
- ✅ Métodos customizados do model
- ✅ Ordenação alfabética
- ✅ Datas automáticas (cadastro/atualização)
- ✅ Todas as operações CRUD
- ✅ Soft delete
- ✅ Valores padrão dos campos

## 🎯 Exemplo de Uso

### Criar uma planta via código:
```python
from plantas.models import Planta

planta = Planta.objects.create(
    nome_comum="Suculenta Jade",
    nome_cientifico="Crassula ovata",
    descricao="Planta suculenta de fácil cultivo",
    dificuldade='facil',
    necessidade_luz='alta',
    frequencia_rega='quinzenal',
    temperatura_min=10,
    temperatura_max=30,
    tipo_solo="bem drenado com areia",
    toxica_pets=False
)
```

### Listar plantas por dificuldade:
```python
plantas_faceis = Planta.objects.filter(dificuldade='facil')
```

### Verificar cuidados especiais:
```python
if planta.requer_cuidados_especiais():
    print("Esta planta precisa de atenção diária!")
```

## 🔐 Acessar o Admin

1. Acesse: `http://127.0.0.1:8000/admin/`
2. Use as credenciais do superusuário criado
3. Gerencie plantas através da interface administrativa

## 📝 Notas Importantes

- O campo `ativa` usa soft delete - plantas não são removidas do banco
- Temperaturas validadas entre -10°C e 50°C
- Altura em centímetros com 2 casas decimais
- Ordenação padrão por nome comum
- Índices criados para otimizar buscas por nome e dificuldade

## 🤝 Contribuindo

Para adicionar novas funcionalidades:
1. Adicione novos campos em `models.py`
2. Crie migrações: `python manage.py makemigrations`
3. Aplique migrações: `python manage.py migrate`
4. Adicione testes em `tests.py`
5. Execute os testes: `python manage.py test`

## 📄 Licença

Projeto educacional - livre para uso e modificação.
