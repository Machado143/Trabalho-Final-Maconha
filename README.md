# 🌿 Trabalho Final - Sistema de Plantas

> Uma rede social colaborativa para amantes de jardinagem compartilharem plantas, experiências de cultivo e dicas com a comunidade.

![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![REST](https://img.shields.io/badge/REST_API-Django_REST-ff1709?style=for-the-badge&logo=django&logoColor=white)

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [API REST](#-api-rest)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Testes](#-testes)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🌱 Sobre o Projeto

**Sistema de Plantas** é uma aplicação web fullstack desenvolvida com Django que permite aos usuários:

- 📸 Cadastrar e compartilhar suas plantas com fotos
- 💬 Comentar e trocar experiências sobre cultivo
- 🔐 Gerenciar suas próprias publicações (CRUD completo)
- 🌐 Acessar dados via API REST para integração externa
- 👥 Criar uma comunidade de jardineiros

Este projeto foi desenvolvido como trabalho final da disciplina de **Desenvolvimento Web** e implementa todos os conceitos de autenticação, autorização, CRUD e boas práticas de desenvolvimento Django.

---

## ✨ Funcionalidades

### 🔒 Sistema de Autenticação
- ✅ Cadastro de novos usuários
- ✅ Login/Logout seguro
- ✅ Controle de permissões (usuários só editam/excluem suas próprias plantas)

### 🌿 Gerenciamento de Plantas (CRUD)
- ✅ **Criar:** Cadastre plantas com nome, espécie, dificuldade, necessidades e foto
- ✅ **Visualizar:** Explore o catálogo completo de plantas da comunidade
- ✅ **Editar:** Atualize informações das suas plantas
- ✅ **Excluir:** Remova plantas que você cadastrou

### 💬 Sistema de Comentários
- ✅ Deixe comentários com dicas e experiências
- ✅ Visualize feedback da comunidade em tempo real

### 🔌 API REST
- ✅ Endpoints completos para integração externa
- ✅ Paginação automática
- ✅ Suporte a CORS para aplicações frontend

---

## 🛠 Tecnologias Utilizadas

### Backend
- **Django 5.2** - Framework web Python
- **Django REST Framework** - API RESTful
- **Pillow** - Processamento de imagens
- **SQLite** - Banco de dados (desenvolvimento)

### Frontend
- **Bootstrap 5.3** - Framework CSS responsivo
- **django-bootstrap5** - Integração Django + Bootstrap
- **Vue.js 3** - Frontend da API (opcional)

### Ferramentas
- **pytest** - Framework de testes
- **CORS Headers** - Suporte a requisições cross-origin

---

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.9+** → [Download](https://www.python.org/downloads/)
- **pip** (geralmente já vem com Python)
- **Git** → [Download](https://git-scm.com/)

---

## 🚀 Instalação

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/trabalho-final.git
cd trabalho-final
```

### 2️⃣ Crie um ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Você verá `(.venv)` no início da linha do terminal.

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure o banco de dados

```bash
python manage.py migrate
```

### 5️⃣ Crie um superusuário (admin)

```bash
python manage.py createsuperuser
```

Responda as perguntas:
```
Username: admin
Email: admin@example.com
Password: ********
```

### 6️⃣ Inicie o servidor

```bash
python manage.py runserver
```

✅ **Pronto!** Acesse: http://127.0.0.1:8000

---

## 💻 Como Usar

### 🌐 Acessando a Aplicação

| Área | URL | Descrição |
|------|-----|-----------|
| **Home** | http://127.0.0.1:8000 | Página inicial |
| **Catálogo** | http://127.0.0.1:8000/plantas/ | Lista de plantas |
| **Admin** | http://127.0.0.1:8000/admin | Painel administrativo |
| **API** | http://127.0.0.1:8000/api/plantas/ | Endpoint REST |

### 📝 Cadastrando uma Planta

1. Faça login na aplicação
2. Clique em **"+ Nova Planta"**
3. Preencha os campos:
   - Nome da planta
   - Espécie científica
   - Dificuldade (Fácil/Média/Difícil)
   - Necessidades de água e luz
   - Descrição detalhada
   - Foto (opcional)
4. Clique em **"Publicar Planta"**

### ✏️ Editando/Excluindo

- Acesse os detalhes da planta
- Botões de **Editar** e **Excluir** aparecem apenas para o autor
- Clique no botão desejado

### 💬 Comentando

1. Acesse os detalhes de qualquer planta
2. Clique em **"+ Deixar um Comentário"**
3. Escreva sua experiência
4. Clique em **"Publicar Comentário"**

---

## 🔌 API REST

### Listar Todas as Plantas

```bash
GET /api/plantas/
```

**Resposta:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "nome": "ALOE VERA",
      "especie": "Aloe barbadensis",
      "dificuldade": "F",
      "necessidade_agua": "Baixa",
      "necessidade_luz": "Sol pleno",
      "descricao": "Planta medicinal resistente",
      "imagem": "http://127.0.0.1:8000/media/plantas/aloe.jpg",
      "autor_nome": "jardineiro1",
      "criado_em": "2025-12-01T10:30:00Z",
      "comentarios": [
        {
          "id": 1,
          "autor_nome": "usuario2",
          "conteudo": "Adorei! Cresce muito rápido.",
          "criado_em": "2025-12-01T14:20:00Z"
        }
      ]
    }
  ]
}
```

### Detalhes de uma Planta

```bash
GET /api/plantas/{id}/
```

### Criar Nova Planta (Requer Autenticação)

```bash
POST /api/plantas/
Content-Type: application/json

{
  "nome": "Cacto",
  "especie": "Cactaceae",
  "dificuldade": "F",
  "necessidade_agua": "Muito baixa",
  "necessidade_luz": "Sol direto",
  "descricao": "Planta desértica"
}
```

### Frontend de Exemplo (Vue.js)

Abra `api_frontend/index.html` no navegador para ver a API em ação com Vue.js.

---

## 📁 Estrutura do Projeto

```
trabalho-final-maconha/
├── 📂 trabalho_final/            # Configurações do projeto
│   ├── settings.py               # Configurações Django
│   ├── urls.py                   # Rotas principais
│   ├── wsgi.py                   # Deploy WSGI
│   └── asgi.py                   # Deploy ASGI
│
├── 📂 plantas/                   # App principal
│   ├── models.py                 # Modelos (Planta, Comentário)
│   ├── views.py                  # Views do frontend
│   ├── viewsets.py               # ViewSets da API
│   ├── serializers.py            # Serializers REST
│   ├── forms.py                  # Formulários Django
│   ├── urls.py                   # Rotas do app
│   ├── admin.py                  # Painel admin
│   ├── tests.py                  # Testes unitários
│   ├── 📂 templates/             # Templates HTML
│   └── 📂 migrations/            # Migrações do banco
│
├── 📂 templates/                 # Templates globais
│   ├── base.html                 # Layout base
│   └── 📂 registration/          # Templates de auth
│
├── 📂 static/                    # Arquivos estáticos
│   └── 📂 css/                   # Estilos customizados
│
├── 📂 media/                     # Uploads de usuários
│   └── 📂 plantas/               # Fotos das plantas
│
├── 📂 api_frontend/              # Frontend Vue.js (demo)
│   ├── index.html
│   └── script.js
│
├── manage.py                     # CLI do Django
├── requirements.txt              # Dependências Python
├── pytest.ini                    # Configuração de testes
├── db.sqlite3                    # Banco de dados
└── README.md                     # Este arquivo
```

---

## 🧪 Testes

### Executar todos os testes

```bash
python manage.py test
```

### Testes com pytest (mais verboso)

```bash
pip install pytest pytest-django
pytest -v
```

### Cobertura dos Testes

O projeto inclui testes para:
- ✅ Modelos (criação, validação, relacionamentos)
- ✅ Views (listagem, criação, edição, exclusão)
- ✅ Formulários (validação customizada)
- ✅ API REST (endpoints, permissões)
- ✅ Autenticação (login, logout, permissões)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga os passos:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

### Padrões de Código

- Siga a [PEP 8](https://pep8.org/) para código Python
- Use nomes descritivos para variáveis e funções
- Adicione docstrings em funções complexas
- Escreva testes para novas funcionalidades

---

## 🐛 Problemas Comuns

### Erro: "ModuleNotFoundError: No module named 'django'"

**Solução:** Ative o ambiente virtual
```bash
# Windows
.\.venv\Scripts\Activate

# Mac/Linux
source .venv/bin/activate
```

### Erro: "Port 8000 is already in use"

**Solução:** Use outra porta
```bash
python manage.py runserver 8001
```

### Imagens não aparecem

**Solução:** Verifique se `DEBUG = True` em `settings.py` e se a pasta `media/` existe.

### CSS não carrega

**Solução:** Execute
```bash
python manage.py collectstatic
```

---

## 🔐 Segurança para Produção

⚠️ **Antes de fazer deploy:**

1. **Altere `SECRET_KEY`** em `settings.py`
2. **Defina `DEBUG = False`**
3. **Configure `ALLOWED_HOSTS`**
```python
ALLOWED_HOSTS = ['seudominio.com', 'www.seudominio.com']
```
4. **Use banco de dados PostgreSQL**
5. **Configure variáveis de ambiente** para credenciais
6. **Use serviço de arquivos** (AWS S3, Cloudinary) para mídia
7. **Configure HTTPS**

---

## 📚 Referências e Documentação

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [PEP 8 Style Guide](https://pep8.org/)

---

## 📝 Comandos Úteis

| Comando | Descrição |
|---------|-----------|
| `python manage.py runserver` | Inicia servidor de desenvolvimento |
| `python manage.py migrate` | Aplica migrações no banco |
| `python manage.py makemigrations` | Cria novas migrações |
| `python manage.py createsuperuser` | Cria usuário admin |
| `python manage.py test` | Executa testes |
| `python manage.py shell` | Abre shell interativo do Django |
| `python manage.py collectstatic` | Coleta arquivos estáticos |



