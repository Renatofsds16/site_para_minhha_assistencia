from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto,Categoria
from .forms import ProdutoForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def lista_produtos(request):
    produtos_qs = Produto.objects.filter(ativo=True,empresa=request.user.perfil.empresa).order_by('nome')

    paginator = Paginator(produtos_qs, 12)  # 10 produtos por página
    page_number = request.GET.get('page')
    produtos = paginator.get_page(page_number)

    return render(request, 'estoque/lista.html', {
        'produtos': produtos
    })


@login_required
def busca_lista_produtos(request):
    busca = request.GET.get('q')

    produtos_qs = Produto.objects.filter(ativo=True,empresa=request.user.perfil.empresa).order_by('nome')

    if busca:
        produtos_qs = produtos_qs.filter(nome__icontains=busca)

    paginator = Paginator(produtos_qs, 12)
    page_number = request.GET.get('page')
    produtos = paginator.get_page(page_number)

    return render(request, 'estoque/lista.html', {
        'produtos': produtos,
        'busca': busca
    })



@login_required
def criar_produto(request):
    empresa = request.user.perfil.empresa

    if request.method == 'POST':
        form = ProdutoForm(request.POST, empresa=empresa)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.empresa = empresa

            nova_categoria = form.cleaned_data.get("nova_categoria")

            if nova_categoria:
                categoria, _ = Categoria.objects.get_or_create(
                    nome=nova_categoria.strip().title(),
                    empresa=empresa
                )
                produto.categoria = categoria
            # else: deixa a categoria como None (permitido)

            produto.save()
            return redirect('estoque:lista')
    else:
        form = ProdutoForm(empresa=empresa)

    return render(request, 'estoque/form.html', {'form': form})



@login_required
def editar_produto(request, pk):
    empresa = request.user.perfil.empresa
    produto = get_object_or_404(Produto, pk=pk, empresa=empresa)

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto, empresa=empresa)
        if form.is_valid():
            produto = form.save(commit=False)

            nova_categoria = form.cleaned_data.get("nova_categoria")
            if nova_categoria:
                categoria, _ = Categoria.objects.get_or_create(
                    nome=nova_categoria.strip(),
                    empresa=empresa
                )
                produto.categoria = categoria

            produto.save()
            return redirect('estoque:lista')
    else:
        form = ProdutoForm(instance=produto, empresa=empresa)

    return render(request, 'estoque/form.html', {'form': form})


@login_required
def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk,empresa=request.user.perfil.empresa)
    produto.delete()
    return redirect('estoque:lista')
