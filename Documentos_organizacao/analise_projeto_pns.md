# 📊 Análise Completa do Projeto PNS 2019
## Mineração de Dados — Pedro Dias Soares

> **Data da análise:** 09/05/2026  
> **Avaliação de:** Desempenho, Progresso e Estrutura do Projeto

---

## 1. Visão Geral do Projeto

| Item | Detalhe |
|------|---------|
| **Objetivo** | Identificar e analisar o perfil de pessoas idosas saudáveis e comparar com aquelas que possuem artrite/reumatismo, utilizando microdados da PNS 2019 |
| **Base de Dados** | Pesquisa Nacional de Saúde 2019 (IBGE) — ~293.726 registros, 1.087 colunas |
| **Linguagem** | Python (Pandas, NumPy, Matplotlib, Seaborn, FPDF, python-docx) |
| **Armazenamento** | SQLite (banco formatado ~1.1 GB) |
| **Metodologia de Referência** | KDD / CRISP-DM |
| **Referências Acadêmicas** | Pereira & Galvão (2012–2014), STROBE Statement 2007, LICAP/PUC Minas (Zárate et al.) |

---

## 2. Estrutura do Repositório

```
Projeto_PNS/
├── 📁 data/
│   ├── raw/           → PNS_2019.txt (~455 MB), dicionário XLS, inputs SAS
│   ├── processed/     → ⚠️ VAZIO
│   └── database/      → 5 bancos SQLite (master + 4 subconjuntos)
│       ├── pns_master_formatado.db  (~1.1 GB)
│       ├── idosos_geral.db          (~16 MB)
│       ├── idosos_saudaveis.db      (~8 MB)
│       ├── idosos_artrite.db        (~8 MB)
│       └── idosos_artrite_puro.db   (~1 MB)
├── 📁 notebooks/
│   ├── pessoas_saudaveis.ipynb  → Notebook principal (~572 KB)
│   ├── pns2019.csv              → CSV principal (~922 MB)
│   └── documentação auxiliar (dicionário, chaves, inputs)
├── 📁 scripts/
│   ├── criar_banco_formatado.py   → ETL: CSV → SQLite com tradução de códigos
│   └── rastrear_registros_nulos.py → Análise de dados faltantes por módulo
├── 📁 src/              → ⚠️ VAZIO (prometido no README)
├── 📁 docs/             → ⚠️ VAZIO (prometido no README)
├── 📁 resultados_analise/
│   ├── 1_Populacao_Idosa_Geral/      → estatísticas + gráficos
│   ├── 1_Populacao_Jovem_Geral/      → estatísticas + gráficos
│   ├── 2_Idosos_Saudaveis/           → estatísticas + gráficos
│   ├── 2_Jovens_Saudaveis/           → estatísticas + gráficos
│   ├── 3_Idosos_com_Artrite/         → estatísticas + gráficos
│   ├── 3_Jovens_com_Artrite/         → estatísticas + gráficos
│   ├── 4_Idosos_APENAS_Artrite/      → estatísticas + gráficos
│   └── 4_Jovens_APENAS_Artrite/      → estatísticas + gráficos
├── Plano_Artigo_Mineracao_Pedro_Dias_Soares.docx
├── README.md
├── requirements.txt
├── .gitignore
├── bfg-1.15.0.jar       → ⚠️ Ferramenta de limpeza Git (deveria ser removida)
└── 2x arquivos ZIP de análise exploratória
```

### 2.1 Avaliação da Estrutura

| Aspecto | Status | Comentário |
|---------|--------|------------|
| Organização de diretórios | ✅ Boa | Segue padrão `data/raw`, `data/processed`, `notebooks`, `scripts`, `src` |
| Pasta `src/` | ⚠️ Vazia | Deveria conter módulos Python reutilizáveis |
| Pasta `docs/` | ⚠️ Vazia | Sem documentação adicional |
| Pasta `data/processed/` | ⚠️ Vazia | Dados processados não estão sendo salvos como CSV intermediários |
| `.gitignore` | ✅ Funcional | Ignora CSVs grandes e banco SQLite master |
| `requirements.txt` | ⚠️ Incompleto | Falta `python-docx`, sem versionamento de pacotes |
| README | ✅ Adequado | Bem estruturado, mas URL do `git clone` está genérica |
| Ambientes virtuais | ⚠️ Duplicados | Existem `.venv` e `.venv-1` (um deveria ser removido) |

---

## 3. Análise do Plano do Artigo

O documento `Plano_Artigo_Mineracao_Pedro_Dias_Soares.docx` segue uma estrutura acadêmica sólida com 8 fases:

### 3.1 Fases Planejadas vs. Implementação

| Fase | Descrição | Implementado? |
|------|-----------|:-------------:|
| **Brainstorm Inicial** | Definição preliminar do tema | ✅ |
| **Fase 0** — Antes de Escrever | Objetivo + periódico/normas | ✅ |
| **Fase 1** — Tabelas e Figuras | Montar visualizações antes da escrita | ⚠️ Parcial |
| **Fase 2** — Método | Delineamento (PICOS), variáveis, análise estatística + **ML** | ⚠️ Parcial |
| **Fase 3** — Resultados | Características da amostra, achados | ⚠️ Apenas EDA básica |
| **Fase 4** — Discussão | Interpretação e comparação com literatura | ❌ Não iniciada |
| **Fase 5** — Introdução | Contexto e justificativa | ❌ Não iniciada |
| **Fase 6** — Resumo e Palavras-chave | Abstract final | ❌ Não iniciada |
| **Fase 7** — Checklist Final | Revisão STROBE | ❌ Não iniciada |

### 3.2 Elementos Metodológicos (PICOS)

| Componente | Definição no Plano |
|------------|-------------------|
| **P** (População) | Idosos brasileiros (≥60 anos) da PNS 2019 |
| **I** (Intervenção/Exposição) | Presença de artrite/reumatismo diagnosticada |
| **C** (Comparação) | Idosos saudáveis (sem doenças crônicas) |
| **O** (Outcomes) | Perfil sociodemográfico, hábitos, acesso à saúde |
| **S** (Study design) | Estudo transversal analítico |

### 3.3 Palavras-chave Definidas

> Artrite / Mineração de Dados / Aprendizado de Máquina / Saúde do Idoso / Pesquisa Nacional de Saúde

**⚠️ PONTO CRÍTICO:** O plano menciona explicitamente **"Análise Estatística e Modelos de Aprendizado de Máquina"** na Fase 2.6, que é um requisito central da disciplina de Mineração de Dados. Essa parte **ainda não foi implementada** no código.

---

## 4. Relatório Modular das Variáveis da PNS 2019

A PNS 2019 é estruturada em **4 partes** e **29 módulos temáticos**, totalizando 1.087 colunas e 5.221 entradas no dicionário de dados. Abaixo segue o mapeamento completo dos módulos e a análise de quais variáveis são (e devem ser) utilizadas no projeto.

### 4.1 Estrutura Modular Completa

| Parte | Módulo | Descrição | Relevância para o Projeto |
|:-----:|:------:|-----------|:-------------------------:|
| **1** | — | Identificação e Controle (V0001, V0024, UPA_PNS...) | ✅ UF/Estado |
| **2** | **A** | Informações do Domicílio | 🟡 Possível |
| **2** | **B** | Visitas Domiciliares de Equipe de Saúde | 🟡 Possível |
| **3** | **C** | Características Gerais dos Moradores | ✅ **Essencial** |
| **3** | **D** | Características de Educação | ✅ **Essencial** |
| **3** | **E** | Características de Trabalho | 🟡 Possível |
| **3** | **F** | Rendimentos de Outras Fontes | 🟡 Possível |
| **3** | **G** | Pessoas com Deficiências (≥2 anos) | 🟡 Possível |
| **3** | **I** | Cobertura de Plano de Saúde | ✅ Importante |
| **3** | **J** | Utilização de Serviços de Saúde | ✅ Importante |
| **3** | **K** | Saúde dos Indivíduos com ≥60 anos | ✅ **Essencial** |
| **3** | **L** | Crianças com menos de 2 anos | ❌ Não relevante |
| **4** | **M** | Características do Trabalho e Apoio Social | 🟡 Possível |
| **4** | **N** | Percepção do Estado de Saúde | ✅ **Essencial** |
| **4** | **O** | Acidentes | 🟡 Baixa |
| **4** | **P** | Estilos de Vida (alimentação, exercício, álcool, tabaco) | ✅ **Essencial** |
| **4** | **Q** | Doenças Crônicas | ✅ **CENTRAL** |
| **4** | **R** | Saúde da Mulher (≥18 anos) | 🟢 Complementar |
| **4** | **S** | Atendimento Pré-Natal | ❌ Não relevante |
| **4** | **T** | Doenças Transmissíveis | 🟢 Complementar |
| **4** | **U** | Saúde Bucal | 🟢 Complementar |
| **4** | **V** | Violência (≥18 anos) | ❌ Não relevante |
| **4** | **W** | Antropometria (peso/altura medidos) | ✅ Importante |
| **4** | **Y** | Atividade Sexual (≥18 anos) | ❌ Não relevante |
| **4** | **Z** | Paternidade e Pré-Natal do Parceiro | ❌ Não relevante |
| — | **VD** | Variáveis Derivadas (renda, escolaridade, etc.) | ✅ **Essencial** |
| **4** | **H** | Atendimento Médico (≥18 anos) | 🟡 Possível |

### 4.2 Módulo Q — Doenças Crônicas (MÓDULO CENTRAL)

Este é o módulo mais importante do projeto. O notebook atualmente utiliza **14 variáveis de diagnóstico** para definir os grupos de análise:

| Variável | Pergunta do Questionário | Uso no Projeto |
|:--------:|--------------------------|:--------------:|
| **Q00201** | Algum médico já lhe deu o diagnóstico de **hipertensão arterial** (pressão alta)? | Filtro: saudável |
| **Q03001** | Algum médico já lhe deu o diagnóstico de **diabetes**? | Filtro: saudável |
| **Q060** | Algum médico já lhe deu o diagnóstico de **colesterol alto**? | Filtro: saudável |
| **Q06306** | Diagnóstico de **doença do coração** (infarto, angina, insuficiência cardíaca)? | Filtro: saudável |
| **Q068** | Diagnóstico de **AVC** (Acidente Vascular Cerebral) ou derrame? | Filtro: saudável |
| **Q074** | Diagnóstico de **asma** (ou bronquite asmática)? | Filtro: saudável |
| **Q079** | Diagnóstico de **artrite ou reumatismo**? | ✅ **Variável-alvo** |
| **Q088** | Diagnóstico de **DORT** (Distúrbio Osteomuscular)? | Filtro: saudável |
| **Q092** | Diagnóstico de **depressão**? | Filtro: saudável |
| **Q11006** | Diagnóstico de **outra doença mental** (ansiedade, pânico, esquizofrenia, bipolar, TOC)? | Filtro: saudável |
| **Q11604** | Diagnóstico de **doença crônica no pulmão** (enfisema, bronquite crônica, DPOC)? | Filtro: saudável |
| **Q120** | Diagnóstico de **câncer**? | Filtro: saudável |
| **Q124** | Diagnóstico de **insuficiência renal crônica**? | Filtro: saudável |
| **Q128** | Diagnóstico de **outra doença crônica** (física ou mental, >6 meses)? | Filtro: saudável |

**Lógica de classificação no código:**
- **Saudável:** Todas as 14 variáveis = 2 (Não)
- **Com artrite:** Q079 = 1 (Sim)
- **Artrite pura:** Q079 = 1 E todas as outras 13 = 2

> **Observação:** O Módulo Q contém ainda dezenas de sub-variáveis por doença (idade do diagnóstico, tratamentos, limitações), que **não estão sendo exploradas** atualmente mas poderiam enriquecer a análise de artrite.

### 4.3 Variáveis Adicionais Relevantes (ainda NÃO utilizadas)

Além do Módulo Q, o projeto deveria incorporar variáveis de outros módulos para criar features para o Machine Learning. Abaixo, a seleção recomendada organizada por categoria:

#### 📋 Sociodemográficas (Módulos C, D, VD)

| Variável | Descrição | Tipo | Prioridade |
|:--------:|-----------|:----:|:----------:|
| **C006** | Sexo | Categórica (1=Masc, 2=Fem) | 🔴 Alta |
| **C008** | Idade do morador (anos) | Numérica | 🔴 Alta |
| **C009** | Cor ou raça | Categórica (1=Branca..5=Indígena) | 🔴 Alta |
| **C004** | Condição no domicílio | Categórica | 🟡 Média |
| **V0001** | Unidade da Federação | Categórica (código UF) | ✅ Já usada |
| **VDD004A** | Nível de instrução mais elevado | Ordinal | 🔴 Alta |
| **VDE001** | Condição em relação à força de trabalho | Categórica | 🟡 Média |
| **VDE002** | Condição de ocupação | Categórica | 🟡 Média |
| **VDE014** | Grupamento de atividade do trabalho | Categórica | 🟡 Média |
| **VDF002** | Rendimento domiciliar (R$) | Numérica | 🔴 Alta |
| **VDF003** | Rendimento domiciliar per capita (R$) | Numérica | 🔴 Alta |
| **VDF004** | Faixa de rendimento per capita | Ordinal | 🔴 Alta |

#### 🏥 Saúde Percebida (Módulo N)

| Variável | Descrição | Tipo | Prioridade |
|:--------:|-----------|:----:|:----------:|
| **N001** | Autoavaliação do estado de saúde | Ordinal (1=Muito bom..5=Muito ruim) | 🔴 Alta |

#### 🏃 Estilo de Vida (Módulo P)

| Variável | Descrição | Tipo | Prioridade |
|:--------:|-----------|:----:|:----------:|
| **P027** | Frequência de consumo de bebida alcoólica | Ordinal | 🟡 Média |
| **P034** | Praticou exercício físico nos últimos 3 meses? | Categórica (1=Sim, 2=Não) | 🔴 Alta |
| **P035** | Dias por semana de exercício | Numérica | 🟡 Média |
| **P00104** | Peso (kg) | Numérica | 🟡 Média |
| **P00404** | Altura (cm) | Numérica | 🟡 Média |
| **P00601–P00622** | Consumo alimentar (22 itens) | Categórica cada | 🟢 Baixa |

#### 🩺 Acesso à Saúde (Módulos I, J)

| Variável | Descrição | Tipo | Prioridade |
|:--------:|-----------|:----:|:----------:|
| **I001** | Possui plano de saúde? | Categórica | 🟡 Média |
| **J001** | Utilizou serviço de saúde nas últimas 2 semanas? | Categórica | 🟡 Média |

#### 👴 Saúde do Idoso (Módulo K — exclusivo ≥60 anos)

| Variável | Descrição | Tipo | Prioridade |
|:--------:|-----------|:----:|:----------:|
| **K001** | Grau de dificuldade para comer sozinho | Ordinal | 🔴 Alta |
| Outras K* | Atividades de vida diária (AVDs) | Ordinal | 🔴 Alta |

#### 🎯 Variáveis Específicas de Artrite (Módulo Q — sub-variáveis)

| Variável | Descrição | Tipo | Prioridade |
|:--------:|-----------|:----:|:----------:|
| **Q080** | Idade no primeiro diagnóstico de artrite | Numérica | 🟡 Média |
| **Q082** | Já fez cirurgia por causa da artrite? | Categórica | 🟡 Média |
| **Q083** | Grau de limitação nas atividades habituais | Ordinal | 🔴 Alta |
| **Q08107–Q08111** | Recomendações recebidas (exercício, fisio, medicamentos...) | Categórica cada | 🟡 Média |

### 4.4 Seleção Recomendada de Features para Machine Learning

Para a modelagem, recomenda-se um conjunto de **15-20 features** organizadas assim:

```
VARIÁVEL-ALVO (target):
  → Q079 (artrite/reumatismo: 1=Sim, 2=Não) — binária

FEATURES RECOMENDADAS:
  Sociodemográficas:
    → C006 (sexo)
    → C008 (idade)
    → C009 (cor/raça)
    → VDD004A (escolaridade)
    → VDF004 (faixa de renda per capita)
    → V0001 (UF/região)
  
  Saúde:
    → N001 (autoavaliação de saúde)
    → Q084 (problema crônico de coluna)
    → Q132 (uso de medicamento para dormir)
  
  Estilo de Vida:
    → P034 (prática de exercício físico)
    → P027 (consumo de álcool)
    → P00104/P00404 (peso/altura → calcular IMC)
  
  Comorbidades (como features, não filtros):
    → Q00201 (hipertensão)
    → Q03001 (diabetes)
    → Q092 (depressão)
    → Q088 (DORT)
```

> **⚠️ IMPORTANTE:** No modelo atual do notebook, as variáveis de doenças crônicas são usadas apenas como **filtros** (para definir "saudável" vs "doente"). Para ML, elas poderiam ser usadas como **features** para predizer a presença de artrite, permitindo identificar perfis de risco.

---

## 5. Análise Detalhada do Código

### 5.1 Script `criar_banco_formatado.py`

**Função:** Lê o CSV bruto da PNS 2019, traduz os códigos numéricos para texto usando o dicionário de dados XLS, e salva tudo em um banco SQLite.

| Aspecto | Avaliação |
|---------|-----------|
| Detecção automática de separador | ✅ Detecta `;` ou `,` automaticamente |
| Processamento em lotes (chunked) | ✅ Usa `chunksize=20000` para não estourar memória |
| Tradução de códigos | ✅ Mapeia códigos → descrições usando dicionário |
| Caminhos dinâmicos | ✅ Usa `os.path` para resolver caminhos relativos |
| Tratamento de erros | ⚠️ Usa `except:` genérico (*bare except*) — má prática Python |
| Documentação | ✅ Bem comentado, cada linha possui explicação |

### 5.2 Script `rastrear_registros_nulos.py`

| Aspecto | Avaliação |
|---------|-----------|
| Análise de nulos por módulo | ✅ Agrupa colunas por letra inicial e analisa nulos |
| Resumo estatístico | ✅ Calcula média, soma e contagem de nulos por módulo |
| **Problema grave** | ❌ Referencia variáveis (`df_bem`, `df_atri_reu`, `df_atri_reu_puro`) que **não são definidas** no script |
| Reutilização | ❌ Não é autônomo — só funciona se colado dentro do notebook |

### 5.3 Notebook `pessoas_saudaveis.ipynb`

#### ❌ PROBLEMA CRÍTICO: Conflitos de Merge Git

O notebook contém **múltiplos conflitos de merge não resolvidos**. Marcadores como:
```
<<<<<<< HEAD
=======
>>>>>>> 0a043f1c9d09640d8b2f4cd209874afdb5ce003b
```
aparecem em diversas células, tornando o arquivo **JSON inválido** e impedindo sua execução normal no Jupyter.

#### Fluxo do Notebook (reconstruído a partir do código-fonte)

1. **Importações:** pandas, numpy, matplotlib, seaborn, os, zipfile, fpdf, docx
2. **Carregamento:** Lê `pns2019.csv` diretamente (~922 MB) — ⚠️ *Não utiliza o banco SQLite criado*
3. **Renomeação de colunas:** Mapeia código UF → nome do estado, cria coluna "Região"
4. **Filtragem por faixa etária:**
   - ⚠️ Filtra **jovens (18-29 anos)** — inconsistente com o objetivo declarado (idosos ≥60)
5. **Definição de doenças crônicas:** 14 colunas (Q00201, Q03001, Q060, Q06306, Q068, Q074, Q079, Q088, Q092, Q11006, Q11604, Q120, Q124, Q128)
6. **Criação de subgrupos:**
   - `df_bem` → Sem nenhuma doença crônica (8.904 registros para jovens)
   - `df_atri_reu` → Com artrite/reumatismo Q079=1 (161 registros)
   - `df_atri_reu_puro` → Artrite sem outras comorbidades (63 registros)
7. **Visualizações:** Histogramas de idade, gráficos de barras por estado e região
8. **Exportação:** Salva estatísticas em TXT, PDF (FPDF) e DOCX (python-docx)
9. **Compactação:** Gera arquivo ZIP com todos os resultados

#### Resumo dos Problemas do Notebook

| # | Problema | Gravidade |
|---|---------|-----------|
| 1 | Conflitos de merge Git não resolvidos | 🔴 Crítico |
| 2 | Lê CSV direto em vez de usar SQLite | 🟡 Importante |
| 3 | Faixa etária (18-29) inconsistente com objetivo (≥60) | 🔴 Crítico |
| 4 | Células duplicadas por causa do merge | 🟡 Importante |
| 5 | Sem análise estatística (testes de hipótese) | 🟡 Importante |
| 6 | Sem Machine Learning | 🔴 Crítico |
| 7 | `PerformanceWarning` nos outputs (DataFrame fragmentado) | 🟢 Menor |

---

## 6. Resultados Gerados

Cada um dos 8 subgrupos contém **5 arquivos** de resultado:

| Arquivo | Formato | Conteúdo |
|---------|---------|----------|
| `estatisticas.txt` | Texto | Contagem por estado e região |
| `estatisticas.pdf` | PDF | Mesma informação em formato PDF |
| `estatisticas.docx` | Word | Mesma informação em formato DOCX |
| `grafico_estados.png` | Imagem | Gráfico de barras por estado |
| `grafico_regioes.png` | Imagem | Gráfico de barras por região |

### 6.1 Exemplo: Dados da População Idosa Geral

| Região | Nº Entrevistados |
|--------|:----------------:|
| Centro-Oeste | 32.488 |
| Nordeste | 85.213 |
| Norte | 64.843 |
| Sudeste | 48.701 |
| Sul | 32.670 |

### 6.2 Exemplo: Idosos Saudáveis

| Região | Nº Saudáveis |
|--------|:------------:|
| Centro-Oeste | 476 |
| Nordeste | 1.185 |
| Norte | 825 |
| Sudeste | 837 |
| Sul | 550 |

**Observação:** Os resultados atuais são exclusivamente **descritivos geográficos** (contagem por estado e região). Não há análises comparativas entre grupos, testes de hipótese, nem modelos preditivos.

---

## 7. Histórico de Desenvolvimento (Git)

| # | Commit | Descrição |
|---|--------|-----------|
| 1 | `4553274` | Notebook inicial de análise |
| 2 | `08e4128` | Documentação e comentários |
| 3 | `ec6bd61` | Remove arquivos grandes do versionamento |
| 4 | `d6f8aaa` | Ignora `pns2019.csv` |
| 5 | `b971f13` | Configura Git LFS para CSVs |
| 6 | `156bb9e` | "Feature X" (genérico) |
| 7 | `45585f9` | Novo README |
| 8 | `8e596d8` | Filtragem preliminar de dados |
| 9 | `1589d99` | Fix no notebook |
| 10 | `00b5714` | Script de análise de nulos |
| 11 | `e5f74af` | PDFs e DOCX de estatísticas |
| 12 | `584b84b` | Atualização genérica |
| 13 | `2d73561` | Refatoração de código |
| 14 | `98ea5f5` | Comentários detalhados no notebook |
| 15 | `ed33407` | ZIP de análise exploratória |
| 16-17 | `c2b1a36`, `ee0f454` | Atualização de dados estatísticos |
| 18 | `0a043f1` | Refatoração (branch secundário) |
| 19 | `76c1f5f` | Remoção de ZIPs + novos resultados |
| 20 | `3df071c` | **Resolve conflitos de merge** ⚠️ *Não resolveu completamente* |

**Observações sobre o Git:**
- O commit `3df071c` ("Resolve conflitos de merge") **não resolveu** todos os conflitos — marcadores ainda presentes
- Mensagens de commit inconsistentes (algumas em português, outras em inglês)
- Alguns commits genéricos demais ("Atualizar", "Feature X")

---

## 8. Problemas Identificados — Por Prioridade

### 🔴 Críticos

| # | Problema | Impacto |
|---|---------|---------|
| 1 | **Conflitos de merge no notebook** | Arquivo `.ipynb` corrompido, não executa |
| 2 | **Inconsistência na faixa etária** | Plano fala ≥60, código filtra 18-29 |
| 3 | **Ausência de Machine Learning** | Requisito central da disciplina não implementado |

### 🟡 Importantes

| # | Problema | Impacto |
|---|---------|---------|
| 4 | Análise apenas descritiva geográfica | Faltam estatísticas comparativas e testes |
| 5 | Script `rastrear_registros_nulos.py` não autônomo | Não funciona fora do notebook |
| 6 | `data/processed/` vazio | Dados intermediários não persistidos |
| 7 | `requirements.txt` incompleto | Falta `python-docx`, sem versões fixas |
| 8 | Notebook carrega CSV direto (~922 MB) | Ignora o banco SQLite já criado |

### 🟢 Menores

| # | Problema | Impacto |
|---|---------|---------|
| 9 | `src/` e `docs/` vazios | Prometidos no README mas sem conteúdo |
| 10 | `bare except` no script de ETL | Má prática Python |
| 11 | CSV na pasta `notebooks/` | Deveria estar em `data/raw/` |
| 12 | Dois ambientes virtuais (`.venv` e `.venv-1`) | Confusão, espaço desperdiçado |
| 13 | `bfg-1.15.0.jar` na raiz | Ferramenta temporária não removida |
| 14 | Mensagens de commit inconsistentes | Dificulta rastreamento de mudanças |

---

## 9. Avaliação de Progresso

### 9.1 Progresso por Fase do KDD/CRISP-DM

| Fase do KDD | Status | Progresso |
|:------------|:------:|:---------:|
| 1. Compreensão do Negócio | ✅ Concluída | **100%** |
| 2. Compreensão dos Dados | ✅ Avançada | **80%** |
| 3. Preparação dos Dados | ⚠️ Parcial | **60%** |
| 4. Modelagem (ML) | ❌ Não iniciada | **0%** |
| 5. Avaliação | ❌ Não iniciada | **0%** |
| 6. Implantação/Apresentação dos Resultados | ⚠️ Parcial | **20%** |

### 9.2 Progresso por Fase do Plano do Artigo

| Fase do Plano | Progresso |
|:-------------|:---------:|
| Fase 0 — Definição do Objetivo | **100%** |
| Fase 1 — Tabelas e Figuras | **30%** |
| Fase 2 — Método (inclui ML) | **25%** |
| Fase 3 — Resultados | **15%** |
| Fase 4 — Discussão | **0%** |
| Fase 5 — Introdução | **0%** |
| Fase 6 — Resumo | **0%** |
| Fase 7 — Checklist | **0%** |

### **Progresso Geral Estimado: ~35%**

O projeto completou a **compreensão do problema** e a **preparação inicial dos dados**, incluindo o ETL completo (CSV → SQLite com tradução de códigos) e a análise exploratória geográfica básica para 8 subgrupos. Porém, as fases mais críticas — **análise estatística avançada**, **modelagem com ML** e **escrita do artigo** — ainda não foram iniciadas.

---

## 10. Próximos Passos Recomendados

### Fase 1 — Correções Urgentes 🔴 *(1 dia)*

- [ ] **Resolver conflitos de merge** no `pessoas_saudaveis.ipynb`
  - Opção 1: Resolver manualmente cada marcador `<<<<<<< HEAD` / `=======` / `>>>>>>>`
  - Opção 2: Recriar o notebook limpo com a versão mais atual do código
  - Testar se executa completamente após correção
- [ ] **Definir e documentar a faixa etária** — O projeto analisa idosos (≥60), jovens (18-29), ou ambos? Documentar claramente a decisão
- [ ] **Limpar repositório** — Remover `bfg-1.15.0.jar`, `.venv-1/`, ZIPs antigos da raiz

### Fase 2 — Preparação dos Dados 🟡 *(1-2 dias)*

- [ ] **Criar notebooks separados** para cada etapa (ETL, EDA, Modelagem, Resultados)
- [ ] **Usar o banco SQLite** para carregar dados no notebook (em vez do CSV de 922 MB)
- [ ] **Salvar dados processados** em `data/processed/` como CSVs filtrados por grupo
- [ ] **Completar o `requirements.txt`** com versões exatas (`pip freeze > requirements.txt`)
- [ ] **Tornar `rastrear_registros_nulos.py` autônomo** — Adicionar carregamento de dados

### Fase 3 — Análise Estatística Bivariada e Comparativa 🟡 *(2-3 dias)*

- [ ] **Análise Bivariada (Artrite vs Saudável):**
  - **Variáveis Categóricas:** Teste Qui-quadrado (χ²) com análise de resíduos padronizados para variáveis nominais e Teste de Mann-Whitney para ordinais.
  - **Variáveis Quantitativas:** Teste T de Student (se distribuição normal - Shapiro-Wilk) ou Mann-Whitney (se não normal) para comparar médias (ex: IMC, idade). Reportar p-valor e IC 95%.
- [ ] **Comparação das 4 Bases (ANOVA e Kruskal-Wallis):**
  - Comparar simultaneamente as 4 bases (Geral, Saudáveis, Com Artrite, Apenas Artrite) para justificar o uso da Base 4. 
  - Usar ANOVA one-way com post-hoc de Tukey ou Kruskal-Wallis com post-hoc de Dunn.
- [ ] **Análise de Prevalência:**
  - Calcular prevalência global de artrite com IC 95%.
  - Comparação de proporções (prop.test) por sexo, faixas etárias, escolaridade e renda.

### Fase 4 — Modelagem com Machine Learning (CAPTO + PICTOREA) 🔴 *(3-5 dias)*

- [ ] **Regressão Logística (Baseline):**
  - Executar análise univariada (p<0,20) e multivariada calculando Odds Ratios (OR) com IC 95%.
- [ ] **Otimização de Hiperparâmetros:**
  - Aplicar `RandomizedSearchCV` com 5-fold CV interno. Métrica-alvo: F1-Score macro. (Fixar `random_state`).
- [ ] **Treinamento e Validação Cruzada (10-fold):**
  - Executar Stratified 10-fold CV no conjunto de treino com Random Under Sampling (RUS) aplicado internamente a cada fold.
  - Calcular Média e IC 95% para Precisão, Recall e F1-Score.
- [ ] **Avaliação no Conjunto de Teste:**
  - Aplicar melhores modelos no teste (20% sem RUS).
  - Reportar Acurácia, AUC-ROC e Matriz de Confusão por classe.
- [ ] **Teste-T de Comparação de Modelos:**
  - Comparar estatisticamente o desempenho (F1-Score nos 10 folds) entre modelos (DT vs RF vs NB vs AdaBoost).

### Fase 5 — Extração de Conhecimento (Interpretabilidade) 🟡 *(2 dias)*

- [ ] **Feature Importance:** 
  - Extrair a importância dos atributos normalizada para os modelos baseados em árvore (Gini/MDI/pesos).
- [ ] **Extração de Regras da Árvore de Decisão:**
  - Limitar profundidade (`max_depth=5`) e exportar regras de classificação legíveis (caminhos de decisão). Ex: 'SE IMC > 27 ENTÃO Artrite'.
- [ ] **Análise por Dimensão CAPTO:**
  - Agrupar importâncias de atributos pelas dimensões CAPTO (Hábitos, Sociodemográficos, Antropometria) para ver qual dimensão tem maior poder preditivo.

### Fase 6 — Escrita do Artigo e Revisão Final 🟡 *(5-7 dias)*

- [ ] Seguir rigorosamente a estrutura do artigo (Método → Resultados → Discussão → Introdução → Resumo).
- [ ] Garantir que F1-scores e p-valores acompanham IC 95% e gráficos de barra iniciam no eixo Y=0.
- [ ] Preencher o Checklist STROBE (22 itens).

---

## 11. Melhorias de Qualidade Sugeridas

| # | Área | Melhoria | Impacto |
|---|------|----------|---------|
| 1 | **Código** | Modularizar funções em `src/` (carregamento, filtragem, análise, visualização) | Alto |
| 2 | **Código** | Adicionar logging em vez de `print()` para rastreamento | Médio |
| 3 | **Código** | Substituir `bare except` por exceções específicas | Médio |
| 4 | **Dados** | Mover `pns2019.csv` de `notebooks/` para `data/raw/` | Baixo |
| 5 | **Git** | Atualizar `.gitignore` para ignorar `.venv-1/`, `*.jar`, `*.zip` | Baixo |
| 6 | **Git** | Padronizar mensagens de commit (português, formato consistente) | Baixo |
| 7 | **Docs** | Preencher `docs/` com dicionário das variáveis selecionadas | Alto |
| 8 | **Docs** | Criar `CHANGELOG.md` com evolução do projeto | Baixo |
| 9 | **Notebook** | Adicionar sumário/índice no início do notebook | Médio |
| 10 | **Notebook** | Separar análise de idosos e jovens em notebooks distintos | Alto |

---

## 12. Resumo Executivo

### Pontos Fortes ✅
- **Estrutura de diretórios** bem organizada seguindo boas práticas
- **Script de ETL** funcional e bem comentado, processando ~293K registros com tradução de códigos
- **8 subgrupos** de análise com resultados exportados em 3 formatos (TXT, PDF, DOCX)
- **Plano do artigo** robusto, seguindo metodologia acadêmica sólida (PICOS/STROBE)
- **Banco de dados SQLite** já criado e populado para cada subgrupo

### Pontos de Atenção ⚠️
- **Notebook corrompido** por conflitos de merge Git não resolvidos
- **Análise superficial** — apenas contagens geográficas por estado/região
- **Inconsistência** entre faixa etária no código (18-29) e no plano (≥60)
- **Machine Learning** (requisito central) não implementado
- **Escrita do artigo** não iniciada

### Recomendação Final

> **Prioridade imediata:** Resolver os conflitos de merge, fixar a inconsistência na faixa etária, e implementar a pipeline de Machine Learning. O projeto possui uma boa fundação de dados e planejamento, mas precisa avançar nas fases de análise e modelagem para cumprir os requisitos da disciplina de Mineração de Dados.
>
> **Estimativa de esforço restante:** 12-18 dias de trabalho dedicado para completar todas as fases pendentes.

---

*Documento gerado automaticamente em 09/05/2026*
