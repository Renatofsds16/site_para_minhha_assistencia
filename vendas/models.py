from django.db import models
from django.db.models import Sum
from clientes.models import Cliente
from estoque.models import Produto
from accounts.models import Empresa


class Venda(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    data = models.DateTimeField(auto_now_add=True)
    observacao = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        editable=False
    )

    forma_pagamento = models.CharField(
        max_length=20,
        choices=[
            ('pix', 'Pix'),
            ('dinheiro', 'Dinheiro'),
            ('cartao', 'Cartão'),
        ]
    )

    def __str__(self):
        return f"Venda #{self.id}"

    def atualizar_total(self):
        """
        Soma apenas o valor total de cada item da venda.
        NÃO multiplica quantidade novamente.
        """
        self.valor_total = self.itens.aggregate(
            total=Sum('valor')
        )['total'] or 0

        self.save(update_fields=['valor_total'])


class ItemVenda(models.Model):
    venda = models.ForeignKey(
        Venda,
        related_name='itens',
        on_delete=models.CASCADE
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.SET_NULL,
        null=True
    )

    quantidade = models.PositiveIntegerField(default=1)

    # Valor TOTAL do item (preço unitário * quantidade)
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        editable=False
    )

    def save(self, *args, **kwargs):
        if self.produto:
            self.valor = self.produto.preco_venda * self.quantidade

        super().save(*args, **kwargs)

        # Atualiza automaticamente o total da venda
        self.venda.atualizar_total()

    def delete(self, *args, **kwargs):
        venda = self.venda
        super().delete(*args, **kwargs)
        venda.atualizar_total()

    def __str__(self):
        return f"{self.produto} ({self.quantidade})"
