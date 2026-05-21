# Análise do Projeto PNS 2019
## Mineração de Dados — Pedro Dias Soares

> **Última atualização:** 21/05/2026
> **Documento companheiro:** [`plano_reestruturacao.md`](plano_reestruturacao.md) (estado atual da estrutura) · [`../proxima_fase.md`](../proxima_fase.md) (roadmap da Fase 4)

---

## 1. Visão geral

| Item | Detalhe |
|------|---------|
| **Objetivo** | Caracterizar idosos brasileiros (≥60 anos) com artrite/reumatismo e construir um classificador supervisionado a partir dos microdados da PNS 2019 |
| **Base de dados** | Pesquisa Nacional de Saúde 2019 (IBGE) — ~293.726 registros, 1.087 colunas |
| **Linguagem** | Python 3.10+ (pandas, numpy, matplotlib, seaborn, scipy, statsmodels, scikit-learn) |
| **Armazenamento intermediário** | SQLite (banco mestre formatado, ~1,1 GB — não versionado) |
| **Metodologia** | KDD · CRISP-DM · CAPTO (Zárate et al.) · PICOS · STROBE |
| **Periódico-alvo** | Journal of Health Informatics (JHI/SBIS) |
| **Orientador** | Prof. Dr. Luis Enrique Zárate — PUC Minas |

---

## 2. Estrutura atual do repositório

```
Projeto_PNS/
├── data/
│   ├── raw/               ← CSV/dicionário/inputs SAS (não versionados)
│   └── results/
│       ├── preprocessing/             ← Desenho 1 — artrite pura
│       ├── preprocessing_comorbidades/← Desenho 2 — artrite + comorbidades
│       └── eda/                       ← Figuras da EDA bivariada
├── Documentos_organizacao/
│   ├── figuras_artigo/                ← Fluxograma KDD
│   ├── Dados PNS/                     ← Questionário, dicionário, relatório de variáveis
│   ├── Avalição Notebooks/            ← Avaliação final do NB02
│   ├── analise_projeto_pns.md         ← ESTE arquivo
│   ├── plano_reestruturacao.md
│   ├── Artigo_Template_de_Trabalho_PNS2019.docx
│   ├── Guia_Redacao_Artigo_PNS2019.docx
│   ├── Guia_Analises_Relatorios_PNS2019_Artrite.docx
│   ├── Plano_Artigo_Mineracao_Pedro_Dias_Soares.docx
│   └── Resultados_Consolidados_PNS2019_Artrite.docx
├── notebooks/
│   ├── 01_extracao_pre_processamento.ipynb
│   ├── 02_analise_exploratoria_bivariada.ipynb
│   ├── 03_preprocessamento_v3.ipynb           ← Desenho 1
│   └── 03b_preprocessamento_comorbidades.ipynb ← Desenho 2
├── scripts/
│   ├── criar_banco_formatado.py
│   ├── build_nb03.py / build_nb03b.py         ← Geram os notebooks idempotentemente
│   ├── build_fluxograma_pipeline.py
│   ├── build_documento_resultados.py
│   ├── build_guia_redacao.py
│   ├── build_template_trabalho.py
│   ├── apply_fixes.py
│   └── rastrear_registros_nulos.py
├── docs/
│   └── Chaves_PNS_2019.pdf
├── README.md
├── requirements.txt
├── proxima_fase.md
└── .gitignore
```

### 2.1 Avaliação da estrutura

| Aspecto | Status | Comentário |
|---------|--------|------------|
| Organização de diretórios | ✅ | Pipeline `data/ → notebooks/ → scripts/ → Documentos_organizacao/` claro |
| `.gitignore` | ✅ | Ignora `.csv`, `.db`, `.venv`, settings locais. Tem algumas linhas duplicadas (cosmético) |
| `requirements.txt` | ⚠️ | Falta `nbformat` (usado em `build_nb03*.py`) e `xlrd` (usado em `criar_banco_formatado.py` para ler `.xls`) |
| README | ✅ | Atualizado, descreve os dois desenhos de estudo |
| Notebooks 01–03b | ✅ | Executados sem erros, com células markdown explicativas em cada etapa |
| Rastreabilidade (JSON) | ✅ | `relatorio_preprocessamento.json` em cada pasta de resultado |
| Scripts reproduzíveis | ✅ | `build_nb03.py` / `build_nb03b.py` regeneram os notebooks do zero |

---

## 3. Pipeline KDD — situação por fase

| Fase | Etapas | Status |
|------|--------|--------|
| **Fase 1** · Entendimento (CAPTO) | 1. Contexto · 2. PICOS · 3. Seleção de variáveis | ✅ Concluído |
| **Fase 2** · Pré-processamento | 4. Skip patterns · 5. Missing >75% · 6. Outliers IQR×3 · 7. Imputação | ✅ Concluído |
| **Fase 3** · Preparação | 8. Feature engineering (IMC, escores) · 9. Encoding OHE | ✅ Concluído |
| **Fase 4** · Modelagem e avaliação | 10. ML — Reg. Logística · Árvore · Random Forest | 🔴 **Pendente — próximo passo** |

Fluxograma: [`figuras_artigo/fluxograma_pipeline_kdd.png`](figuras_artigo/fluxograma_pipeline_kdd.png) · regerado por `python scripts/build_fluxograma_pipeline.py`.

---

## 4. Dois desenhos de estudo

| Aspecto | Desenho 1 — Artrite Pura | Desenho 2 — Artrite c/ Comorbidades |
|---------|--------------------------|--------------------------------------|
| Notebook | `03_preprocessamento_v3.ipynb` | `03b_preprocessamento_comorbidades.ipynb` |
| Critério | `Q079 = Sim` e demais 13 doenças = Não | `Q079 = Sim` com qualquer combinação |
| n casos | 494 | 4 025 |
| n controles | 4 332 | 4 332 |
| Razão | 8,77:1 (desbalanceado) | 1,08:1 (quase balanceado) |
| Features | 49 | 57 |
| Vars Q* | Constantes → removidas | Mantidas como features |
| Skip patterns | 1 344 NaN preenchidos | 1 489 NaN preenchidos |
| Vars excluídas (>75% NaN) | 13 | 16 |
| Outliers tratados (IQR×3) | 50 | 208 |
| Valores imputados | 27 455 | 29 768 |
| Risco metodológico | Amostra pequena para ML | **Data leakage circular nas Q*** (ver Etapa 0 do NB03b) |

Comorbidades mais prevalentes no Desenho 2: hipertensão 65,3% · colesterol alto 39,8% · diabetes 21,9% · depressão 19,5%.

---

## 5. Decisões metodológicas registradas

| Etapa | Decisão | Justificativa |
|-------|---------|---------------|
| Faixa etária | ≥ 60 anos (idosos) | Alinhado com Cancella (2025) e Plano do Artigo |
| Limite de missing | Excluir variável se > 75% NaN | Padrão Cancella (60%) flexibilizado para preservar variáveis-chave |
| Outliers | IQR × 3,0 por classe → substituir por limite | ~3,3 σ na normal; conservador (Hipertensão/DPOC usam 1,5×) |
| Imputação | Média (numérica) / Moda (categórica) **por classe** | Preserva n; estratificada para não vazar informação |
| Categorização | Faixa etária, IMC-OMS, atividade física, escore inflamatório | Padrão CAPTO/STROBE — facilita interpretabilidade das regras |
| Encoding | OHE com `drop_first=True, dtype=int` (nominais) | Compatível com Logistic Regression e árvores |
| Balanceamento | RUS **dentro de cada fold da CV** (NB04) | Evita vazamento entre treino e teste |
| Random state | `42` em tudo | Reprodutibilidade |

---

## 6. Pontos de atenção atuais

### 🔴 Bug ativo

| # | Arquivo | Problema |
|---|---------|----------|
| 1 | `scripts/rastrear_registros_nulos.py` | Usa `df_bem`, `df_atri_reu`, `df_atri_reu_puro` sem definir. `NameError` se rodado standalone. Solução: carregar bases do SQLite no topo, ou mover o conteúdo para uma célula do NB01. |

### 🟡 Pendências cosméticas / má prática

| # | Arquivo | Observação |
|---|---------|------------|
| 2 | `requirements.txt` | Adicionar `nbformat` (build dos notebooks) e `xlrd` (leitura do dicionário `.xls`) |
| 3 | `scripts/criar_banco_formatado.py` | `except:` bare na linha 54 — trocar por `except (ValueError, TypeError)` |
| 4 | `.gitignore` | Linhas redundantes (`*.csv` e `*.db` aparecem 2× cada); `archive/` referencia pasta que não existe |
| 5 | `data/raw/input_PNS_2019.sas` ↔ `.txt` | Idênticos exceto pelo `\n` final — manter só um |
| 6 | `dicionario_PNS_microdados_2019.xls` | Duplicado em `data/raw/` e `Documentos_organizacao/Dados PNS/` |

### 🟢 Risco metodológico documentado

| # | Observação |
|---|------------|
| 7 | **Data leakage circular no Desenho 2:** as variáveis Q* foram usadas para definir o controle "saudável" (todas Q* = Não) e simultaneamente entram como features no NB03b. Os modelos terão acurácia inflada — discutir como limitação no artigo. Mitigação prevista no NB04: treinar Modelo A (com Q*) e Modelo B (sem Q*) para análise de sensibilidade. |

---

## 7. Progresso geral

| Eixo | Status |
|------|:------:|
| Compreensão do problema (CAPTO/PICOS) | ✅ 100% |
| ETL e bases SQLite | ✅ 100% |
| EDA bivariada (NB02) | ✅ 100% |
| Pré-processamento — Desenho 1 (NB03) | ✅ 100% |
| Pré-processamento — Desenho 2 (NB03b) | ✅ 100% |
| Documentação (template, guias, resultados consolidados) | ✅ 100% |
| **Modelagem ML (NB04)** | 🔴 **0%** |
| Avaliação e feature importance | 🔴 0% |
| Redação do artigo (Resultados/Discussão) | 🔴 0% |

**Progresso geral estimado:** ~70% — falta a fase de modelagem e a escrita do artigo.

---

## 8. Próximos passos

Detalhamento em [`../proxima_fase.md`](../proxima_fase.md). Em resumo:

1. **Corrigir** o `rastrear_registros_nulos.py` (ou remover).
2. **Completar** `requirements.txt` com `nbformat` e `xlrd`.
3. **Criar** `notebooks/04_modelagem_ml.ipynb` — pipeline ML rodando nos dois desenhos.
4. **Atualizar** o `Resultados_Consolidados_PNS2019_Artrite.docx` com as métricas do ML.
5. **Redigir** as seções de Resultados e Discussão do artigo.

---

*Documento atualizado em 21/05/2026 substituindo a versão original de 09/05/2026.*
