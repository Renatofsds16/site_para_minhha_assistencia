import csv
from django.core.management.base import BaseCommand
from estoque.models import Produto
from accounts.models import Empresa

class Command(BaseCommand):
    help = 'Importa produtos de um arquivo CSV para uma empresa específica'

    def add_arguments(self, parser):
        parser.add_argument('caminho_csv', type=str, help='Caminho para o arquivo CSV')
        parser.add_argument('--empresa_id', type=int, default=1, help='ID da empresa (default: 1)')

    def handle(self, *args, **options):
        caminho_csv = options['caminho_csv']
        empresa_id = options['empresa_id']
        produtos_criados = 0

        # Busca a empresa no banco de dados
        try:
            empresa = Empresa.objects.get(id=empresa_id)
        except Empresa.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Empresa com ID {empresa_id} não encontrada!'))
            return

        try:
            with open(caminho_csv, mode='r', encoding='utf-8-sig') as arquivo:
                leitor = csv.DictReader(arquivo, delimiter=',')

                for linha in leitor:
                    # Limpa espaços nas chaves e valores
                    linha = {chave.strip(): valor.strip() for chave, valor in linha.items() if chave}

                    nome = linha.get('nome')
                    if not nome:
                        continue

                    # Tratamento dos preços (suporta 'R$ 49,90' ou '49.90')
                    def converte_preco(val):
                        if not val:
                            return 0.0
                        val_limpo = val.replace('R$', '').replace('.', '').replace(',', '.').strip()
                        return float(val_limpo) if val_limpo else 0.0

                    preco_venda = converte_preco(linha.get('preco_venda') or linha.get('preco'))
                    preco_custo = converte_preco(linha.get('preco_custo'))

                    # Tratamento da quantidade
                    raw_qtd = linha.get('quantidade') or linha.get('estoque', '0')
                    quantidade = int(raw_qtd) if raw_qtd.isdigit() else 0

                    # Salva no banco vinculando à empresa
                    Produto.objects.update_or_create(
                        nome=nome,
                        empresa=empresa,
                        defaults={
                            'preco_venda': preco_venda,
                            'preco_custo': preco_custo,
                            'quantidade': quantidade,
                        }
                    )
                    produtos_criados += 1

            self.stdout.write(
                self.style.SUCCESS(f'Sucesso! {produtos_criados} produtos importados para a empresa "{empresa.nome}".')
            )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Arquivo não encontrado: {caminho_csv}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao processar arquivo: {e}'))