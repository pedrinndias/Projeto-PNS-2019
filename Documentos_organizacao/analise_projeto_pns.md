# Análise do Projeto PNS 2019
## Mineração de Dados — Pedro Dias Soares

> **Última atualização:** 10/06/2026
> **Documento companheiro:** [`../proxima_fase.md`](../proxima_fase.md) (roadmap das Fases 3.x e 4). O antigo `plano_reestruturacao.md` está **descontinuado** (ver banner no topo dele).

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
│       ├── discretizacao/             ← Desenho 1 discretizado (NB04)
│       ├── discretizacao_comorbidades/← Desenho 2 discretizado (NB04)
│       ├── bases_finais/              ← bases finais: 2 .db + 2 .csv + Excel (NB05)
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
│   ├── 02_analise_exploratoria_bivariada.ipynb     ← EDA bivariada — Desenho 1
│   ├── 02b_analise_exploratoria_comorbidades.ipynb ← EDA bivariada — Desenho 2
│   ├── 03_preprocessamento_v3.ipynb           ← Desenho 1
│   ├── 03b_preprocessamento_comorbidades.ipynb ← Desenho 2
│   ├── 04_discretizacao.ipynb                 ← discretização (faixas de domínio + plano cartesiano)
│   ├── 05_exportacao_bases.ipynb              ← exporta bases finais (.db + .csv) dos 2 desenhos
│   └── 06_modelagem_ml.ipynb                  ← (a criar) modelagem e avaliação
├── scripts/                                   ← (vazio no momento — scripts de build removidos)
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
| `.gitignore` | ✅ | Ignora `.csv`, `.db`, `.venv`, settings locais. Limpo (duplicatas removidas em 30/05) |
| `requirements.txt` | ✅ | Inclui `nbformat` e `xlrd` |
| README | ✅ | Sincronizado em 08/06 (NB04/05 existem; 05 = exportação; +02b; NB06 a criar) |
| Notebooks 01–05 + 02b | ✅ | Reexecutados em 10/06 (skip patterns corrigidos, imputação global target-blind, skip na EDA). `data/results/` e bases finais regenerados e versionados |
| Rastreabilidade (JSON) | ✅ | `relatorio_preprocessamento.json` em cada pasta de resultado |
| Scripts de build | ⚠️ | Removidos do repo (commit ad89d7a). Os notebooks são mantidos diretamente, não mais por geradores |

---

## 3. Pipeline KDD — situação por fase

| Fase | Etapas | Status |
|------|--------|--------|
| **Fase 1** · Entendimento (CAPTO) | 1. Contexto · 2. PICOS · 3. Seleção de variáveis | ✅ Concluído |
| **Fase 2** · Pré-processamento | 4. Skip patterns · 5. Missing >75% · 6. Outliers IQR×3 · 7. Imputação | ✅ Concluído |
| **Fase 3** · Preparação | 8. Feature engineering (IMC, escores) · 9. Encoding OHE · 10. Discretização — faixas de domínio + plano cartesiano (NB04) · 11. Exportação das bases finais (NB05) | ✅ **Concluído** |
| **Fase 4** · Modelagem e avaliação | 12. ML — Reg. Logística · Árvore · Random Forest (NB06) | 🔴 **Pendente** |

Fluxograma: [`figuras_artigo/fluxograma_pipeline_kdd.png`](figuras_artigo/fluxograma_pipeline_kdd.png).

---

## 4. Dois desenhos de estudo

| Aspecto | Desenho 1 — Artrite Pura | Desenho 2 — Artrite c/ Comorbidades |
|---------|--------------------------|--------------------------------------|
| Notebook | `03_preprocessamento_v3.ipynb` | `03b_preprocessamento_comorbidades.ipynb` |
| Critério | `Q079 = Sim` e demais 13 doenças = Não | `Q079 = Sim` com qualquer combinação |
| n casos | 494 | 4 025 |
| n controles | 4 332 | 4 332 |
| Razão | 8,77:1 (desbalanceado) | 1,08:1 (quase balanceado) |
| Features (pré-proc → após NB04) | 69 → 56 | 66 → 54 |
| Vars Q* (comorbidades) | Constantes → removidas | **Removidas das features** (filtro de coorte; anti-leakage) — só Q084 permanece; **+ exames condicionais** (`Q04708/Q047081/Q04711/Q047111/Q05901`) também removidos |
| Skip patterns | 29 274 NaN preenchidos | 50 565 NaN preenchidos |
| Vars excluídas (>75% NaN) | 13 | 15 |
| Outliers tratados (IQR×3 → NaN → média global) | 320 | 493 |
| Valores imputados | 26 443 (global target-blind) | 33 616 (global target-blind) |
| Risco metodológico | Amostra pequena para ML | Leakage circular das Q* + exames **resolvido por anti-leakage** (NB03b) |

Comorbidades mais prevalentes no Desenho 2: hipertensão 65,3% · colesterol alto 39,8% · diabetes 21,9% · depressão 19,5%.

---

## 5. Decisões metodológicas registradas

| Etapa | Decisão | Justificativa |
|-------|---------|---------------|
| Faixa etária | ≥ 60 anos (idosos) | Alinhado com Cancella (2025) e Plano do Artigo |
| Limite de missing | Excluir variável se > 75% NaN | Padrão Cancella (60%) flexibilizado para preservar variáveis-chave |
| Outliers | IQR × 3,0 por classe → marcar como NaN → imputar por média global | ~3,3 σ na normal; conservador (Hipertensão/DPOC usam 1,5×) |
| Imputação | Média (numérica) / Moda (categórica) **global (target-blind)**; IMC/escores por **mediana global** | Sem vazamento do alvo no dataset de ML (a EDA descritiva vem dos `.db`, à parte); mediana evita `IMC=0` no `fillna` final |
| Renda (`VDF004`) | Tratada como **faixa** (1–7) via `coerce_codificado` (aceita texto ou código) | É faixa de salário mínimo, não "quintil"; evita exclusão silenciosa |
| Plano de saúde | `I00102` (médico) — **não** `I00101` (odontológico) | Correção de código contra o dicionário PNS 2019 |
| Discretização (NB04) | Faixa etária, IMC-OMS, atividade física, consultas (J012), álcool (NIAAA, só D1) e **padrão alimentar via plano cartesiano** (Ribeiro & Zárate, 2019) — substitui os escores em quartis | Faixas de organismos oficiais (OMS, Guia AF BR 2021, NIAAA); padrão CAPTO/STROBE |
| Anti-leakage (D2) | Comorbidades-filtro (13 Q*) **+ exames condicionais** (Q047*/Q05901) removidos das features (só Q084 permanece) | Q* e exames a elas atrelados definem a coorte, não o modelo — evita vazamento circular |
| Consistência D1×D2 | NB03 e NB03b usam **a mesma metodologia/variáveis**; diferem só na coorte e no anti-leakage | Alinhados em 08/06; evita divergência de resultados entre desenhos |
| Encoding | OHE com `drop_first=True, dtype=int` (nominais) | Compatível com Logistic Regression e árvores |
| Balanceamento | RUS **dentro de cada fold da CV** (NB06) | Evita vazamento entre treino e teste |
| Random state | `42` em tudo | Reprodutibilidade |

---

## 6. Pontos de atenção atuais

### 🔴 Correções de código aplicadas (10/06/2026 — **exigem reexecução**)

Bugs **substantivos** corrigidos no código; o `data/results/` versionado ainda reflete a versão ANTIGA — **reexecutar `02 → 03 → 03b → 04 → 05`** para regenerar CSVs/figuras/JSON e atualizar as dimensões e contagens abaixo.

- **3.1/3.2 — Escore alimentar corrompido por bug texto→NaN (RESOLVIDO na raiz):** as variáveis de frequência alimentar guardam o valor 0 dia/sem. como o **texto** `"Nunca ou menos de uma vez por semana"`; o `pd.to_numeric` o jogava para `NaN`, que virava **média imputada** (não-consumidor tratado como consumidor médio). Efeito medido: `Escore_Inflamatorio` **inflado ~2×** (média 12,5 → 6,3 real; P02001 74% imputado → 0%). Corrigido com `coerce_frequencia` (`"Nunca…"→0`) em **NB02, NB02b, NB03, NB03b**. Como `P02001`/`P02602` saem do corte >75% missing, **o escore volta a ter a mesma composição nos dois desenhos** (3.2). ⚠️ Reflexo na EDA: as medianas alimentares e o alerta de **causalidade reversa** (NB02) precisam ser **reinterpretados** — parte do achado "contraintuitivo" vinha de descartar os não-consumidores.
- **3.3 — Outliers IQR só em contínuas verdadeiras:** o IQR×3 por classe era aplicado também a **contagens limitadas** (dias/sem. 0–7, doses, consultas), achatando respostas legítimas (ex.: 285 doses de álcool → média). Agora o tratamento de outlier é restrito a `P00104`/`P00404`/`C008` (peso/altura/idade), onde extremo = erro de medição. As contagens são absorvidas pela discretização do NB04.
- **3.4 — Vazamento não-supervisionado documentado:** a **mediana** do plano cartesiano alimentar (NB04) é o **único** corte data-driven (os demais são faixas de domínio fixas) e é alvo-cega; fica registrado que o **NB06 deve reajustá-la _in-fold_** (só no treino) dentro da CV.

### 🟢 Resolvidos (08/06/2026 — auditoria + alinhamento)

- **Rótulos de variáveis corrigidos** (contra o dicionário PNS 2019): `I00101`→`I00102` (plano médico, não odontológico); rótulos alimentares do NB02 (`P02001`=suco em pó, `P01601`=suco natural, `P02602`=subst. almoço); `VDF004`=faixa (não "quintil"). +`P006`/`P013` (feijão/frango semanais), +`P00620` (embutidos) qualitativo.
- **Inconsistência D1×D2 (introduzida no merge) — RESOLVIDA:** o NB03b recebeu todas as correções do NB03 (I00102, coerce/renda-faixa, skip-8 P03202, imputação por mediana de IMC/escores, +15 variáveis); anti-leakage do D2 estendido para remover exames condicionais a comorbidades.
- **Bug `NaN`-como-categoria na Tab 2-C** (NB02/02b): `dropna()` antes do `crosstab`, alinhando com a Tab 2-B (não contamina mais χ²/Fisher).
- **`IMC=0` latente:** imputação por mediana de IMC/escores antes do `fillna(0)` final (NB03 e NB03b).

### 🟢 Reexecução concluída (10/06/2026)

O pipeline `02 → 03 → 03b → 04 → 05` foi **reexecutado** após as correções de 10/06 (skip patterns das perguntas-pai textuais, imputação **global target-blind**, skip P035←P034 na EDA). `data/results/` (CSVs, figuras, relatórios) e as bases finais foram **regenerados e commitados**. Dims atuais: D1 4 826×69→56, D2 8 357×66→54. Não há mais reexecução pendente — resta a modelagem (NB06).

### 🟢 Resolvidos (30/05/2026)

- `requirements.txt` — `nbformat` e `xlrd` adicionados.
- `.gitignore` — duplicatas e referência a `archive/` limpas.
- `scripts/rastrear_registros_nulos.py` e `scripts/criar_banco_formatado.py` — removidos do repo (não há mais bug ativo neles).
- `04_eliminacao_outliers.ipynb` — removido; o tratamento de outliers permanece embutido no NB03/NB03b. O NB04 será dedicado à **discretização**.

### 🟡 Pendências cosméticas

| # | Arquivo | Observação |
|---|---------|------------|
| 1 | `data/raw/input_PNS_2019.sas` ↔ `.txt` | Diferem só por 2 bytes (provável `\n`) — considerar manter um só |
| 2 | `dicionario_PNS_microdados_2019.xls` | Existe em `data/raw/` e `Documentos_organizacao/Dados PNS/` com **hashes diferentes** — verificar qual é a versão correta |
| 3 | `scripts/` | Pasta vazia — sem geradores; notebooks mantidos diretamente |

### ✅ Risco metodológico documentado (resolvido)

| # | Observação |
|---|------------|
| 7 | **Data leakage circular no Desenho 2 — RESOLVIDO:** as variáveis Q* foram usadas para definir o controle "saudável" (todas Q* = Não). Para evitar vazamento, as comorbidades-filtro são **removidas das features** no NB03b (anti-leakage), permanecendo apenas como critério de seleção da coorte; só Q084 (não-filtro, varia nos controles) fica. Não há mais Modelo A vs Modelo B. |

---

## 7. Progresso geral

| Eixo | Status |
|------|:------:|
| Compreensão do problema (CAPTO/PICOS) | ✅ 100% |
| ETL e bases SQLite | ✅ 100% |
| EDA bivariada (NB02 D1 + NB02b D2) | ✅ 100% — reexecutada 10/06 (figuras/tabelas regeneradas) |
| Pré-processamento — Desenho 1 (NB03) | ✅ 100% |
| Pré-processamento — Desenho 2 (NB03b) | ✅ 100% — alinhado ao D1 e reexecutado 10/06 |
| Documentação (template, guias, resultados consolidados) | ✅ 100% |
| **Discretização (NB04)** | ✅ 100% — faixas de domínio + plano cartesiano |
| **Exportação das bases (NB05)** | ✅ 100% — 2 .db + 2 .csv + Excel |
| **Modelagem ML (NB06)** | 🔴 0% |
| Avaliação e feature importance | 🔴 0% |
| Redação do artigo (Resultados/Discussão) | 🔴 0% |

**Progresso geral estimado:** ~85% — pipeline corrigido, consistente entre os dois desenhos e **reexecutado** (bases finais regeneradas); faltam a modelagem (NB06) e a escrita do artigo.

---

## 8. Próximos passos

Detalhamento em [`../proxima_fase.md`](../proxima_fase.md). Em resumo:

1. ✅ **Concluído** — `notebooks/04_discretizacao.ipynb` (faixas de domínio + plano cartesiano) e `05_exportacao_bases.ipynb` (bases finais .db/.csv/Excel).
2. ✅ **Concluído (10/06)** — pipeline `02 → 03 → 03b → 04 → 05` reexecutado e `data/results/`/bases finais regenerados e commitados.
3. **Criar** `notebooks/06_modelagem_ml.ipynb` — pipeline ML nos dois desenhos (Reg. Logística, Árvore, Random Forest; RUS dentro da CV; F1-macro com IC 95%).
4. **Atualizar** o `Resultados_Consolidados_PNS2019_Artrite.docx` com as métricas do ML.
5. **Redigir** as seções de Resultados e Discussão do artigo.

---

*Documento atualizado em 10/06/2026: correção dos skip patterns (perguntas-pai textuais → `MAPA_PAIS` texto→código nos NB03/03b), imputação trocada para **global target-blind** (sem vazamento do alvo), skip P035←P034 aplicado na EDA (NB02 incl. Tab 3-A). Pipeline `02→03→03b→04→05` reexecutado e `data/results/` regenerado/versionado. Dims atuais: D1 4 826×69→56, D2 8 357×66→54. **Pendente:** modelagem no NB06.*
