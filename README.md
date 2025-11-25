# 🌿 Pai do Verde

Um site comunitário para jardineiros compartilharem plantas, dicas de cultivo e experiências. Feito com Django + REST API + Vue.js.

---

## 🎯 O que é?

Um sistema web onde você pode:
- ✅ Cadastrar suas plantas
- ✅ Ver plantas cadastradas por outros usuários
- ✅ Deixar comentários e dicas
- ✅ Acessar via API REST

---

## 📋 Requisitos

Você precisa ter instalado:
- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **Git** (opcional, mas recomendado)

---

## 🚀 Instalação Passo a Passo

### 1️⃣ Clone ou baixe o projeto

```bash
git clone https://github.com/seu-usuario/Pai_do_Verde.git
cd Pai_do_Verde
```

### 2️⃣ Crie um ambiente virtual

**No Windows (PowerShell):**
```bash
python -m venv venv
.\venv\Scripts\Activate
```

**No Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Após rodar esses comandos, você verá `(venv)` no começo da linha do terminal.

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

Isso vai instalar:
- Django
- Django REST Framework
- Pillow (para fotos)
- Bootstrap 5
- CORS (para API)

---

## 🔧 Configuração do Banco de Dados

### 1️⃣ Crie as tabelas

```bash
python manage.py migrate
```

### 2️⃣ Crie um usuário admin (super usuário)

```bash
python manage.py createsuperuser
```

Responda as perguntas:
```
Nome de usuário: seu_nome
Email: seu_email@example.com
Senha: uma_senha_segura
```

---

## ▶️ Rodando o Servidor

```bash
python manage.py runserver
```

Pronto! Abra seu navegador e acesse:

- **Site principal:** http://127.0.0.1:8000
- **Painel admin:** http://127.0.0.1:8000/admin

**Login no admin:**
- Usuário: o que você criou no `createsuperuser`
- Senha: a senha que você criou

---

## 👤 Criar Usuários para Teste

### Opção 1: Via Painel Admin
1. Acesse http://127.0.0.1:8000/admin
2. Clique em "Users" → "Add User"
3. Preencha os dados
4. Clique em "Save"

### Opção 2: Via Site
1. Clique em "Cadastrar" na página inicial
2. Escolha um nome de usuário e senha
3. Pronto!

---

## 📱 Como Usar o Site

### Listar Plantas
1. Acesse http://127.0.0.1:8000/plantas/
2. Veja todas as plantas cadastradas
3. Clique em "Ver Detalhes" para mais informações

### Cadastrar uma Nova Planta
1. Faça login (canto superior direito)
2. Clique em "+ Nova Planta"
3. Preencha:
   - Nome da planta
   - Espécie científica
   - Nível de dificuldade (Fácil, Médio, Difícil)
   - Necessidade de água (ex: "Pouca", "Moderada")
   - Necessidade de luz (ex: "Sol pleno", "Sombra")
   - Descrição
   - Foto (opcional)
4. Clique em "Publicar"

### Editar ou Excluir Planta
1. Vá aos detalhes da planta que você criou
2. Se for sua planta, aparecem botões "Editar" e "Excluir"
3. Clique no botão desejado

### Deixar Comentários
1. Na página de detalhes de uma planta
2. Clique em "+ Deixar um Comentário"
3. Escreva sua experiência
4. Clique em "Publicar Comentário"

---

## 🔗 API REST

Se quiser usar a API em aplicações externas:

### Listar todas as plantas

```bash
curl http://127.0.0.1:8000/api/plantas/
```

**Resposta (JSON):**
```json
{
  "count": 5,
  "next": null,
  "results": [
    {
      "id": 1,
      "nome": "Aloe Vera",
      "especie": "Aloe barbadensis",
      "dificuldade": "F",
      "autor_nome": "jardineiro1",
      "comentarios": [...]
    }
  ]
}
```

### Detalhes de uma planta específica

```bash
curl http://127.0.0.1:8000/api/plantas/1/
```

---

## 🧪 Rodando Testes

```bash
python manage.py test
```

Ou com mais detalhes:

```bash
python -m pytest -v
```

---

## 📂 Estrutura do Projeto

```
Pai_do_Verde/
├── Pai_do_Verde/          # Configurações do projeto
│   ├── settings.py        # Configurações (banco, apps, etc)
│   ├── urls.py            # Rotas principais
│   └── wsgi.py
├── plantas/               # Aplicação principal
│   ├── models.py          # Banco de dados (Planta, Comentario)
│   ├── views.py           # Lógica das páginas
│   ├── forms.py           # Formulários
│   ├── serializers.py     # API REST
│   ├── templates/         # HTML
│   └── migrations/        # Histórico do banco de dados
├── templates/             # HTML globais (login, base)
├── static/                # CSS, JS, imagens
├── api_frontend/          # Frontend Vue.js para API
├── manage.py              # Comando principal do Django
└── requirements.txt       # Dependências Python
```

---

## 🐛 Problemas Comuns

### ❌ "ModuleNotFoundError: No module named 'django'"
**Solução:** Você esqueceu de ativar o ambiente virtual. Execute:
```bash
# Windows
.\venv\Scripts\Activate
# Mac/Linux
source venv/bin/activate
```

### ❌ "Port 8000 is already in use"
**Solução:** Outra aplicação está usando a porta 8000. Use:
```bash
python manage.py runserver 8001
```

### ❌ Fotos não aparecem
**Solução:** Certifique-se de que:
1. A pasta `media/` existe
2. Você está no modo `DEBUG = True` em `settings.py`

### ❌ CSS não aparece
**Solução:** Execute:
```bash
python manage.py collectstatic
```

---

## 📝 Comandos Úteis

| Comando | O que faz |
|---------|-----------|
| `python manage.py runserver` | Inicia o servidor |
| `python manage.py migrate` | Aplica mudanças no banco |
| `python manage.py makemigrations` | Prepara mudanças no banco |
| `python manage.py createsuperuser` | Cria admin |
| `python manage.py test` | Roda testes |
| `python manage.py shell` | Terminal Python interativo |

---

## 🔐 Segurança para Produção

⚠️ **NÃO coloque esse projeto em produção assim!**

Antes de subir para a internet:
1. Mude `DEBUG = False` em `settings.py`
2. Gere uma nova `SECRET_KEY` aleatória
3. Configure `ALLOWED_HOSTS`
4. Use um banco de dados real (PostgreSQL)
5. Configure variáveis de ambiente

---

## 👨‍💻 Desenvolvendo

### Criar uma nova funcionalidade

1. Faça as mudanças no código
2. Se alterou modelos, execute:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Teste tudo:
   ```bash
   python manage.py test
   ```

### Adicionar dependências

1. Instale com pip:
   ```bash
   pip install nome_do_pacote
   ```
2. Atualize `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```

---

## 📚 Referências

- [Documentação Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Bootstrap 5](https://getbootstrap.com/)
- [Vue.js 3](https://vuejs.org/)

---

## 📄 Licença

Este projeto está livre para usar e modificar.

---

## ❓ Dúvidas?

Se tiver problemas, verifique:
1. Se o `venv` está ativado
2. Se executou `migrate` e `createsuperuser`
3. Se está rodando `python manage.py runserver`
4. Se a porta 8000 não está ocupada

**Boa sorte, jardineiro(a)! 🌱**
