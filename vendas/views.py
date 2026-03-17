from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Venda, ItemVenda
from .form import VendaForm
from estoque.models import Produto
from datetime import date



@login_required
def lista_vendas(request):
    hoje = date.today()
    ano_atual = hoje.year
    mes_atual = hoje.month
    vendas = Venda.objects.filter(
        empresa=request.user.perfil.empresa,
        data__year=ano_atual,
        data__month=mes_atual
    ).order_by('-data')
    return render(request, "vendas/lista_vendas.html", {
        "vendas": vendas,
        "mes_atual": mes_atual,
        "ano_atual": ano_atual
    })

@login_required
def criar_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            venda = form.save(commit=False)
            venda.empresa = request.user.perfil.empresa
            venda.save()
            return redirect('vendas:detalhe', venda.id)
    else:
        form = VendaForm()

    return render(request, 'vendas/form_venda.html', {
        'form': form
    })

@login_required
def detalhe_venda(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id,empresa=request.user.perfil.empresa)
    venda.atualizar_total()
    produtos = Produto.objects.filter(ativo=True,empresa=request.user.perfil.empresa)
    itens = venda.itens.all()

    if request.method == 'POST':
        produto_id = request.POST.get('produto')
        quantidade = int(request.POST.get('quantidade', 1))

        produto = get_object_or_404(Produto, id=produto_id,empresa=request.user.perfil.empresa)

        ItemVenda.objects.create(
            venda=venda,
            produto=produto,
            quantidade=quantidade
        )

        return redirect('vendas:detalhe', venda.id)

    return render(request, 'vendas/detalhe_venda.html', {
        'venda': venda,
        'produtos': produtos,
        'itens': itens
    })


@login_required
def remover_item_venda(request, item_venda_id):
    item = get_object_or_404(ItemVenda, id=item_venda_id,venda__empresa=request.user.perfil.empresa)
    venda = item.venda
    item.delete()
    venda.atualizar_total()
    return redirect('vendas:detalhe', venda_id=venda.id)



@login_required
def editar_venda(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id,empresa=request.user.perfil.empresa)

    if request.method == 'POST':
        form = VendaForm(request.POST, instance=venda)
        if form.is_valid():
            form.save()
            return redirect('vendas:detalhe', venda.id)
    else:
        form = VendaForm(instance=venda)

    return render(request, 'vendas/form_venda.html', {
        'form': form,
        'venda': venda
    })


@login_required
def remover_venda(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id,empresa=request.user.perfil.empresa)
    venda.delete()
    return redirect('vendas:lista_vendas')
