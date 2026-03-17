from django.urls import path
from . import views 

app_name = 'estoque'

urlpatterns = [
    path('', views.lista_produtos, name='lista'),
    path('novo/', views.criar_produto, name='novo'),
    path('buscar/', views.busca_lista_produtos, name='buscar'),
    path('editar/<int:pk>/', views.editar_produto, name='editar'),
    path('excluir/<int:pk>/', views.excluir_produto, name='excluir'),
]
