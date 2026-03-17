from django.urls import path
from . import views


app_name = 'agenda'


urlpatterns = [
    path('', views.lista_agenda, name='lista'),
    path('nova/', views.nova_agenda, name='nova'),
    path('editar/<int:agenda_id>/', views.editar_agenda, name='editar'),
    path('excluir/<int:agenda_id>/', views.remover_agenda, name='excluir'),
]
