from django.urls import path
from .views import login_view,cadastro


app_name = 'accounts'

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
]
