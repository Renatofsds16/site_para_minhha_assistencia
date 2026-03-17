from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from accounts.models import Perfil, Empresa

@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, **kwargs):
    if created:
        empresa = Empresa.objects.create(
            nome=f'Empresa de {instance.username}',
            dono=instance
        )
        Perfil.objects.create(
            user=instance,
            empresa=empresa,
            cargo='dono'
        )
