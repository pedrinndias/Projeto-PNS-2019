## 1. Padrão metodológico dos 6 artigos da PUC Minas

Olhando os artigos (DPOC, TOC, Depressão, Hipertensão, AVC e Artrite-Depressão), todos seguem **a mesma espinha dorsal** — que é exatamente o método CAPTO+PICTOREA do seu projeto:

| Etapa | O que fazem | Variação entre artigos |
|---|---|---|
| **1. Seleção conceitual** | Mapa CAPTO → seleção de ~12-30 atributos | Igual em todos |
| **2. Fusão/transformação** | Cria IMC, faixa etária, score alimentar, jornada de trabalho, vulnerabilidade econômica, nível de fumo, etc. | Cada artigo cria 5-10 atributos derivados |
| **3. Categorização (discretização ordinal)** | Transforma quantitativas em níveis de risco (IMC OMS, idade em faixas, etc.) | DPOC e Hipertensão são os mais agressivos nisso |
| **4. Tratamento de ausentes** | Imputa NaN como "menor risco" ou pela moda/mediana por classe | Depressão usa threshold de 60% para descartar coluna |
| **5. Outliers** | Z-score > 4 OU IQR (Q1-1,5·IQR, Q3+1,5·IQR) | Idade e renda são os principais alvos |
| **6. Codificação** | OrdinalEncoder para escalas, One-Hot para nominais | Padrão consistente |
| **7. Split** | 70/30 ou 80/20, estratificado, `random_state=42` | DPOC usa 90/10 |
| **8. Balanceamento** | **RandomUnderSampler** (RUS) na classe majoritária | Cancella aplica em treino+teste; outros só no treino |
| **9. ML** | Árvore, RF, Naive Bayes, AdaBoost, MLP, Regressão Logística | Todos com 10-fold CV + `RandomizedSearchCV` |

O artigo do **Cancella (Artrite + Depressão, 2025)** é o mais próximo do seu domínio. Ele:
- Identifica 23 atributos via CAPTO, mas só conseguiu mapear na PNS 12-19
- Descarta colunas com >60% de NaN
- Categoriza IMC, vulnerabilidade econômica (renda < ¼ SM)
- Aplica RUS pra balancear (saudáveis: 312, artrite+depressão: 752 → equilibra)
- Usa árvore + floresta — F1 entre 76% e 80%
- Conclui: idosos têm regras "intrínsecas" (sexo, diabetes, autopercepção); adultos meia-idade têm regras "comportamentais"

---

## 2. Estado atual dos seus notebooks

**Notebook 01** entrega 3 bancos SQLite filtrados (≥60 anos):
- `idosos_artrite.db` — Q079=1 (com comorbidades) → provavelmente ~4.025 idosos
- `idosos_artrite_puro.db` — Q079=1 E todas outras 13=2 → **494 idosos**
- `idosos_saudaveis.db` — todas as 14=2 → **4.332 idosos**

**Notebook 02** já fez a EDA com filtros V0015+M001, gerou as 6 tabelas e 5 gráficos, identificou que **8 variáveis** são significativas pra distinguir artrite vs saudável (Sexo, IMC, Idade, Renda, Autoavaliação, Frutas, Refrigerante, Plano de Saúde).

**O gap**: entre o que o notebook 02 produziu (dataset analítico bruto) e o que o notebook 03 precisa (X_train, X_test, y_train, y_test, features codificadas, classes balanceadas), há um **vão de preparação para ML** que ainda não existe.

---

## 3. Proposta de estrutura: Notebook 02b — Preparação para ML

Sugiro **um notebook intermediário** chamado `02b_preparacao_ml.ipynb`, para não inflar o 03 com 600 linhas de transformação de features antes do modelo. Esse é o padrão que o Pedro Henrique (Depressão) usa: ele tem um diagrama de 11 etapas só de preparação antes da modelagem.

### Fluxo proposto do Notebook 02b

```
Carrega bancos SQLite (saudáveis + artrite) → aplica V0015+M001
        ↓
Engenharia de features (fusão CAPTO)
   • IMC + categorização OMS
   • Faixa etária (60-69, 70-79, 80+)
   • Score alimentar (saudável/intermediário/não saudável)
   • Vulnerabilidade econômica (renda < ¼ SM)
   • Nível de exercício físico (combina P034+P035)
   • Autoavaliação de saúde (já existe, só limpar)
        ↓
Tratamento de ausentes (decisão: imputar ou descartar?)
        ↓
Tratamento de outliers (Idade, IMC, Renda)
        ↓
Análise de entropia + correlação (remover features irrelevantes)
        ↓
Codificação (One-Hot nominais, Ordinal escalas)
        ↓
Split estratificado 80/20 (random_state=42)
        ↓
Salva em data/processed/:
   • X_train.csv / y_train.csv
   • X_test.csv  / y_test.csv
   • dicionario_features.csv (nome, tipo, dimensão CAPTO)
```

**Observação importante sobre balanceamento**: pelas instruções do seu projeto, "RUS aplicado dentro de cada fold da CV (não fora — evite vazamento)". Então o **RUS em si não acontece no 02b** — ele fica embutido no Pipeline `imblearn` dentro do `RandomizedSearchCV` do Notebook 03. O 02b só prepara, codifica e divide.

---

## 4. Decisões metodológicas que preciso confirmar antes de codar

Estas são as escolhas que vão mudar o resultado final do artigo. Não dá pra avançar 300 linhas de código antes de fixar:

### Q1. Qual classe usar como "Artrite"?
- **A) Artrite com comorbidades** (`idosos_artrite.db`, n≈4.025) — mais realista, mais poder estatístico
- **B) Artrite Pura** (`idosos_artrite_puro.db`, n=494) — comparação "limpa" com saudáveis, mas amostra pequena pra ML
- **C) Ambas** — treinar dois modelos paralelos e comparar

### Q2. Usar comorbidades como features?
- Se a resposta da Q1 for A, faz sentido manter Q00201, Q03001, Q092, Q088 como **features preditoras** (jeito Cancella) — pode dar regras tipo "SE diabetes E hipertensão → artrite"
- Se for B, comorbidades são **constantes=2** e tem que excluir

### Q3. Tratamento de ausentes
- **A) Imputar pela moda/mediana** (estratificado por classe) — preserva n
- **B) Descartar coluna se >60% NaN, imputar resto** (padrão Cancella/Pedro Henrique)
- **C) Descartar linhas com qualquer NaN** — mais limpo, mas perde n

### Q4. Outliers
- **A) Manter tudo** — idosos com IMC 40+ fazem parte do estudo, não são erro
- **B) Remover via IQR** (padrão Hipertensão/DPOC) — Q1-1,5·IQR, Q3+1,5·IQR
- **C) Híbrido**: só remover valores fisicamente impossíveis (altura 0,3m, peso 500kg)

### Q5. Discretização das quantitativas
- **A) Manter contínuas** (IMC, idade, renda como números) — melhor pra Regressão Logística
- **B) Discretizar tudo em ordinais** (padrão CAPTO/DPOC) — melhor pra interpretabilidade da Árvore

### Q6. Onde colocar o notebook?
- **A) Novo arquivo** `02b_preparacao_ml.ipynb` entre 02 e 03 (mais modular)
- **B) Primeiras seções do 03** (mais coeso, mas o 03 fica grande)

---

Me responde essas 6 perguntas (pode ser só "A, A, B, C, A, A" ou explicando) que eu monto o esqueleto do notebook na sequência, com as células decoradas no padrão dos outros, comentários linha-a-linha em PT-BR e `random_state=42` em tudo. Se preferir, posso já começar com as escolhas que considero mais defensáveis pro artigo e você me corrige.


**RESPOSTA**
1-C
2-Não sei 
3-B Não usei 60%, usei 75% de valores faltantes para retirar a coluna
4-B Remover os outilers seguindo a metodologia que eu usei, 3 desvios padões
5-B
6- Vamos criar essa engenharia de features como um notebook 4 antes de iniciar o 5 que será a modelagem
