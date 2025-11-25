from django import forms
from .models import Planta

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
        return nome.upper()  # Exemplo de transformação