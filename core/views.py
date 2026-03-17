from django.shortcuts import render,redirect
from django.utils.timezone import now
from servicos.models import OrdemServico
from vendas.models import Venda
from estoque.models import Produto
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from financeiro.models import ContaReceber
from django.db.models import Sum,F
from django.utils.timezone import localdate





@login_required
def dashboard(request):
    empresa = request.user.perfil.empresa
    hoje = now()

        # Fiado (contas a receber em aberto)
    fiado_aberto = ContaReceber.objects.filter(
        empresa=empresa,
        status='aberto'
    ).aggregate(total=Sum('valor'))['total'] or 0


    # Total de produtos
    produtos = Produto.objects.filter(empresa=empresa).count()

    valor_total_produtos = Produto.objects.filter(
            empresa=empresa
        ).aggregate(
            total=Sum(F('preco_venda') * F('quantidade'))
        )['total'] or 0

    # OS abertas
    os_abertas_qs = OrdemServico.objects.filter(
        empresa=empresa,
        status='Aberta'
    )
    os_abertas = os_abertas_qs.count()
    valor_a_receber = sum(os.total_geral() for os in os_abertas_qs)

    # OS concluídas
    os_concluidas_qs = OrdemServico.objects.filter(
        empresa=empresa,
        status='Concluída'
    )

    # OS com serviços
    servicos = os_concluidas_qs.filter(
        mao_obra__isnull=False
    ).count()

    # OS só de produtos
    os_produtos = os_concluidas_qs.filter(
        mao_obra__isnull=True
    ).count()

    # Vendas
    vendas_qs = Venda.objects.filter(empresa=empresa)
    vendas = vendas_qs.count()

    # Faturamento do mês
    ordens_mes = os_concluidas_qs.filter(
        data_entrada__month=hoje.month,
        data_entrada__year=hoje.year
    )
    faturamento_os = sum(os.total_geral() for os in ordens_mes)

    vendas_mes = vendas_qs.filter(
        data__month=hoje.month,
        data__year=hoje.year
    )
    faturamento_vendas = sum(v.valor_total for v in vendas_mes)

    faturamento_mes = faturamento_os + faturamento_vendas

    total_os_concluidas = os_concluidas_qs.count()

    # Gráficos
    grafico_os = {
        'Serviços': servicos,
        'Só Produtos': os_produtos
    }

    grafico_faturamento = {
        'OS': faturamento_os,
        'Vendas': faturamento_vendas
    }

    # 📅 Data de hoje (sem hora)
    hoje_data = localdate()

    # 💰 Vendas do dia
    vendas_dia = Venda.objects.filter(
        empresa=empresa,
        data__date=hoje_data
    )
    faturamento_vendas_dia = vendas_dia.aggregate(
        total=Sum('valor_total')
    )['total'] or 0

    # 💰 OS concluídas hoje
    os_dia = OrdemServico.objects.filter(
        empresa=empresa,
        status='Concluída',
        data_entrada__date=hoje_data
    )
    faturamento_os_dia = sum(os.total_geral() for os in os_dia)

    # 💵 Faturamento total do dia
    faturamento_dia = faturamento_vendas_dia + faturamento_os_dia

    context = {
        'produtos': produtos,
        'servicos': servicos,
        'vendas': vendas,
        'os_abertas': os_abertas,
        'valor_a_receber': valor_a_receber,
        'fiado_aberto': fiado_aberto,
        'faturamento_os': faturamento_os,
        'faturamento_vendas': faturamento_vendas,
        'faturamento_mes': faturamento_mes,
        'total_os_concluidas': total_os_concluidas,
        'grafico_os': grafico_os,
        'grafico_faturamento': grafico_faturamento,
        'valor_total_produtos': valor_total_produtos,
        'faturamento_dia': faturamento_dia,
        'faturamento_vendas_dia': faturamento_vendas_dia,
        'faturamento_os_dia': faturamento_os_dia,
    }

    return render(request, "dashboard/dashboard.html", context)




def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    erro = None

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            erro = "Usuário ou senha inválidos"

    return render(request, 'auth/login.html', {'erro': erro})




