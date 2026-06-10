# Próxima Fase — Modelagem ML (Notebook 06)

> **Última atualização:** 08/06/2026
> **Pré-requisito:** Notebooks 01–05 concluídos e **reexecutados em 10/06** (correção dos skip patterns + imputação global target-blind + skip na EDA); `data/results/` regenerado e versionado
> **Documentos relacionados:** [`README.md`](README.md) · [`Documentos_organizacao/analise_projeto_pns.md`](Documentos_organizacao/analise_projeto_pns.md)

> **Histórico:** o `04_eliminacao_outliers.ipynb` foi removido (outliers seguem embutidos no NB03/NB03b, IQR×3 por classe). O **Notebook 04 é a discretização** (faixas de domínio + plano cartesiano) e o **Notebook 05 é a exportação das bases finais** — ambos **concluídos**. A modelagem de ML é o **Notebook 06** (a criar).

---

## 0. Passo imediato — criar o NB06

✅ **Reexecução concluída (10/06).** O pipeline `02 → 03 → 03b → 04 → 05` foi reexecutado após as correções de 10/06 (skip patterns das perguntas-pai textuais, imputação **global target-blind**, skip P035←P034 na EDA incl. Tab 3-A). `data/results/` e as bases finais já estão regenerados e versionados. O NB06 consome diretamente o `dataset_discretizado.csv` atualizado — **não há mais reexecução pendente**.

- ✅ **NB04 — Discretização (concluído):** faixas de domínio (OMS/Guia AF BR/NIAAA) + plano cartesiano dos padrões alimentares (Ribeiro & Zárate, 2019). Entrada: datasets pré-processados; saída: dataset discretizado + relatório JSON de cortes.
- ✅ **NB05 — Exportação (concluído):** 2 `.db` + 2 `.csv` + Excel das bases finais dos dois desenhos.

---

## 1. Onde estamos

Os notebooks 03 e 03b já entregam datasets **prontos para ML**:

| Desenho | Arquivo (não versionado) | n × p | Distribuição (0/1) | Razão |
|---------|--------------------------|-------|--------------------|-------|
| 1 — Artrite Pura | `data/results/preprocessing/dataset_preprocessado.csv` | 4 826 × 70 (→ 57 NB04) | 4 332 / 494 | 8,77:1 |
| 2 — Artrite c/ Comorbidades | `data/results/preprocessing_comorbidades/dataset_preprocessado.csv` | 8 357 × 68 (→ 55 NB04) | 4 332 / 4 025 | 1,08:1 |

Cada CSV traz `X` (features encoded) + coluna `Label` (0 = saudável, 1 = artrite). Não há mais NaN, não há mais outliers extremos, encoding já feito. O NB06 consome o **dataset discretizado** (saída do NB04).

> ✅ Números **pós-reexecução (10/06)**. Anti-leakage do D2 = 13 Q* + 5 exames removidos. Os skips agora preenchem P035/P029/G060/G062/P02801/P03201 (antes descartados por >75% missing), por isso `p` subiu vs. versões antigas.

---

## 2. Notebook 06 — esqueleto proposto (ML)

```
notebooks/06_modelagem_ml.ipynb
│
├── 1. Configuração
│     • Imports (scikit-learn, imblearn, scipy.stats)
│     • RANDOM_STATE = 42, ALPHA = 0.05
│     • Caminhos para os dois datasets
│
├── 2. Carregamento e split
│     • read_csv dos dois desenhos
│     • train_test_split(80/20, stratify=y, random_state=42)
│     • Salvar índices para reprodutibilidade
│
├── 3. Pipeline com RUS interno (Desenho 1)
│     • imblearn.Pipeline:
│       [RandomUnderSampler] → [Modelo]
│     • Aplicado APENAS no treino, dentro de cada fold da CV
│       (evita vazamento; o teste fica desbalanceado, como no mundo real)
│
├── 4. Modelos a treinar (em ambos os desenhos)
│     • 4.1 Regressão Logística — baseline interpretável (OR + IC 95%)
│     • 4.2 Árvore de Decisão (max_depth=5) — regras explícitas
│     • 4.3 Random Forest (n_estimators=300) — melhor desempenho
│     • (Opcional) Naive Bayes · AdaBoost · MLP — para comparação
│
├── 5. Otimização de hiperparâmetros
│     • RandomizedSearchCV(cv=StratifiedKFold(5), scoring='f1_macro')
│     • n_iter=30, random_state=42
│
├── 6. Avaliação (10-fold CV)
│     • Stratified 10-fold no conjunto de treino
│     • Por fold: Accuracy, Precision, Recall, F1-macro, AUC-ROC
│     • Reportar Média ± IC 95%
│
├── 7. Avaliação no conjunto de teste (hold-out 20%)
│     • Matriz de confusão por classe
│     • Curva ROC + AUC
│     • Classification report
│
├── 8. Comparação estatística entre modelos
│     • Teste t pareado nos 10 folds (Logística vs Árvore vs RF)
│     • Correção de Bonferroni
│
├── 9. Interpretabilidade
│     • 9.1 Feature importance — Gini/MDI para árvores
│     • 9.2 Coeficientes da Logística (com IC 95%)
│     • 9.3 Extração das regras da árvore (texto + visualização)
│     • 9.4 Agrupamento por dimensão CAPTO (Hábitos · Sociodemográficos · Antropometria · Comorbidades)
│
├── 10. (Revisado) Sem "Modelo A vs B" — anti-leakage já no NB03b
│     • As Q* e exames condicionais são removidos das features no NB03b (filtro de coorte).
│     • A comparação relevante é entre DESENHOS (§11), não entre com/sem Q* dentro do D2.
│
├── 11. Comparação dos dois desenhos
│     • Tabela: métricas do Desenho 1 (artrite pura) vs Desenho 2 (com comorbidades)
│     • Discussão: ganho de poder estatístico vs vazamento metodológico
│
└── 12. Exportação
      • data/results/modelagem/metrics.json    — métricas consolidadas
      • data/results/modelagem/figuras/*.png   — matriz confusão, ROC, importâncias
      • data/results/modelagem/regras_arvore.txt
```

---

## 3. Decisões fixadas

Essas decisões já foram tomadas e ficam registradas para evitar retrabalho:

| Decisão | Valor | Motivo |
|---------|-------|--------|
| Desenhos | **C** — treinar e comparar os dois | Triangulação metodológica; Desenho 1 = limpo; Desenho 2 = poder estatístico |
| Q* como features | **Não** em nenhum desenho — removidas no NB03b (anti-leakage; + exames condicionais) | Q* definem a coorte, não o modelo — evita vazamento circular |
| Tratamento de missing | **Imputação global (target-blind)** (média/moda) após corte de >75% NaN | Sem vazamento do alvo no dataset de ML; já no NB03/NB03b |
| Outliers | **IQR × 3,0 por classe → NaN → média global** | ~3,3 σ; já feito no NB03/NB03b |
| Discretização | **Sim** — IMC-OMS, faixa etária, atividade física, escore inflamatório | Melhor interpretabilidade das regras (CAPTO) |
| Mediana do plano alimentar | **Reajustar _in-fold_ no NB06** (só no treino) | Único corte data-driven do NB04 (3.4); evita vazamento não-supervisionado |
| Split | **80/20 estratificado**, `random_state=42` | Padrão da literatura PUC Minas |
| Balanceamento | **RUS dentro de cada fold da CV** (não fora) | Evita vazamento; padrão Cancella |
| Métrica-alvo | **F1-macro** | Robusta a desbalanceamento (Desenho 1) |
| Onde mora o ML | **`notebooks/06_modelagem_ml.ipynb`** | NB04 = discretização; NB05 = exportação; ML separado no NB06 |

---

## 4. Artefatos esperados ao final do NB06

```
data/results/modelagem/
├── metrics.json                          ← Métricas dos 6 modelos (3 algoritmos × 2 desenhos)
├── regras_arvore_desenho1.txt
├── regras_arvore_desenho2.txt
├── feature_importance_consolidada.csv
└── figuras/
    ├── matriz_confusao_logreg_d1.png
    ├── matriz_confusao_arvore_d1.png
    ├── matriz_confusao_rf_d1.png
    ├── (idem para Desenho 2)
    ├── curva_roc_comparativa.png
    └── feature_importance_top15.png
```

Esses artefatos alimentam:
- A seção **Resultados** do artigo (template já pronto em `Documentos_organizacao/Artigo_Template_de_Trabalho_PNS2019.docx`)
- A atualização manual do `Resultados_Consolidados_PNS2019_Artrite.docx` com as métricas e figuras do ML

---

## 5. Checklist

**Pré-processamento / Discretização / Exportação:**
- [x] `04_discretizacao.ipynb` criado (faixas de domínio + plano cartesiano)
- [x] `05_exportacao_bases.ipynb` criado (bases finais .db/.csv)
- [x] Alinhamento D1×D2 + anti-leakage de exames (08/06)
- [x] Correção skip patterns + imputação global target-blind + skip na EDA (10/06)
- [x] **Reexecutado** `02 → 03 → 03b → 04 → 05` e commitado `data/results/` regenerado (10/06)

**Modelagem (NB06):**
- [ ] Criar `notebooks/06_modelagem_ml.ipynb` seguindo o esqueleto da §2
- [ ] Consumir o dataset discretizado nos dois desenhos

---

## 6. Depois do NB06 — fechamento do projeto

1. **Atualizar** `Resultados_Consolidados_PNS2019_Artrite.docx` com as métricas e figuras do ML.
2. **Redigir** as seções pendentes do artigo (Resultados → Discussão → Introdução → Resumo), seguindo o template em `Artigo_Template_de_Trabalho_PNS2019.docx` e o guia em `Guia_Redacao_Artigo_PNS2019.docx`.
3. **Preencher** o checklist STROBE (22 itens) — referência teórica registrada no orientador.
4. **Revisão final** com o Prof. Zárate antes de submissão ao JHI/SBIS.

---

*Documento atualizado em 10/06/2026: skip patterns das perguntas-pai textuais corrigidos (NB03/03b), imputação trocada para global target-blind, skip P035←P034 aplicado na EDA (NB02 incl. Tab 3-A). Pipeline `02→03→03b→04→05` reexecutado e `data/results/` regenerado/versionado. Dims atuais: D1 4 826×70→57, D2 8 357×68→55. Resta apenas a modelagem (NB06).*
