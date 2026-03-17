from django.urls import path
from . import views

app_name = 'servicos'

urlpatterns = [
    # Listagens
    path('', views.lista_servicos, name='lista_servicos'),
    path('os-abertas/', views.lista_servicos_abertos, name='lista_servicos_abertos'),

    # Ordem de Serviço
    path('nova/', views.criar_os, name='nova'),
    path('editar/<int:os_id>/', views.detalhe_os, name='detalhe'),
    path('finalizar/<int:os_id>/', views.finalizar_os, name='finalizar_os'),

    # Exclusões (bem separadas)
    path('item/excluir/<int:item_id>/', views.remover_item_os, name='remover_item'),
    path('os/excluir/<int:os_id>/', views.remover_os, name='excluir_os'),
]