# Plano de Reestruturação do Projeto PNS 2019

> ⚠️ **DOCUMENTO DESCONTINUADO (30/05/2026).** A reestruturação descrita aqui foi concluída e este plano não reflete mais o estado atual. Em particular: os scripts `build_*.py`/utilitários listados abaixo **foram removidos do repo**; o balanceamento adotado é **RUS** (não SMOTE); o **NB04 passou a ser de discretização** e o ML vai para o **NB05**.
> **Use no lugar deste:** [`analise_projeto_pns.md`](analise_projeto_pns.md) (estado atual) e [`../proxima_fase.md`](../proxima_fase.md) (roadmap). Mantido apenas como registro histórico.

---

**Última atualização original:** 18/05/2026  
**Status geral:** Pré-processamento concluído. Fase de Modelagem (ML) pendente.

---

## Situação Atual

### O que foi feito

| Etapa | Descrição | Status |
|-------|-----------|--------|
| Estrutura de pastas | `data/`, `notebooks/`, `scripts/`, `docs/`, `.gitignore` | Concluído |
| `01_extracao_pre_processamento.ipynb` | Carga, filtro de idosos ≥60 anos, criação do target Q079 | Concluído |
| `02_analise_exploratoria_bivariada.ipynb` | Testes qui-quadrado, Mann-Whitney, gráficos EDA | Concluído |
| `03_preprocessamento_v3.ipynb` | Pipeline completo – **Desenho 1: artrite pura** | Concluído |
| `03b_preprocessamento_comorbidades.ipynb` | Pipeline completo – **Desenho 2: artrite + comorbidades** | Concluído |
| Fluxograma KDD | PNG horizontal 4 fases/10 etapas (`figuras_artigo/`) | Concluído |
| Scripts reproduzíveis | `build_nb03.py`, `build_nb03b.py`, `build_fluxograma_pipeline.py` | Concluído |
| Documentação do artigo | Template, guia de redação, resultados consolidados (`.docx`) | Concluído |

### O que está pendente

| Próxima etapa | Descrição |
|---------------|-----------|
| Notebook 04 – ML | Regressão Logística, Árvore de Decisão, Random Forest |
| Balanceamento | SMOTE / RUS para o Desenho 1 (razão 8,77:1) |
| Avaliação | Matrizes de confusão, curva ROC, AUC, feature importance |
| Artigo | Redigir seções Resultados e Discussão com base nos achados do ML |

---

## Estrutura de Diretórios Atual

```
Projeto_PNS/
├── data/
│   ├── raw/                            ← pns2019.csv (não versionado)
│   └── results/
│       ├── preprocessing/              ← Dataset Desenho 1 (4 826 × 49)
│       ├── preprocessing_comorbidades/ ← Dataset Desenho 2 (8 357 × 57)
│       └── eda/                        ← Figuras EDA
├── Documentos_organizacao/
│   ├── figuras_artigo/
│   │   └── fluxograma_pipeline_kdd.png
│   ├── Artigo_Template_de_Trabalho_PNS2019.docx
│   ├── Guia_Redacao_Artigo_PNS2019.docx
│   ├── Guia_Analises_Relatorios_PNS2019_Artrite.docx
│   ├── Plano_Artigo_Mineracao_Pedro_Dias_Soares.docx
│   └── Resultados_Consolidados_PNS2019_Artrite.docx
├── notebooks/
│   ├── 01_extracao_pre_processamento.ipynb
│   ├── 02_analise_exploratoria_bivariada.ipynb
│   ├── 03_preprocessamento_v3.ipynb
│   └── 03b_preprocessamento_comorbidades.ipynb
├── scripts/
│   ├── build_nb03.py
│   ├── build_nb03b.py
│   ├── build_fluxograma_pipeline.py
│   ├── build_guia_redacao.py
│   ├── build_documento_resultados.py
│   ├── build_template_trabalho.py
│   ├── criar_banco_formatado.py
│   └── rastrear_registros_nulos.py
├── docs/
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Datasets Finais Gerados

### Desenho 1 – Artrite Pura

- **Arquivo:** `data/results/preprocessing/dataset_preprocessado.csv`
- **Dimensões:** 4 826 registros × 49 features
- **Target:** 0 = saudável (4 332) · 1 = artrite (494)
- **Razão:** 8,77:1 (desbalanceado – requer SMOTE/RUS no ML)
- **Variáveis excluídas (>75% missing):** 13 variáveis removidas
- **Imputações realizadas:** 27 455 valores (média/moda por classe)
- **Features sintéticas:** IMC · Escore Inflamatório · Escore Saudável · Razão Inf/Saud
- **Encoding:** OHE em 22 variáveis categóricas

### Desenho 2 – Artrite com Comorbidades

- **Arquivo:** `data/results/preprocessing_comorbidades/dataset_preprocessado.csv`
- **Dimensões:** 8 357 registros × 57 features
- **Target:** 0 = saudável (4 332) · 1 = artrite (4 025)
- **Razão:** 1,08:1 (quase balanceado – não requer SMOTE)
- **NaN estruturais:** 1 489 preenchidos por skip patterns
- **Variáveis excluídas (>75% missing):** 16 variáveis removidas
- **Comorbidades documentadas (Etapa 3.5):** hipertensão 65,3% · colesterol 39,8% · diabetes 21,9% · depressão 19,5%

---

## Pipeline KDD – Visão Geral

```
Fase 1 – Entendimento         Fase 2 – Pré-processamento
  Etapa 1: Contexto      →      Etapa 4: Skip patterns
  Etapa 2: PICOS         →      Etapa 5: Missing >75%
  Etapa 3: Variáveis     →      Etapa 6: Outliers (IQR×3)
                                Etapa 7: Imputação

Fase 3 – Preparação           Fase 4 – Modelagem [PENDENTE]
  Etapa 8: Feature eng.  →      Etapa 10: Modelos ML
  Etapa 9: Encoding OHE
```

Fluxograma gerado em: `Documentos_organizacao/figuras_artigo/fluxograma_pipeline_kdd.png`  
Script reproduzível: `scripts/build_fluxograma_pipeline.py`

---

## Próximos Passos – Fase de Modelagem

### Notebook 04 (a criar) – Machine Learning

**Entrada:** `data/results/preprocessing/dataset_preprocessado.csv` (Desenho 1) ou variante de comorbidades.

**Estrutura sugerida:**

```
Etapa 10.1  Divisão treino/teste (80/20, stratified, random_state=42)
Etapa 10.2  Balanceamento – SMOTE no treino (Desenho 1 apenas)
Etapa 10.3  Regressão Logística – baseline interpretável
Etapa 10.4  Árvore de Decisão – regras explícitas para o artigo
Etapa 10.5  Random Forest – melhor desempenho preditivo
Etapa 10.6  Avaliação – Accuracy, Precision, Recall, F1, AUC-ROC
Etapa 10.7  Feature Importance – quais variáveis predizem artrite?
Etapa 10.8  Comparação entre os dois desenhos de estudo
```

**Artefatos esperados:**
- Matrizes de confusão (PNG) → `data/results/eda/`
- Curvas ROC (PNG)
- Tabela comparativa de métricas (exportar para `.docx` / atualizar `Resultados_Consolidados`)
- Regras da Árvore de Decisão (texto)

---

## Histórico de Reestruturação (Concluído)

O plano original de reestruturação de pastas foi **integralmente executado**:

- [x] Criadas as pastas `data/raw/`, `data/results/`, `scripts/`, `docs/`
- [x] Notebooks renumerados e com nomes descritivos
- [x] `.gitignore` atualizado (ignora `.csv`, `.db`, `.venv`, `archive/`)
- [x] Scripts utilitários organizados em `scripts/`
- [x] Documentação centralizada em `Documentos_organizacao/`
- [x] Notebooks gerados por scripts reproduzíveis (`build_nb03.py`, `build_nb03b.py`)
