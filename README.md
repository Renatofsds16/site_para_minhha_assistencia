# Smart Fix - Sistema de Gestão para Assistência Técnica

O Smart Fix é uma aplicação web desenvolvida com Django, projetada para gerenciar operações de assistências técnicas de forma eficiente. O sistema centraliza informações essenciais como vendas, ordens de serviço, estoque, faturamento e agendamentos, oferecendo uma visão clara e organizada do negócio.

A aplicação foi construída com foco em escalabilidade e multiusuário, permitindo que cada usuário administre sua própria assistência técnica de forma isolada e segura.

## Visão Geral

## link do projeto online
- https://site-para-minhha-assistencia.onrender.com

O sistema possui um dashboard inicial que apresenta indicadores importantes para a tomada de decisão, além de diversas funcionalidades para controle operacional do dia a dia.

## Funcionalidades

### Dashboard

- Faturamento diário e mensal
- Total de vendas realizadas
- Controle de valores em aberto (fiado)
- Indicadores de ordens de serviço
- Visão geral do estoque
- Agendamentos do dia

### Gestão de Vendas

- Criação de vendas simples
- Venda integrada com ordem de serviço
- Registro de produtos vendidos
- Controle de valores e formas de pagamento

### Ordem de Serviço

- Abertura e acompanhamento de serviços
- Controle de status (em andamento, concluído, entregue)
- Associação com produtos e clientes
- Cálculo de valores de serviço

### Produtos e Estoque

- Cadastro de produtos
- Controle de quantidade em estoque
- Registro de entrada e saída de itens
- Organização por categorias

### Agendamentos

- Cadastro de atendimentos agendados
- Organização por data
- Controle de clientes e serviços

### Garantia

- Listagem de serviços ainda dentro do período de garantia
- Controle de prazos

### Multiusuário (Multi-tenant)

- Cada usuário representa uma assistência técnica
- Dados completamente isolados por usuário
- Segurança e privacidade das informações

### Área do Cliente

- Página dedicada para clientes realizarem consultas de orçamento
- Interface simplificada para interação com a assistência

## Funcionalidades Futuras

- Integração com IA generativa para:
  - Consulta automática de orçamento
  - Suporte na identificação de problemas em aparelhos
- Sistema de notificações
- Relatórios avançados
- Integração com meios de pagamento
- API pública para integrações externas

## Tecnologias Utilizadas

- Python
- Django
- SQLite (ou outro banco configurável)
- HTML5
- CSS3
- JavaScript


## Como Executar o Projeto

### Pré-requisitos

- Python 3.8+
- pip
- virtualenv (recomendado)

### 1. Clone o repositório

```bash
git clone https://github.com/Renatofsds16/smart-fix.git

cd smart-fix

python -m venv venv

venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
http://127.0.0.1:8000/
