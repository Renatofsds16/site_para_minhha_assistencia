from django.urls import path
from .  import views


app_name = 'vendas'

urlpatterns = [
    path('', views.lista_vendas, name='lista_vendas'),#ok
    path('nova/', views.criar_venda, name='nova'),
    path('detalhe/<int:venda_id>/', views.detalhe_venda, name='detalhe'),
    path('<int:venda_id>/editar/', views.editar_venda, name='editar'),
    path('remover_venda/<int:venda_id>/', views.remover_venda, name='remover_venda'),
    path('remover_item/<int:item_venda_id>/', views.remover_item_venda, name='remover_item'),
]
