from django.contrib import admin
from .models import OrdemServico, ItemOrdemServico, MaoObra


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente',
        'aparelho',
        'status',
        'total_geral',
        'data_entrada',
    )

    readonly_fields = (
        'data_entrada',
        'total_geral',
    )

    def total_geral(self, obj):
        return obj.total_geral()

    total_geral.short_description = 'Total da OS'


@admin.register(ItemOrdemServico)
class ItemOrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('ordem', 'produto', 'quantidade', 'valor')


@admin.register(MaoObra)
class MaoObraAdmin(admin.ModelAdmin):
    list_display = ('ordem', 'descricao', 'valor')
