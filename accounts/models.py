
from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    dono = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='empresas'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cargo = models.CharField(
        max_length=20,
        choices=[
            ('dono', 'Dono'),
            ('funcionario', 'Funcionário')
        ],
        default='dono'
    )

    def __str__(self):
        return self.user.username
