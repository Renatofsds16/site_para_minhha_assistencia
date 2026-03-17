from django.contrib import admin
from django.urls import path, include
from core.views import login_view, dashboard
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # AUTH
    path('', login_view),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # DASHBOARD (protegido)
    path('dashboard/', dashboard, name='dashboard'),
    # APPS
    path('accounts/', include('accounts.urls')),
    path('agenda/', include('agenda.urls')),
    path('estoque/', include('estoque.urls')),
    path('servicos/', include('servicos.urls')),
    path('vendas/', include('vendas.urls')),
    path('financeiro/', include('financeiro.urls')),
    path('clientes/', include('clientes.urls')),
]
