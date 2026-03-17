from django.contrib import admin
from .models import Venda, ItemVenda

class ItemInline(admin.TabularInline):
    model = ItemVenda
    readonly_fields = ('valor',)
    fields = ('produto', 'quantidade', 'valor')
    extra = 1

class VendaAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
    readonly_fields = ('valor_total',)

admin.site.register(Venda, VendaAdmin)
