from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import OrdemServico, ItemOrdemServico, MaoObra
from .form import OrdemServicoForm
from estoque.models import Produto


@login_required
def lista_servicos(request):
    servicos = OrdemServico.objects.filter(
        empresa=request.user.perfil.empresa
    ).order_by('-id')

    return render(request, "servicos/lista_servicos.html", {"servicos": servicos})


@login_required
def criar_os(request):
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            os = form.save(commit=False)
            os.empresa = request.user.perfil.empresa
            os.save()
            return redirect('servicos:detalhe', os_id=os.id)
    else:
        form = OrdemServicoForm()

    return render(request, 'servicos/form_os.html', {'form': form})


@login_required
def detalhe_os(request, os_id):
    os = get_object_or_404(
        OrdemServico,
        id=os_id,
        empresa=request.user.perfil.empresa
    )

    produtos = Produto.objects.filter(
        ativo=True,
        empresa=request.user.perfil.empresa
    )

    itens = os.itens.all()
    servicos = os.mao_obra.all()

    if request.method == 'POST':
        tipo_form = request.POST.get('tipo_form')

        # ➕ PRODUTO
        if tipo_form == "produto":
            produto_id = request.POST.get('produto')
            quantidade = int(request.POST.get('quantidade', 1))

            produto = get_object_or_404(
                Produto,
                id=produto_id,
                empresa=request.user.perfil.empresa
            )

            ItemOrdemServico.objects.create(
                ordem=os,
                produto=produto,
                quantidade=quantidade
            )
            return redirect('servicos:detalhe', os_id=os.id)

        # ➕ SERVIÇO
        elif tipo_form == "servico_extra":
            descricao = request.POST.get('descricao')
            valor = request.POST.get('valor')

            if descricao and valor:
                MaoObra.objects.create(
                    ordem=os,
                    descricao=descricao,
                    valor=valor
                )
            return redirect('servicos:detalhe', os_id=os.id)

    return render(request, 'servicos/detalhe_os.html', {
        'os': os,
        'produtos': produtos,
        'itens': itens,
        'servicos': servicos,
    })


@login_required
def finalizar_os(request, os_id):
    os = get_object_or_404(
        OrdemServico,
        id=os_id,
        empresa=request.user.perfil.empresa
    )

    if request.method == 'POST':
        form = OrdemServicoForm(request.POST, instance=os)
        if form.is_valid():
            form.save()

    return redirect('servicos:lista_servicos')


@login_required
def remover_item_os(request, item_id):
    if request.method != 'POST':
        return redirect('servicos:lista_servicos')

    item = get_object_or_404(
        ItemOrdemServico,
        id=item_id,
        ordem__empresa=request.user.perfil.empresa
    )

    os_id = item.ordem.id
    item.delete()

    return redirect('servicos:detalhe', os_id=os_id)


@login_required
def lista_servicos_abertos(request):
    servicos = OrdemServico.objects.filter(
        status='Aberta',
        empresa=request.user.perfil.empresa
    ).order_by('-data_entrada')

    return render(request, 'servicos/lista_servicos.html', {
        'servicos': servicos
    })


@login_required
def remover_os(request, os_id):
    if request.method != 'POST':
        return redirect('servicos:lista_servicos')

    os = get_object_or_404(
        OrdemServico,
        id=os_id,
        empresa=request.user.perfil.empresa
    )

    # Proteção: não excluir OS finalizada
    if os.status == 'finalizada':
        return redirect('servicos:lista_servicos')

    os.delete()
    return redirect('servicos:lista_servicos')