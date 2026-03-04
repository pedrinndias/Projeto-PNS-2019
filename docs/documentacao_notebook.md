# Documentação do Notebook: Análise de Pessoas Saudáveis e com Artrite/Reumatismo (PNS 2019)

## 1. Introdução
Este notebook realiza uma análise dos dados da Pesquisa Nacional de Saúde (PNS) 2019, focando em pessoas com mais de 60 anos, identificando indivíduos saudáveis e aqueles com artrite/reumatismo, além de gerar visualizações para comparação.

## 2. Bibliotecas Utilizadas
- pandas: manipulação de dados.
- numpy: operações numéricas.
- matplotlib.pyplot: visualização de dados.

## 3. Carregamento e Filtragem dos Dados
O arquivo `pns2019.csv` é carregado em um DataFrame. Filtra-se apenas os registros de pessoas com mais de 60 anos (`df['C008'] > 60`).

```python
df = pd.read_csv("pns2019.csv")
df = df[df['C008'] > 60]
```

## 4. Seleção de Colunas de Doenças Crônicas
Define-se uma lista de colunas relacionadas a doenças crônicas. Filtra-se pessoas sem nenhuma dessas doenças (`df_bem`). Filtra-se pessoas com artrite/reumatismo (`df_atri_reu`).

```python
cols = ["Q00201","Q03001","Q060","Q06306","Q068","Q074","Q079","Q088","Q092","Q11006","Q11604","Q120","Q128"]
df_bem = df[df[cols].eq(2).all(axis=1)]
df_atri_reu = df[df['Q079'] == 1]
```

## 5. Identificação de Casos Puros de Artrite/Reumatismo
Remove-se a coluna `Q079` da lista de doenças crônicas. Filtra-se pessoas que não possuem nenhuma das outras doenças crônicas, mas possuem artrite/reumatismo.

```python
cols.remove("Q079")
df_atri_reu_puro = df[(df[cols].eq(2).all(axis=1))]
df_atri_reu_puro = df_atri_reu_puro[df_atri_reu_puro["Q079"] == 1]
```

## 6. Visualização dos Dados
Une os DataFrames de pessoas saudáveis e com artrite/reumatismo. Plota histogramas da idade para ambos os grupos, facilitando a comparação.

```python

```

## 7. Resultados
O notebook imprime o número de registros em cada grupo analisado. Os histogramas permitem comparar a distribuição de idade entre pessoas saudáveis e com artrite/reumatismo.

## 8. Conclusão
O notebook fornece uma base para análise do perfil de saúde de idosos na PNS 2019, permitindo identificar padrões e possíveis fatores associados à presença de doenças crônicas.
