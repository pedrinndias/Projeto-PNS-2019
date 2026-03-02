# Projeto PNS 2019 – Análise de Dados de Saúde

Este repositório contém scripts, notebooks e dados utilizados para análise da Pesquisa Nacional de Saúde (PNS) 2019, com foco em pessoas idosas (acima de 60 anos) e a prevalência de doenças crônicas, especialmente artrite e reumatismo.

## Estrutura do Repositório

- **data/**: Dados utilizados no projeto.
  - **raw/**: Dados brutos originais (SAS, TXT, CSV).
  - **processed/**: Dados processados e prontos para análise.
  - **database/**: Banco de dados formatado.
- **docs/**: Documentação adicional.
- **notebooks/**: Notebooks Jupyter para exploração e análise dos dados.
- **scripts/**: Scripts Python para processamento e preparação dos dados.
- **src/**: Código-fonte adicional (em desenvolvimento).

## Principais Arquivos

- `notebooks/pessoas_saudaveis.ipynb`: Notebook principal de análise de pessoas idosas sem doenças crônicas e com artrite/reumatismo.
- `scripts/criar_banco_formatado.py`: Script para criação do banco de dados formatado a partir dos dados brutos.
- `data/raw/pns2019.csv`: Base de dados principal em formato CSV.

## Objetivo

O objetivo deste projeto é identificar e analisar o perfil de pessoas idosas saudáveis e comparar com aquelas que possuem artrite/reumatismo, utilizando os microdados da PNS 2019.

## Como Utilizar

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```
2. Instale as dependências necessárias (recomenda-se uso de ambiente virtual):
   ```bash
   pip install -r requirements.txt
   ```
3. Execute os notebooks ou scripts conforme desejado.

## Requisitos
- Python 3.x
- Pandas, NumPy, Matplotlib (e outras bibliotecas listadas em `requirements.txt`)

## Créditos
- Dados: [IBGE - Pesquisa Nacional de Saúde 2019](https://www.ibge.gov.br/estatisticas/sociais/saude/9160-pesquisa-nacional-de-saude.html)

---

Sinta-se à vontade para contribuir ou abrir issues para sugestões e melhorias!