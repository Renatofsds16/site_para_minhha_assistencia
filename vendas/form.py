from django import forms
from .models import Venda,ItemVenda

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente']
        exclude = ['empresa', 'data']
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-select'
            })
        }

class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade']
        widgets = {
            'produto': forms.Select(attrs={
                'class': 'form-select produto-select'
            })
        }