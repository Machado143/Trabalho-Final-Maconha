from django import forms
from .models import Planta, Comentario
from .models import UserProfile
from .models import Denuncia
from .models import Colecao, DiarioPlanta, Lembrete, Mensagem, Enquete, OpcaoEnquete

class PlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = ['nome', 'especie', 'dificuldade', 'necessidade_agua', 'necessidade_luz', 'descricao', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.TextInput(attrs={'class': 'form-control'}),
            'dificuldade': forms.Select(attrs={'class': 'form-select'}),
            'necessidade_agua': forms.TextInput(attrs={'class': 'form-control'}),
            'necessidade_luz': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome.upper()

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Compartilhe sua experiência com esta planta...'
            }),
        }
        labels = {
            'conteudo': 'Seu Comentário'
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'localizacao', 'nivel_experiencia']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Conte um pouco sobre você...'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: São Paulo - SP'}),
            'nivel_experiencia': forms.Select(attrs={'class': 'form-select'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'avatar': 'Foto de Perfil',
            'bio': 'Bio',
            'localizacao': 'Localização',
            'nivel_experiencia': 'Nível de Experiência'
        }

class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ['categoria', 'descricao']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva o problema...'}),
        }

class ColecaoForm(forms.ModelForm):
    class Meta:
        model = Colecao
        fields = ['nome', 'descricao', 'publica', 'plantas']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da coleção'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição da coleção'}),
            'publica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'plantas': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

class DiarioPlantaForm(forms.ModelForm):
    class Meta:
        model = DiarioPlanta
        fields = ['titulo', 'anotacao', 'regou', 'fertilizou', 'altura', 'temperatura', 'umidade', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da entrada'}),
            'anotacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Anotações sobre a planta'}),
            'regou': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fertilizou': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Altura em cm'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Temperatura em °C'}),
            'umidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Umidade em %'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }

class LembreteForm(forms.ModelForm):
    class Meta:
        model = Lembrete
        fields = ['tipo', 'notas', 'frequencia', 'proxima_data', 'ativo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notas adicionais'}),
            'frequencia': forms.Select(attrs={'class': 'form-select'}),
            'proxima_data': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['assunto', 'conteudo']
        widgets = {
            'assunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Assunto da mensagem'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Conteúdo da mensagem'}),
        }

class EnqueteForm(forms.ModelForm):
    class Meta:
        model = Enquete
        fields = ['pergunta', 'descricao', 'data_fim']
        widgets = {
            'pergunta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pergunta da enquete'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição opcional'}),
            'data_fim': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class OpcaoEnqueteForm(forms.ModelForm):
    class Meta:
        model = OpcaoEnquete
        fields = ['texto']
        widgets = {
            'texto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto da opção'}),
        }

class ColecaoForm(forms.ModelForm):
    class Meta:
        model = Colecao
        fields = ['nome', 'descricao', 'plantas', 'publica']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

class DiarioPlantaForm(forms.ModelForm):
    class Meta:
        model = DiarioPlanta
        fields = ['data', 'titulo', 'anotacao', 'regou', 'fertilizou', 'imagem']
        widgets = {
            'anotacao': forms.Textarea(attrs={'rows': 4}),
        }