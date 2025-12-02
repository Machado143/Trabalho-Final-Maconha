# 🌿 **Pai do Verde** – Rede Social de Plantas  
**Versão 2.0** ✨ *(com deploy para o ar!)*

![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Render](https://img.shields.io/badge/Deployed-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

---

## 📋 Índice

- [Sobre](#sobre)
- [Funcionalidades 2.0](#funcionalidades-20)
- [Tecnologias](#tecnologias)
- [Como rodar localmente](#como-rodar-localmente)
- [Deploy no Render (grátis)](#deploy-no-render-grátis)
- [API REST](#api-rest)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Testes](#testes)
- [Contribuindo](#contribuindo)
- [Comandos úteis](#comandos-úteis)

---

## 🌱 Sobre

**Pai do Verde** é uma rede social colaborativa onde jardineiros compartilham plantas, dicas e conquistas.  
Desenvolvida como **Trabalho Final de Desenvolvimento Web**, agora com **sistema de notificações**, **badges**, **seguir usuários** e **deploy na nuvem**.

---

## ✨ Funcionalidades 2.0

| Área | Funcionalidades |
|------|----------------|
| 🔐 **Autenticação** | Cadastro, login, logout, perfil completo com avatar |
| 🌿 **Plantas** | CRUD completo, curtidas, favoritos, comentários |
| 👥 **Rede Social** | Seguir usuários, feed de atividades, conquistas (badges) |
| 📬 **Notificações** | Like, comentário, nova conquista – tudo na caixa de mensagens |
| 🔍 **Busca Inteligente** | Por nome, espécie, autor ou palavra-chave |
| 🏆 **Gamificação** | Ganhe badges ao postar, comentar ou receber likes |
| 🌐 **API REST** | Endpoints completos com paginação e CORS |
| 📱 **Responsivo** | Bootstrap 5.3 + Vue.js 3 (demo) |
| 🚀 **Deploy** | Um clique no Render (grátis) |

---

## 🛠 Tecnologias

- **Backend:** Django 5.2, Django REST Framework, SQLite (ou PostgreSQL)
- **Frontend:** Bootstrap 5.3, Vue.js 3 (demo), ícones e gradientes modernos
- **Deploy:** Render, WhiteNoise, Gunicorn, variáveis de ambiente
- **Dev:** pytest, Git, Python 3.9+

---

## 🚀 Como rodar localmente

### 1. Clone e entre na pasta
```bash
git clone https://github.com/seu-usuario/pai-do-verde.git
cd pai-do-verde
```

### 2. Ambiente virtual
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Banco de dados e superusuário
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Rode o servidor
```bash
python manage.py runserver
```
Acesse: http://127.0.0.1:8000

---

## 🌐 Deploy no Render (grátis)

### 1. Push no GitHub
```bash
git add .
git commit -m "v2.0 pronta para o ar"
git push origin main
```

### 2. Render
- Login com GitHub em [https://render.com](https://render.com)
- **New → Web Service**
- Escolha o repositório
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn trabalho_final.wsgi:application`
- **Environment Variables (caso use PostgreSQL):**
  ```
  DATABASE_URL=sqlite:///db.sqlite3
  SECRET_KEY=sua-chave-secreta
  DEBUG=False
  ```
- **Create Web Service** → em 3 minutos estará no ar!

### 3. Arquivos necessários (já estão no repo)
- `render.yaml`
- `build.sh` (chmod +x)
- `requirements.txt` com `whitenoise` e `gunicorn`

---

## 🔌 API REST

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/plantas/` | Listar plantas (paginado) |
| POST | `/api/plantas/` | Criar planta (autenticado) |
| GET | `/api/plantas/{id}/` | Detalhar planta |
| PUT | `/api/plantas/{id}/` | Atualizar (dono) |
| DELETE | `/api/plantas/{id}/` | Excluir (dono) |

**Exemplo de resposta:**
```json
{
  "id": 1,
  "nome": "Aloe Vera",
  "especie": "Aloe barbadensis",
  "dificuldade": "F",
  "imagem": "https://seu-app.onrender.com/media/plantas/aloe.jpg",
  "autor_nome": "jardineiro1",
  "comentarios": [...],
  "likes_count": 7
}
```

---

## 📁 Estrutura do Projeto (resumida)

```
pai-do-verde/
├── trabalho_final/        # config Django
├── plantas/               # app principal
│   ├── models.py          # Planta, Comentário, Perfil, Like, Seguir, Badge...
│   ├── views.py           # CRUD + notificações
│   ├── signals.py         # badges & notificações automáticas
│   └── templates/         # HTML (Bootstrap 5.3)
├── templates/             # base.html, auth
├── static/                # CSS custom (global.css)
├── media/                 # uploads
├── api_frontend/          # demo Vue.js 3
├── requirements.txt
├── render.yaml
├── build.sh
└── README.md
```

---

## 🧪 Testes

```bash
python manage.py test
# ou
pytest -v
```

Cobertura: modelos, views, forms, API, permissões, sinais.

---

## 🤝 Contribuindo

1. Fork o projeto
2. Branch: `git checkout -b feature/nova-func`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-func`
5. Pull Request 🎉

---

## 📝 Comandos úteis

| Comando | Descrição |
|---------|-----------|
| `python manage.py runserver` | rodar local |
| `python manage.py migrate` | aplicar migrações |
| `python manage.py collectstatic` | preparar estáticos |
| `render shell` + `createsuperuser` | criar admin no Render |



