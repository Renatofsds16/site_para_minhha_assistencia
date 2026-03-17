from django.urls import path
from . import views


app_name = 'financeiro'

6
urlpatterns = [
    path('fiados/', views.lista_fiado, name='lista_fiado'),
    path('fiado/novo/', views.novo_fiado, name='novo_fiado'),
    path('fiado/pago/<int:pk>/', views.marcar_fiado_pago, name='marcar_pago'),
    path('fiado/excluir/<int:pk>/', views.excluir_fiado, name='excluir_fiado')
]
