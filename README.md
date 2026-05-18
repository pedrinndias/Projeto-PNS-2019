# Projeto PNS 2019 – Artrite e Reumatismo em Idosos Brasileiros

Projeto de Mineração de Dados (PUC Minas – Semestre 3) que investiga o perfil de idosos brasileiros (≥ 60 anos) com artrite/reumatismo utilizando os microdados da Pesquisa Nacional de Saúde (PNS) 2019.

**Autor:** Pedro Dias Soares  
**Orientador:** Prof. Dr. Luis Enrique Zárate – PUC Minas  
**Metodologia:** CRISP-DM / framework CAPTO / PICOS / STROBE

---

## Estrutura do Repositório

```
Projeto_PNS/
├── data/
│   ├── raw/               ← Dados brutos (pns2019.csv não versionado – ver .gitignore)
│   └── results/
│       ├── preprocessing/             ← Desenho 1: artrite pura (4 826 × 49)
│       ├── preprocessing_comorbidades/← Desenho 2: artrite + comorbidades (8 357 × 57)
│       └── eda/                       ← Figuras da análise exploratória
├── Documentos_organizacao/
│   ├── figuras_artigo/
│   │   └── fluxograma_pipeline_kdd.png  ← Fluxograma KDD (4 fases, 10 etapas)
│   ├── Artigo_Template_de_Trabalho_PNS2019.docx
│   ├── Guia_Redacao_Artigo_PNS2019.docx
│   ├── Guia_Analises_Relatorios_PNS2019_Artrite.docx
│   ├── Plano_Artigo_Mineracao_Pedro_Dias_Soares.docx
│   ├── Resultados_Consolidados_PNS2019_Artrite.docx
│   ├── analise_projeto_pns.md
│   └── plano_reestruturacao.md
├── notebooks/
│   ├── 01_extracao_pre_processamento.ipynb
│   ├── 02_analise_exploratoria_bivariada.ipynb
│   ├── 03_preprocessamento_v3.ipynb          ← Desenho 1 – artrite pura
│   └── 03b_preprocessamento_comorbidades.ipynb ← Desenho 2 – artrite + comorbidades
├── scripts/
│   ├── build_nb03.py                  ← Gerador reproduzível do nb03
│   ├── build_nb03b.py                 ← Gerador reproduzível do nb03b
│   ├── build_fluxograma_pipeline.py   ← Gerador do fluxograma KDD (matplotlib)
│   ├── build_guia_redacao.py
│   ├── build_documento_resultados.py
│   ├── build_template_trabalho.py
│   ├── criar_banco_formatado.py
│   └── rastrear_registros_nulos.py
├── docs/
├── requirements.txt
└── .gitignore
```

---

## Pipeline KDD – 10 Etapas / 4 Fases

| Fase | Etapas | Status |
|------|--------|--------|
| **Fase 1** – Entendimento do problema (CAPTO) | 1. Contexto · 2. Perguntas PICOS · 3. Seleção de variáveis | Concluído |
| **Fase 2** – Pré-processamento | 4. Skip patterns · 5. Missing (>75%) · 6. Outliers · 7. Imputação | Concluído |
| **Fase 3** – Preparação para mineração | 8. Feature engineering · 9. Encoding (OHE) | Concluído |
| **Fase 4** – Modelagem e avaliação | 10. ML (Reg. Logística, Árvore, Random Forest) | **Pendente** |

---

## Dois Desenhos de Estudo

### Desenho 1 – Artrite Pura (`03_preprocessamento_v3.ipynb`)
- **Critério:** `Q079 = Sim` (sem exigência de outras doenças)
- **Amostra:** 4 826 registros · 49 features
- **Distribuição:** 4 332 saudáveis vs 494 artrite (razão 8,77:1 – desbalanceado)
- **Dataset:** `data/results/preprocessing/dataset_preprocessado.csv`

### Desenho 2 – Artrite com Comorbidades (`03b_preprocessamento_comorbidades.ipynb`)
- **Critério:** `Q079 = Sim` com qualquer combinação de outras doenças crônicas
- **Amostra:** 8 357 registros · 57 features
- **Distribuição:** 4 332 saudáveis vs 4 025 artrite (razão 1,08:1 – quase balanceado)
- **Comorbidades prevalentes:** hipertensão 65,3% · colesterol alto 39,8% · diabetes 21,9% · depressão 19,5%
- **Dataset:** `data/results/preprocessing_comorbidades/dataset_preprocessado.csv`

---

## Decisões de Pré-processamento (Desenho 1)

| Etapa | Decisão | Resultado |
|-------|---------|-----------|
| Skip patterns | Preenchimento condicional (J012, P035, P02801…) | 1 344 NaN estruturais resolvidos |
| Missing >75% | Exclusão da variável | 13 variáveis removidas |
| Outliers | Substituição por limite IQR×3 por classe | 50 valores tratados |
| Imputação | Média/classe (numérica) · Moda/classe (categórica) | 27 455 valores imputados |
| Feature eng. | IMC · Escore Inflamatório · Escore Saudável · Razão Inf/Saud | 4 features criadas |
| Encoding | OHE em 22 variáveis categóricas | Dataset final 4 826 × 49 |

---

## Como Reproduzir

```bash
# Clonar o repositório
git clone https://github.com/pedrinndias/Projeto-PNS-2019.git

# Instalar dependências
pip install -r requirements.txt

# Executar os notebooks em ordem
jupyter notebook notebooks/01_extracao_pre_processamento.ipynb
jupyter notebook notebooks/02_analise_exploratoria_bivariada.ipynb
jupyter notebook notebooks/03_preprocessamento_v3.ipynb        # Desenho 1
jupyter notebook notebooks/03b_preprocessamento_comorbidades.ipynb  # Desenho 2

# Regenerar o fluxograma KDD
python scripts/build_fluxograma_pipeline.py

# Regenerar notebooks via script (idempotente)
python scripts/build_nb03.py
python scripts/build_nb03b.py
```

---

## Dados

- **Fonte:** [IBGE – Pesquisa Nacional de Saúde 2019](https://www.ibge.gov.br/estatisticas/sociais/saude/9160-pesquisa-nacional-de-saude.html)
- `pns2019.csv` não é versionado por tamanho (~700 MB). Baixar diretamente no IBGE e colocar em `data/raw/`.
- Bancos SQLite gerados pelo `scripts/criar_banco_formatado.py` também não são versionados.

---

## Requisitos Principais

- Python 3.10+
- pandas · numpy · matplotlib · seaborn · scikit-learn · nbformat · python-docx · imbalanced-learn

Ver lista completa em `requirements.txt`.
