from django import forms
from .models import Produto,Categoria


class ProdutoForm(forms.ModelForm):
    nova_categoria = forms.CharField(
        label="Nova categoria",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Digite para criar nova categoria"
        })
    )

    class Meta:
        model = Produto
        fields = [
            'nome',
            'categoria',
            'preco_custo',
            'preco_venda',
            'quantidade',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco_custo': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.empresa = kwargs.pop("empresa", None)
        super().__init__(*args, **kwargs)

        if self.empresa:
            self.fields["categoria"].queryset = Categoria.objects.filter(
                empresa=self.empresa
            )
