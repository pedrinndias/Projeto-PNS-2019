# Projeto PNS 2019 – Análise de Dados de Saúde

Este repositório contém scripts, notebooks e dados utilizados para análise da Pesquisa Nacional de Saúde (PNS) 2019, com foco em pessoas idosas (acima de 60 anos) e a prevalência de doenças crônicas, especialmente artrite e reumatismo.

## Estrutura do Repositório

- **archive/**: Backup de notebooks antigos, relatórios anteriores e arquivos não utilizados.
- **data/**: Dados utilizados no projeto.
  - **raw/**: Dados brutos originais (CSV, TXT e dicionários XLS). *Atenção: o arquivo `pns2019.csv` não é versionado no Git devido ao tamanho.*
  - **processed/**: Dados processados, filtrados e prontos para modelagem.
  - **database/**: Bancos de dados em formato SQLite.
- **docs/**: Documentação adicional (chaves de leitura, dicionários) e guias do projeto.
- **notebooks/**: Fluxo principal de análise em cadernos numerados:
  - `01_extracao_pre_processamento.ipynb`
  - `02_analise_exploratoria_bivariada.ipynb`
  - `03_machine_learning_capto.ipynb`
- **scripts/**: Scripts Python utilitários.
- **src/**: Código-fonte modular e funções reutilizáveis.

## Principais Arquivos

- `notebooks/01_extracao_pre_processamento.ipynb`: Início do fluxo, realiza o carregamento e filtro dos dados brutos para a amostra de idosos.
- `scripts/criar_banco_formatado.py`: Script original para criação de um banco SQLite mapeado.
- `data/raw/pns2019.csv`: Base de dados principal em formato CSV (não incluída no repositório remoto).

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