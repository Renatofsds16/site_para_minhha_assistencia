from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.lista_clientes, name='lista'),
    path('novo/', views.criar_cliente, name='novo'),
    path('editar/<int:pk>/', views.editar_cliente, name='editar'),
    path('excluir/<int:pk>/', views.excluir_cliente, name='excluir'),
]
