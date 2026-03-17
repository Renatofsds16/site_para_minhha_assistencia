from django import forms
from .models import OrdemServico, MaoObra


class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = [
            'cliente',
            'aparelho',
            'status',
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'aparelho': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class MaoObraForm(forms.ModelForm):
    class Meta:
        model = MaoObra
        fields = ['descricao', 'valor']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
        }
