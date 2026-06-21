# Projeto PNS 2019 – Artrite e Reumatismo em Idosos Brasileiros

Projeto de Mineração de Dados (PUC Minas – Semestre 3) que investiga o perfil de idosos brasileiros (≥ 60 anos) com artrite/reumatismo utilizando os microdados da Pesquisa Nacional de Saúde (PNS) 2019.

**Autor:** Pedro Dias Soares  
**Orientador:** Prof. Dr. Luis Enrique Zárate – PUC Minas  
**Metodologia:** CRISP-DM / framework CAPTO / PICOS / STROBE

---

## Estrutura do Repositório

```
Projeto_PNS/
├── data/                     ← dados (.db/.csv NÃO versionados – ver .gitignore)
│   ├── raw/                  ← brutos (pns2019.csv / PNS_2019.txt baixados do IBGE)
│   ├── processed/csv/        ← CSVs-semente dos 4 grupos (regeneram os .db)
│   ├── database/             ← bancos SQLite derivados (gerados pelo NB01 / preparar_bancos.py)
│   └── results/
│       ├── preprocessing/ · preprocessing_comorbidades/ · preprocessing_desenho3/
│       ├── discretizacao/ · discretizacao_comorbidades/
│       ├── eda/ · eda_comorbidades/
│       └── modelagem/ · bases_finais/
├── notebooks/
│   ├── 01_extracao_pre_processamento.ipynb
│   ├── 02_analise_exploratoria_bivariada.ipynb     ← EDA bivariada – Desenho 1
│   ├── 02b_analise_exploratoria_comorbidades.ipynb ← EDA bivariada – Desenho 2
│   ├── 03_preprocessamento_v3.ipynb            ← Desenho 1 – artrite pura
│   ├── 03b_preprocessamento_comorbidades.ipynb ← Desenho 2 – artrite + comorbidades
│   ├── 03c_preprocessamento_desenho3.ipynb     ← Desenho 3 – carga de comorbidade (eixo nutricional)
│   ├── 04_discretizacao.ipynb                  ← discretização (faixas de domínio + plano cartesiano)
│   ├── 05_exportacao_bases.ipynb               ← exporta bases finais (.db + .csv) dos 2 desenhos
│   ├── 06_modelagem_ml.ipynb                   ← seleção por entropia / modelagem
│   ├── nutricao.py                             ← módulo do eixo nutricional (IRNI + cluster)
│   └── preparar_bancos.py                      ← bootstrap: regenera os .db ausentes a partir dos CSVs-semente
├── docs/                     ← TODA a documentação consolidada
│   ├── artigo/               ← artigo atual (v6, v5_REEXECUTADO) + versoes_antigas/
│   ├── apresentacoes/        ← pptx do NB06 + apresentacao_nb04/ (deck + figuras)
│   ├── guias/                ← guias de redação/análise, plano, template, resultados consolidados
│   ├── referencia_pns/       ← dicionário, questionário, Chaves_PNS, relatório de variáveis
│   ├── figuras_artigo/       ← fluxograma_pipeline_kdd.png (KDD, 4 fases / 10 etapas)
│   ├── avaliacoes/           ← avaliações dos notebooks
│   ├── spec_nutricao_desenho3.md
│   ├── analise_projeto_pns.md · plano_reestruturacao.md · proxima_fase.md
├── archive/                  ← backups (não versionado)
├── config.toml               ← Parâmetros centrais (hiperparâmetros, cores, cortes de discretização)
├── pyproject.toml            ← Dependências e metadados (pip install -e .)
├── README.md · .gitignore · .gitattributes
```

> **Configuração central (`config.toml`).** Os hiperparâmetros (`random_state`, `alpha`,
> `limite_missing`, `limite_iqr_mult`, limiares de entropia/correlação), as cores dos gráficos e
> os **cortes de discretização com a sua fonte oficial** ficam num único `config.toml`, lido pelos
> notebooks 02–05. Para mudar uma semente ou um corte de domínio, edite o `config.toml` — não os
> notebooks. Leitura via `tomllib` (Python 3.11+, stdlib) ou `tomli` (Python 3.10).

---

## Pipeline KDD – 10 Etapas / 4 Fases

| Fase | Etapas | Status |
|------|--------|--------|
| **Fase 1** – Entendimento do problema (CAPTO) | 1. Contexto · 2. Perguntas PICOS · 3. Seleção de variáveis | Concluído |
| **Fase 2** – Pré-processamento | 4. Skip patterns · 5. Missing (>75%) · 6. Outliers · 7. Imputação | Concluído |
| **Fase 3** – Preparação para mineração | 8. Feature engineering · 9. Encoding (OHE) · 10. Discretização (NB04) · 11. Exportação das bases finais (NB05) | Concluído |
| **Fase 4** – Modelagem e avaliação | 12. ML — Reg. Logística, Árvore, Random Forest (NB06) | **Pendente** |

---

## Dois Desenhos de Estudo

### Desenho 1 – Artrite Pura (`03_preprocessamento_v3.ipynb`)
- **Critério:** `Q079 = Sim` **e** as demais 13 doenças crônicas = Não (artrite isolada)
- **Amostra:** 4 826 registros · 70 features (→ 57 após discretização no NB04)
- **Distribuição:** 4 332 saudáveis vs 494 artrite (razão 8,77:1 – desbalanceado)
- **Dataset:** `data/results/preprocessing/dataset_preprocessado.csv`

### Desenho 2 – Artrite com Comorbidades (`03b_preprocessamento_comorbidades.ipynb`)
- **Critério:** `Q079 = Sim` com qualquer combinação de outras doenças crônicas
- **Amostra:** 8 357 registros · 68 features (→ 55 após discretização no NB04)
- **Distribuição:** 4 332 saudáveis vs 4 025 artrite (razão 1,08:1 – quase balanceado)
- **Comorbidades prevalentes:** hipertensão 65,3% · colesterol alto 39,8% · diabetes 21,9% · depressão 19,5%
- **Dataset:** `data/results/preprocessing_comorbidades/dataset_preprocessado.csv`

---

## Decisões de Pré-processamento (Desenho 1)

| Etapa | Decisão | Resultado |
|-------|---------|-----------|
| Skip patterns | Preenchimento condicional (P035, P029, J012, G060/G062…) | 29 274 NaN estruturais resolvidos |
| Missing >75% | Exclusão da variável | 12 variáveis removidas |
| Outliers | IQR×3 por classe → substituído por NaN → imputação por média global | 4 valores tratados (só contínuas: peso/altura/idade) |
| Imputação | Média/moda **global** (target-blind, não usa o alvo) | 9 633 valores imputados |
| Feature eng. | IMC · Escore Inflamatório · Escore Saudável · Razão Inf/Saud | 4 features criadas |
| Encoding | OHE em 31 + Label Encoding em 4 variáveis | Dataset final 4 826 × 70 |

---

## Como Reproduzir

```bash
# Clonar o repositório
git clone https://github.com/pedrinndias/Projeto-PNS-2019.git

# Instalar dependências (lê o pyproject.toml)
pip install -e .

# Preparar os bancos derivados (.db são gitignored). Regenera a partir dos
# CSVs-semente em data/processed/csv/ — os notebooks NB01–03c também fazem
# isso sozinhos (bootstrap) se algum .db faltar.
python notebooks/preparar_bancos.py

# Executar os notebooks em ordem
jupyter notebook notebooks/01_extracao_pre_processamento.ipynb
jupyter notebook notebooks/02_analise_exploratoria_bivariada.ipynb     # EDA Desenho 1
jupyter notebook notebooks/02b_analise_exploratoria_comorbidades.ipynb # EDA Desenho 2
jupyter notebook notebooks/03_preprocessamento_v3.ipynb            # Desenho 1
jupyter notebook notebooks/03b_preprocessamento_comorbidades.ipynb # Desenho 2
jupyter notebook notebooks/03c_preprocessamento_desenho3.ipynb     # Desenho 3 (eixo nutricional)
jupyter notebook notebooks/04_discretizacao.ipynb                  # discretização (ambos)
jupyter notebook notebooks/05_exportacao_bases.ipynb              # bases finais (.db + .csv)
jupyter notebook notebooks/06_modelagem_ml.ipynb                  # seleção por entropia / modelagem
```

---

## Dados

- **Fonte:** [IBGE – Pesquisa Nacional de Saúde 2019](https://www.ibge.gov.br/estatisticas/sociais/saude/9160-pesquisa-nacional-de-saude.html)
- `pns2019.csv` não é versionado por tamanho (~700 MB). Baixar diretamente no IBGE e colocar em `data/raw/`.
- Bancos SQLite intermediários (`data/database/*.db`) também não são versionados.

---

## Requisitos Principais

- Python 3.10+ (no 3.10, instale `tomli` para ler o `config.toml`; no 3.11+ já vem no `tomllib`)
- pandas · numpy · matplotlib · seaborn · scikit-learn · nbformat · python-docx · imbalanced-learn

Ver lista completa em `pyproject.toml` (`[project.dependencies]`).
