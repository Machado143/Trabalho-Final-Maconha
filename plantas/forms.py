from django import forms
from django.contrib.auth.models import User
from .models import (
    Planta, Comentario, UserProfile, Denuncia,
    Colecao, DiarioPlanta, Lembrete, Mensagem, 
    Enquete, OpcaoEnquete
)
from django.utils import timezone

# ===== FORMS DE PLANTAS =====

class PlantaForm(forms.ModelForm):
    """Formulário para criar/editar plantas"""
    
    class Meta:
        model = Planta
        fields = ['nome', 'especie', 'dificuldade', 'necessidade_agua', 'necessidade_luz', 'descricao', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da planta'
            }),
            'especie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Espécie científica'
            }),
            'dificuldade': forms.Select(attrs={'class': 'form-select'}),
            'necessidade_agua': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Baixa, Moderada, Alta'
            }),
            'necessidade_luz': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Sol pleno, Sombra parcial, Luz filtrada'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva a planta, dicas de cultivo, curiosidades...'
            }),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_nome(self):
        """Validação do nome da planta"""
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        if len(nome) > 100:
            raise forms.ValidationError("O nome deve ter no máximo 100 caracteres.")
        return nome.strip().title()  # Capitaliza o nome

    def clean_imagem(self):
        """Validação do tamanho da imagem"""
        imagem = self.cleaned_data.get('imagem')
        if imagem:
            if imagem.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError("A imagem deve ter menos de 5MB.")
            
            # Valida tipos de arquivo
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            ext = imagem.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError("Formato de imagem inválido. Use: JPG, PNG, GIF ou WEBP.")
        return imagem

class ComentarioForm(forms.ModelForm):
    """Formulário para criar comentários"""
    
    class Meta:
        model = Comentario
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Compartilhe sua experiência com esta planta...',
                'maxlength': '1000'
            }),
        }
        labels = {
            'conteudo': 'Seu Comentário'
        }

    def clean_conteudo(self):
        """Validação do conteúdo do comentário"""
        conteudo = self.cleaned_data.get('conteudo')
        if len(conteudo) < 5:
            raise forms.ValidationError("O comentário deve ter pelo menos 5 caracteres.")
        if len(conteudo) > 1000:
            raise forms.ValidationError("O comentário deve ter no máximo 1000 caracteres.")
        return conteudo.strip()

# ===== FORMS DE PERFIL =====

class UserProfileForm(forms.ModelForm):
    """Formulário para editar perfil do usuário"""
    
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'localizacao', 'nivel_experiencia']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Conte um pouco sobre você, sua experiência com plantas...',
                'maxlength': '500'
            }),
            'localizacao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: São Paulo - SP'
            }),
            'nivel_experiencia': forms.Select(attrs={'class': 'form-select'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'avatar': 'Foto de Perfil',
            'bio': 'Biografia',
            'localizacao': 'Localização',
            'nivel_experiencia': 'Nível de Experiência'
        }

    def clean_bio(self):
        """Validação da biografia"""
        bio = self.cleaned_data.get('bio')
        if bio and len(bio) > 500:
            raise forms.ValidationError("A biografia deve ter no máximo 500 caracteres.")
        return bio

    def clean_localizacao(self):
        """Validação da localização"""
        localizacao = self.cleaned_data.get('localizacao')
        if localizacao and len(localizacao) > 100:
            raise forms.ValidationError("A localização deve ter no máximo 100 caracteres.")
        return localizacao.strip()

    def clean_avatar(self):
        """Validação do avatar"""
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError("O avatar deve ter menos de 2MB.")
            
            # Valida tipos de arquivo
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            ext = avatar.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError("Formato de imagem inválido. Use: JPG, PNG, GIF ou WEBP.")
        return avatar

# ===== FORMS DE DENÚNCIAS =====

class DenunciaForm(forms.ModelForm):
    """Formulário para criar denúncias"""
    
    class Meta:
        model = Denuncia
        fields = ['categoria', 'descricao']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva o problema detalhadamente...',
                'maxlength': '1000'
            }),
        }
        labels = {
            'categoria': 'Tipo de Problema',
            'descricao': 'Descrição Detalhada'
        }

    def clean_descricao(self):
        """Validação da descrição"""
        descricao = self.cleaned_data.get('descricao')
        if descricao and len(descricao) < 10:
            raise forms.ValidationError("A descrição deve ter pelo menos 10 caracteres.")
        if descricao and len(descricao) > 1000:
            raise forms.ValidationError("A descrição deve ter no máximo 1000 caracteres.")
        return descricao.strip()

# ===== FORMS DE COLEÇÕES =====

class ColecaoForm(forms.ModelForm):
    """Formulário para criar/editar coleções"""
    
    class Meta:
        model = Colecao
        fields = ['nome', 'descricao', 'publica', 'plantas']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da coleção'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição da coleção (opcional)',
                'maxlength': '500'
            }),
            'publica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'plantas': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '10'
            }),
        }
        labels = {
            'nome': 'Nome da Coleção',
            'descricao': 'Descrição',
            'publica': 'Tornar Pública',
            'plantas': 'Plantas da Coleção'
        }

    def __init__(self, *args, **kwargs):
        """Inicializa o formulário com plantas do usuário"""
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filtra apenas as plantas do usuário logado
            self.fields['plantas'].queryset = Planta.objects.filter(autor=user)
            self.fields['plantas'].label_from_instance = lambda obj: f"{obj.nome} ({obj.especie})"

    def clean_nome(self):
        """Validação do nome da coleção"""
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        if len(nome) > 100:
            raise forms.ValidationError("O nome deve ter no máximo 100 caracteres.")
        return nome.strip()

# ===== FORMS DE DIÁRIO =====

class DiarioPlantaForm(forms.ModelForm):
    """Formulário para adicionar entradas no diário"""
    
    class Meta:
        model = DiarioPlanta
        fields = ['titulo', 'anotacao', 'regou', 'fertilizou', 'altura', 'temperatura', 'umidade', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título da entrada'
            }),
            'anotacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Anotações sobre a planta, observações, cuidados...'
            }),
            'regou': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fertilizou': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'altura': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Altura em cm',
                'min': '0',
                'max': '9999',
                'step': '0.1'
            }),
            'temperatura': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Temperatura em °C',
                'min': '-50',
                'max': '60',
                'step': '0.1'
            }),
            'umidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Umidade em %',
                'min': '0',
                'max': '100',
                'step': '0.1'
            }),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'titulo': 'Título da Entrada',
            'anotacao': 'Anotações',
            'regou': 'Regou a planta hoje?',
            'fertilizou': 'Fertilizou a planta hoje?',
            'altura': 'Altura (cm)',
            'temperatura': 'Temperatura (°C)',
            'umidade': 'Umidade (%)',
            'imagem': 'Foto da Planta'
        }

    def clean_titulo(self):
        """Validação do título"""
        titulo = self.cleaned_data.get('titulo')
        if len(titulo) < 3:
            raise forms.ValidationError("O título deve ter pelo menos 3 caracteres.")
        if len(titulo) > 200:
            raise forms.ValidationError("O título deve ter no máximo 200 caracteres.")
        return titulo.strip()

    def clean_anotacao(self):
        """Validação das anotações"""
        anotacao = self.cleaned_data.get('anotacao')
        if anotacao and len(anotacao) > 2000:
            raise forms.ValidationError("As anotações devem ter no máximo 2000 caracteres.")
        return anotacao

    def clean_imagem(self):
        """Validação da imagem"""
        imagem = self.cleaned_data.get('imagem')
        if imagem:
            if imagem.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError("A imagem deve ter menos de 5MB.")
        return imagem

# ===== FORMS DE LEMBRETES =====

class LembreteForm(forms.ModelForm):
    """Formulário para criar lembretes"""
    
    class Meta:
        model = Lembrete
        fields = ['tipo', 'notas', 'frequencia', 'proxima_data', 'ativo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionais (opcional)',
                'maxlength': '500'
            }),
            'frequencia': forms.Select(attrs={'class': 'form-select'}),
            'proxima_data': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'tipo': 'Tipo de Lembrete',
            'notas': 'Notas Adicionais',
            'frequencia': 'Frequência',
            'proxima_data': 'Próxima Data',
            'ativo': 'Ativo'
        }

    def clean_notas(self):
        """Validação das notas"""
        notas = self.cleaned_data.get('notas')
        if notas and len(notas) > 500:
            raise forms.ValidationError("As notas devem ter no máximo 500 caracteres.")
        return notas

    def clean_proxima_data(self):
        """Validação da data"""
        proxima_data = self.cleaned_data.get('proxima_data')
        if proxima_data and proxima_data < timezone.now():
            raise forms.ValidationError("A data não pode ser no passado.")
        return proxima_data

# ===== FORMS DE MENSAGENS =====

class MensagemForm(forms.ModelForm):
    """Formulário para enviar mensagens"""
    
    class Meta:
        model = Mensagem
        fields = ['assunto', 'conteudo']
        widgets = {
            'assunto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Assunto da mensagem',
                'maxlength': '200'
            }),
            'conteudo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Conteúdo da mensagem',
                'maxlength': '2000'
            }),
        }
        labels = {
            'assunto': 'Assunto',
            'conteudo': 'Mensagem'
        }

    def clean_assunto(self):
        """Validação do assunto"""
        assunto = self.cleaned_data.get('assunto')
        if assunto and len(assunto) > 200:
            raise forms.ValidationError("O assunto deve ter no máximo 200 caracteres.")
        return assunto.strip()

    def clean_conteudo(self):
        """Validação do conteúdo"""
        conteudo = self.cleaned_data.get('conteudo')
        if len(conteudo) < 5:
            raise forms.ValidationError("A mensagem deve ter pelo menos 5 caracteres.")
        if len(conteudo) > 2000:
            raise forms.ValidationError("A mensagem deve ter no máximo 2000 caracteres.")
        return conteudo.strip()

# ===== FORMS DE ENQUETES =====

class EnqueteForm(forms.ModelForm):
    """Formulário para criar enquetes"""
    
    class Meta:
        model = Enquete
        fields = ['pergunta', 'descricao', 'data_fim']
        widgets = {
            'pergunta': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pergunta da enquete',
                'maxlength': '500'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição opcional da enquete',
                'maxlength': '1000'
            }),
            'data_fim': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'pergunta': 'Pergunta',
            'descricao': 'Descrição (opcional)',
            'data_fim': 'Data de Término'
        }

    def clean_pergunta(self):
        """Validação da pergunta"""
        pergunta = self.cleaned_data.get('pergunta')
        if len(pergunta) < 10:
            raise forms.ValidationError("A pergunta deve ter pelo menos 10 caracteres.")
        if len(pergunta) > 500:
            raise forms.ValidationError("A pergunta deve ter no máximo 500 caracteres.")
        return pergunta.strip()

    def clean_data_fim(self):
        """Validação da data de término"""
        data_fim = self.cleaned_data.get('data_fim')
        if data_fim and data_fim < timezone.now():
            raise forms.ValidationError("A data de término não pode ser no passado.")
        return data_fim

class OpcaoEnqueteForm(forms.ModelForm):
    """Formulário para criar opções de enquete"""
    
    class Meta:
        model = OpcaoEnquete
        fields = ['texto']
        widgets = {
            'texto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Texto da opção',
                'maxlength': '200'
            }),
        }
        labels = {
            'texto': 'Opção'
        }

    def clean_texto(self):
        """Validação do texto"""
        texto = self.cleaned_data.get('texto')
        if len(texto) < 2:
            raise forms.ValidationError("O texto deve ter pelo menos 2 caracteres.")
        if len(texto) > 200:
            raise forms.ValidationError("O texto deve ter no máximo 200 caracteres.")
        return texto.strip()