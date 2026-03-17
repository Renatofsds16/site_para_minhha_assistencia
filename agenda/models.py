from django.db import models
from servicos.models import OrdemServico
from accounts.models import Empresa

class Agenda(models.Model):

    STATUS_CHOICES = [
        ('AGENDADO', 'Agendado'),
        ('CONFIRMADO', 'Confirmado'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    ]

    ordem_servico = models.OneToOneField(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='agenda'
    )

    data = models.DateField()
    hora = models.TimeField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='AGENDADO'
    )

    observacao = models.TextField(blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OS #{self.ordem_servico.id} - {self.data} {self.hora}"
