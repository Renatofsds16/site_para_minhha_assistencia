
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm
from django.contrib.auth.decorators import login_required


@login_required
def lista_clientes(request):
    clientes = Cliente.objects.filter(empresa=request.user.perfil.empresa)
    return render(request, 'clientes/lista.html', {'clientes': clientes})


@login_required
def criar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.empresa = request.user.perfil.empresa
            cliente.save()
            return redirect('clientes:lista')
    else:
        form = ClienteForm()

    return render(request, 'clientes/form.html', {'form': form})

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk,empresa=request.user.perfil.empresa)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes:lista')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/form.html', {'form': form})


@login_required
def excluir_cliente(request, pk):
    cliente = get_object_or_404(
        Cliente,
        pk=pk,
        empresa=request.user.perfil.empresa
    )

    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes:lista')

    return render(request, 'clientes/confirmar_exclusao.html', {'cliente': cliente})

