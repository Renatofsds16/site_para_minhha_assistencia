from django.db import models
from django.db.models import Sum
from estoque.models import Produto
from clientes.models import Cliente
from accounts.models import Empresa


class OrdemServico(models.Model):
    STATUS_CHOICES = (
        ('Aberta', 'Aberta'),
        ('Concluída', 'Concluída'),
    )

    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    aparelho = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Aberta')
    data_entrada = models.DateTimeField(auto_now_add=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    

    def total_produtos(self):
        return self.itens.aggregate(
            total=Sum('valor')
        )['total'] or 0

    def total_servicos(self):
        return self.mao_obra.aggregate(
            total=Sum('valor')
        )['total'] or 0

    def total_geral(self):
        return self.total_produtos() + self.total_servicos()

    def __str__(self):
        return f'OS #{self.id} - {self.cliente}'


class ItemOrdemServico(models.Model):
    ordem = models.ForeignKey(
        OrdemServico,
        related_name='itens',
        on_delete=models.CASCADE
    )
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    valor = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.valor = self.produto.preco_venda * self.quantidade
        super().save(*args, **kwargs)


class MaoObra(models.Model):
    ordem = models.ForeignKey(
        OrdemServico,
        related_name='mao_obra',
        on_delete=models.CASCADE
    )
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.descricao
