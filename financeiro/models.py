from django.db import models
from clientes.models import Cliente
from estoque.models import Produto
from accounts.models import Empresa
from servicos.models import OrdemServico


class ContaReceber(models.Model):
    STATUS_CHOICES = (
        ('aberto', 'Em aberto'),
        ('pago', 'Pago'),
    )

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='aberto')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cliente} - R$ {self.valor}'
    


class ItemFiado(models.Model):
    conta = models.ForeignKey(ContaReceber, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True)
    servico = models.ForeignKey(OrdemServico, on_delete=models.SET_NULL, null=True, blank=True)
    quantidade = models.PositiveIntegerField(default=1)
    valor_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.valor_unitario:
            if self.produto:
                self.valor_unitario = self.produto.preco_venda
            elif self.servico:
                self.valor_unitario = self.servico.valor
        super().save(*args, **kwargs)

    def subtotal(self):
        return self.quantidade * self.valor_unitario



