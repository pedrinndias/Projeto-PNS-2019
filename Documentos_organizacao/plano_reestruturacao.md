# 🔄 Plano de Reestruturação do Projeto PNS 2019

Este documento define a estratégia para "reiniciar" o projeto, garantindo um fluxo de trabalho limpo, profissional (baseado em Data Science/CRISP-DM) e alinhado aos novos guias metodológicos, **sem perder nenhum dado ou análise feita anteriormente**.

---

## 1. A Nova Estrutura de Diretórios Alvo

A organização do projeto passará a seguir esta hierarquia limpa:

```text
Projeto_PNS/
├── 📁 archive/                    ← 🛡️ NOVO: BACKUP SEGURO DE TUDO QUE É ANTIGO
│   ├── notebooks_antigos/         ← Seu notebook com conflito de merge vem pra cá
│   ├── resultados_antigos/        ← A pasta 'resultados_analise' e os arquivos .zip
│   └── lixo_raiz/                 ← O arquivo bfg-1.15.0.jar
│
├── 📁 data/                       ← DADOS (Nunca vai para o GitHub)
│   ├── raw/                       ← APENAS dados brutos (pns2019.csv, dicionários .xls)
│   ├── processed/                 ← Dados limpos e filtrados prontos para o ML
│   └── database/                  ← Seus bancos SQLite (esses se mantêm)
│
├── 📁 notebooks/                  ← 🚀 NOVOS NOTEBOOKS (Começando do zero)
│   ├── 01_extracao_pre_processamento.ipynb   ← Filtros, tratamento de nulos
│   ├── 02_analise_exploratoria_bivariada.ipynb ← Estatística, Teste T, Qui-quadrado
│   └── 03_machine_learning_capto.ipynb       ← Modelagem, Regressão Logística, Random Forest
│
├── 📁 scripts/                    ← Scripts utilitários soltos
│   ├── criar_banco_formatado.py   ← (Mantém como está)
│   └── rastrear_registros_nulos.py
│
├── 📁 docs/                       ← DOCUMENTAÇÃO
│   └── Documentos_organizacao/    ← Seus guias DOCX, planos e relatórios MD
│
├── README.md                      ← Descrição do projeto
├── requirements.txt               ← Dependências do projeto
└── .gitignore                     ← Arquivos ignorados pelo Git
```

---

## 2. Plano de Ação Passo a Passo

Para chegarmos na estrutura acima, execute os seguintes passos no seu terminal/VSCode:

### Passo 1: Criar as pastas de Backup e limpar a Raiz
Vamos criar uma pasta `archive` e mover tudo que está atrapalhando ou que é resultado antigo para lá.
1. Crie a pasta `archive`, e dentro dela crie `notebooks_antigos` e `resultados_antigos`.
2. Mova a pasta `resultados_analise` inteira para `archive/resultados_antigos/`.
3. Mova os arquivos `.zip` soltos na raiz para `archive/resultados_antigos/`.
4. Mova o arquivo `bfg-1.15.0.jar` para `archive/`.

### Passo 2: Limpar a pasta `notebooks/` e centralizar os Dados Brutos
Atualmente, a sua pasta `notebooks` está misturada com dados pesados e PDFs. Vamos separar o código dos dados.
1. Mova o arquivo `notebooks/pessoas_saudaveis.ipynb` para `archive/notebooks_antigos/`.
2. Mova **o gigantesco** `pns2019.csv` de `notebooks/` para `data/raw/` (é o lugar correto dele).
3. Na pasta `notebooks/`, existem arquivos duplicados (`dicionario_PNS_microdados_2019.xls`, `input_PNS_2019.sas`, `input_PNS_2019.txt`). Se eles já existem em `data/raw/`, **apague** as cópias que estão dentro da pasta `notebooks/`. Deixe a pasta `notebooks` completamente vazia.
4. Mova o arquivo `notebooks/Chaves_PNS_2019.pdf` para `docs/`.

### Passo 3: Limpar Ambientes Virtuais Duplicados
Você tem `.venv` e `.venv-1`. Isso causa confusão no VSCode.
1. Exclua a pasta `.venv-1` (geralmente uma cópia acidental). Mantenha apenas o `.venv`.

### Passo 4: Atualizar o `.gitignore`
Para garantir que seu repositório Git fique leve e não tente fazer o upload dos backups:
1. Abra o arquivo `.gitignore`.
2. Adicione as seguintes linhas ao final do arquivo:
```gitignore
# Backups e lixo
archive/
*.jar
*.zip
.venv-1/

# Ignorar CSVs e bancos em qualquer lugar
*.csv
*.db
```

### Passo 5: Criar os Novos Notebooks
Na pasta `notebooks/` recém-esvaziada, crie os três arquivos vazios a seguir. A numeração os manterá na ordem lógica de execução:
- `01_extracao_pre_processamento.ipynb`
- `02_analise_exploratoria_bivariada.ipynb`
- `03_machine_learning_capto.ipynb`

---

## 3. O Que Fazer nos Novos Notebooks?

Agora que o projeto está limpo, veja como o fluxo de trabalho será distribuído sem gerar códigos gigantescos e impossíveis de dar manutenção:

### 📔 Notebook 01: Extração e Pré-processamento
**Objetivo:** Carregar os dados e criar o dataset final que será usado em tudo.
- Conecte ao seu banco SQLite ou leia o `pns2019.csv` em *chunks*.
- Aplique o filtro de Idosos (`C008 >= 60`).
- Use o Dicionário de Variáveis para selecionar APENAS as colunas que importam (aquelas ~30 colunas do Guia).
- Crie a variável alvo (Target = `Q079`).
- Exporte o resultado final limpo como um arquivo pequeno (ex: `data/processed/dataset_idosos_artrite.csv`).

### 📔 Notebook 02: Análise Exploratória Bivariada
**Objetivo:** Gerar tabelas e gráficos estatísticos para o artigo.
- Carregue o arquivo `dataset_idosos_artrite.csv`.
- Faça testes de Qui-Quadrado (ex: Sexo vs Artrite).
- Faça testes T ou Mann-Whitney (ex: Idade/IMC vs Artrite).
- Gere gráficos e exporte para a pasta de imagens do seu artigo.

### 📔 Notebook 03: Machine Learning (CAPTO)
**Objetivo:** Treinar os modelos preditivos e extrair conhecimento.
- Carregue o arquivo `dataset_idosos_artrite.csv`.
- Faça o pré-processamento (One-Hot Encoding, SMOTE/RUS para balancear saudáveis vs artrite).
- Treine Regressão Logística, Árvore de Decisão e Random Forest.
- Plote as matrizes de confusão e curvas ROC.
- Extraia a *Feature Importance* e as Regras da Árvore de Decisão.

---

> 💡 **Pronto para começar?**  
> Se quiser, eu posso executar os **Passos 1 a 4** automaticamente para você no terminal via PowerShell, organizando as pastas, movendo os arquivos com segurança e atualizando o `.gitignore`. Me avise se posso fazer isso!
