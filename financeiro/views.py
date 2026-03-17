from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.db import transaction
from django.utils.timezone import now
from vendas.models import Venda


from .models import ContaReceber, ItemFiado
from .forms import ContaReceberForm, ItemFiadoForm


@login_required
def lista_fiado(request):
    empresa = request.user.perfil.empresa

    fiados = ContaReceber.objects.filter(
        empresa=empresa
    ).order_by('status', 'data_vencimento')

    return render(request, 'financeiro/lista_fiado.html', {
        'fiados': fiados
    })


@login_required
def novo_fiado(request):
    empresa = request.user.perfil.empresa

    # ✅ AQUI É ONDE O ItemFormSet É CRIADO
    ItemFormSet = modelformset_factory(
        ItemFiado,
        form=ItemFiadoForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        # ✅ Form principal (Conta a Receber)
        form = ContaReceberForm(
            request.POST,
            empresa=empresa
        )

        # ✅ Formset dos itens do fiado
        formset = ItemFormSet(
            request.POST,
            queryset=ItemFiado.objects.none(),
            form_kwargs={'empresa': empresa}
        )

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                conta = form.save(commit=False)
                conta.empresa = empresa
                conta.status = 'aberto'
                conta.valor = 0
                conta.save()

                total = 0

                for item in formset.save(commit=False):
                    item.conta = conta

                    # 💰 Define valor automaticamente
                    if item.produto:
                        item.valor_unitario = item.produto.preco_venda
                        item.produto.quantidade -= item.quantidade
                        item.produto.save()

                    if item.servico:
                        item.valor_unitario = item.servico.total_geral()

                    total += item.subtotal()
                    item.save()

                conta.valor = total
                conta.save()

            return redirect('financeiro:lista_fiado')

    else:
        # ✅ GET (primeiro carregamento da página)
        form = ContaReceberForm(empresa=empresa)
        formset = ItemFormSet(
            queryset=ItemFiado.objects.none(),
            form_kwargs={'empresa': empresa}
        )

    return render(request, 'financeiro/form_fiado.html', {
        'form': form,
        'formset': formset
    })


@login_required
@transaction.atomic
def marcar_fiado_pago(request, pk):
    fiado = get_object_or_404(
        ContaReceber.objects.select_for_update(),
        id=pk
    )

    # Segurança: não duplicar pagamento
    if fiado.status == 'pago':
        return redirect('financeiro:lista_fiado')

    # 1️⃣ Marca como pago
    fiado.status = 'pago'
    fiado.data_vencimento = now()  # ✅ campo correto
    fiado.save()

    # 2️⃣ Cria a venda (entra no faturamento)
    Venda.objects.create(
        empresa=fiado.empresa,
        cliente=fiado.cliente,
        valor_total=fiado.valor,
        data=now(),
        observacao=f'Fiado pago - ID {fiado.pk}'
    )

    return redirect('financeiro:lista_fiado')




@login_required
def excluir_fiado(request, pk):
    empresa = request.user.perfil.empresa

    fiado = get_object_or_404(
        ContaReceber,
        pk=pk,
        empresa=empresa
    )

    fiado.delete()

    return redirect('financeiro:lista_fiado')

