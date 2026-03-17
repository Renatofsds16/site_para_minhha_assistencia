from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ItemOrdemServico, MaoObra

@receiver([post_save, post_delete], sender=ItemOrdemServico)
@receiver([post_save, post_delete], sender=MaoObra)
def atualizar_total_os(sender, instance, **kwargs):
    instance.ordem.total_geral()
