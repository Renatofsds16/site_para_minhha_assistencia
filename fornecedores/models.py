from django.db import models

class Fornecedor(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
