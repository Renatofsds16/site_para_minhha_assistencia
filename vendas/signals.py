
from .models import ItemVenda
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ItemVenda


@receiver(post_save, sender=ItemVenda)
def baixar_estoque(sender, instance, created, **kwargs):
    if created:
        produto = instance.produto
        produto.quantidade -= instance.quantidade
        produto.save()


@receiver(post_save, sender=ItemVenda)
@receiver(post_delete, sender=ItemVenda)
def atualizar_total_venda(sender, instance, **kwargs):
    instance.venda.atualizar_total()


