from django.contrib import admin
from .models import Agenda

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('ordem_servico', 'data', 'hora', 'status')
    list_filter = ('status', 'data')
