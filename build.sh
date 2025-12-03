#!/bin/bash
set -o errexit  # Para execução se houver erro

echo "🚀 Iniciando build do Pai do Verde..."

# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências
echo "📦 Instalando dependências..."
python -m pip install -r requirements.txt

# Coletar arquivos estáticos
echo "📂 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Executar migrações
echo "🗄️ Aplicando migrações do banco de dados..."
python manage.py migrate --noinput

# Criar superusuário (apenas se não existir)
echo "👤 Verificando superusuário..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@paidoverde.com', 'Admin123!')
    print('✅ Superusuário criado: admin / Admin123!')
else:
    print('ℹ️ Superusuário já existe')
EOF

echo "✅ Build concluído com sucesso!"