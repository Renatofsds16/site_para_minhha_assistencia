from django import forms
from .models import ContaReceber, ItemFiado
from clientes.models import Cliente
from estoque.models import Produto
from servicos.models import OrdemServico


class ContaReceberForm(forms.ModelForm):
    class Meta:
        model = ContaReceber
        exclude = ('empresa', 'status', 'valor')
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'data_vencimento': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)

        if empresa:
            self.fields['cliente'].queryset = Cliente.objects.filter(
                empresa=empresa
            )


class ItemFiadoForm(forms.ModelForm):
    class Meta:
        model = ItemFiado
        fields = ('produto', 'servico', 'quantidade')
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'servico': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)

        if empresa:
            self.fields['produto'].queryset = Produto.objects.filter(
                empresa=empresa,
                ativo=True
            )
            self.fields['servico'].queryset = OrdemServico.objects.filter(
                empresa=empresa
            )

    def clean(self):
        cleaned = super().clean()
        produto = cleaned.get('produto')
        servico = cleaned.get('servico')

        if not produto and not servico:
            raise forms.ValidationError(
                'Informe um produto ou um serviço.'
            )

        if produto and servico:
            raise forms.ValidationError(
                'Escolha apenas produto ou serviço, não os dois.'
            )

        return cleaned
