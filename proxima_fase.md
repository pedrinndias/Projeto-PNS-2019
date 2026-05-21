# Próxima Fase — Modelagem com Machine Learning (Notebook 04)

> **Última atualização:** 21/05/2026
> **Pré-requisito:** Notebooks 01–03b concluídos · datasets pré-processados disponíveis em `data/results/preprocessing/` e `data/results/preprocessing_comorbidades/`
> **Documentos relacionados:** [`README.md`](README.md) · [`Documentos_organizacao/plano_reestruturacao.md`](Documentos_organizacao/plano_reestruturacao.md) · [`Documentos_organizacao/analise_projeto_pns.md`](Documentos_organizacao/analise_projeto_pns.md)

---

## 1. Onde estamos

Os notebooks 03 e 03b já entregam datasets **prontos para ML**:

| Desenho | Arquivo (não versionado) | n × p | Distribuição (0/1) | Razão |
|---------|--------------------------|-------|--------------------|-------|
| 1 — Artrite Pura | `data/results/preprocessing/dataset_preprocessado.csv` | 4 826 × 49 | 4 332 / 494 | 8,77:1 |
| 2 — Artrite c/ Comorbidades | `data/results/preprocessing_comorbidades/dataset_preprocessado.csv` | 8 357 × 57 | 4 332 / 4 025 | 1,08:1 |

Cada CSV traz `X` (features encoded) + coluna `Label` (0 = saudável, 1 = artrite). Não há mais NaN, não há mais outliers extremos, encoding já feito.

> A "preparação para ML" prevista em discussões antigas (notebook 02b separado) foi **incorporada dentro do NB03/NB03b** — não há etapa intermediária pendente.

---

## 2. Notebook 04 — esqueleto proposto

```
notebooks/04_modelagem_ml.ipynb
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
├── 10. Análise de sensibilidade — Modelo A vs Modelo B (Desenho 2)
│     • Modelo A: com as 13 variáveis Q* (cenário "realista")
│     • Modelo B: sem nenhuma Q* (controle de data leakage circular)
│     • Comparar F1 e feature importance — quanto a acurácia cai sem comorbidades?
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
| Q* como features | **Sim** no Desenho 2; constantes no Desenho 1 (excluídas) | Estilo Cancella; documentar leakage circular como limitação |
| Tratamento de missing | **Imputação por classe** (média/moda) após corte de >75% NaN | Já feito no NB03/NB03b |
| Outliers | **IQR × 3,0 por classe → substituir** | ~3,3 σ; já feito no NB03/NB03b |
| Discretização | **Sim** — IMC-OMS, faixa etária, atividade física, escore inflamatório | Melhor interpretabilidade das regras (CAPTO) |
| Split | **80/20 estratificado**, `random_state=42` | Padrão da literatura PUC Minas |
| Balanceamento | **RUS dentro de cada fold da CV** (não fora) | Evita vazamento; padrão Cancella |
| Métrica-alvo | **F1-macro** | Robusta a desbalanceamento (Desenho 1) |
| Onde mora o ML | **`notebooks/04_modelagem_ml.ipynb`** | Não criar 02b/04b separados — feature eng já está nos NB03/03b |

---

## 4. Artefatos esperados ao final do NB04

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
- A atualização do `Resultados_Consolidados_PNS2019_Artrite.docx` via `python scripts/build_documento_resultados.py`

---

## 5. Checklist antes de começar o NB04

- [ ] Corrigir ou remover `scripts/rastrear_registros_nulos.py` (script quebrado — `NameError`)
- [ ] Adicionar `nbformat` e `xlrd` ao `requirements.txt`
- [ ] Confirmar que `dataset_preprocessado.csv` foi gerado nos dois desenhos (rodar NB03 e NB03b se necessário)
- [ ] Criar `notebooks/04_modelagem_ml.ipynb` seguindo o esqueleto acima
- [ ] Considerar criar `scripts/build_nb04.py` para gerar o notebook de forma idempotente (padrão dos NB03/NB03b)

---

## 6. Depois do NB04 — fechamento do projeto

1. **Atualizar** `Resultados_Consolidados_PNS2019_Artrite.docx` com as métricas e figuras do ML.
2. **Redigir** as seções pendentes do artigo (Resultados → Discussão → Introdução → Resumo), seguindo o template em `Artigo_Template_de_Trabalho_PNS2019.docx` e o guia em `Guia_Redacao_Artigo_PNS2019.docx`.
3. **Preencher** o checklist STROBE (22 itens) — referência teórica registrada no orientador.
4. **Revisão final** com o Prof. Zárate antes de submissão ao JHI/SBIS.

---

*Documento atualizado em 21/05/2026, substituindo o Q&A original de definição de arquitetura (cujas decisões foram absorvidas nos NB03/NB03b).*
