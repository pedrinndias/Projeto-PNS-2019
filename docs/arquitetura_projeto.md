# Arquitetura de Pastas e Arquivos do Projeto

Este documento descreve a organização das pastas e arquivos do repositório, explicando o propósito de cada diretório principal.

## Estrutura Geral

```
data/
  database/
  processed/
  raw/
docs/
notebooks/
scripts/
src/
```

## Descrição dos Diretórios

### data/
Armazena todos os dados utilizados e gerados pelo projeto. Subdividido em:
- **database/**: Para bancos de dados ou arquivos de armazenamento estruturado.
- **processed/**: Para dados já tratados, limpos ou prontos para análise/modelagem.
- **raw/**: Para dados brutos, originais, sem qualquer tratamento.

### docs/
Diretório para documentação do projeto, como manuais, resumos, atas de reunião, diagramas e arquivos explicativos.

### notebooks/
Local reservado para Jupyter Notebooks ou outros arquivos de experimentação interativa, análises exploratórias e prototipagem.

### scripts/
Scripts utilitários, de automação, limpeza, extração ou transformação de dados. Ideal para códigos que não fazem parte do produto final, mas auxiliam no fluxo de trabalho.

### src/
Código-fonte principal do projeto. Aqui devem ficar os módulos, pacotes, funções e classes que compõem a lógica central do sistema, pipelines, dashboards, etc.

## Recomendações de Organização
- Mantenha cada tipo de arquivo em seu diretório correspondente.
- Use subpastas para separar diferentes etapas ou componentes, se necessário.
- Documente scripts e módulos para facilitar a manutenção e colaboração.

---

Esta arquitetura visa garantir organização, clareza e escalabilidade ao longo do desenvolvimento do projeto.