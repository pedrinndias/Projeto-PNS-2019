# Documentação do Projeto PNS

## Estrutura de Pastas do Projeto

```
data/
  database/
  processed/
  raw/
    input_PNS_2019.sas
    input_PNS_2019.txt
    PNS_2019.txt
    pns2019.csv
docs/
  arquitetura_projeto.md
notebooks/
  pessoas_saudaveis.ipynb
  pns2019.csv
scripts/
  criar_banco_formatado.py
src/
```

## Modificações Realizadas

- Adicionados comentários explicativos nas células de código do notebook `pessoas_saudaveis.ipynb`, detalhando o propósito de cada linha.
- Comentários inseridos principalmente nos trechos de filtragem de dados e visualização (histograma).
- Observação: sugerido substituir `plt.plot` por `plt.show()` para exibir o gráfico corretamente.

## Estrutura Atual do Notebook `pessoas_saudaveis.ipynb`

1. **Importação de bibliotecas**
   - pandas, numpy, matplotlib.pyplot
2. **Leitura e filtragem inicial dos dados**
   - Leitura do arquivo `pns2019.csv`
   - Seleção de registros com idade maior que 60 anos
3. **Definição de colunas de doenças crônicas**
   - Lista de colunas relacionadas a doenças crônicas
   - Filtragem de pessoas sem doenças crônicas
   - Filtragem de pessoas com artrite/reumatismo
4. **Filtragem de pessoas com artrite/reumatismo puro**
   - Remoção da coluna de artrite da lista de doenças crônicas
   - Seleção de pessoas sem outras doenças crônicas, mas com artrite/reumatismo
5. **Visualização dos DataFrames filtrados**
   - Exibição dos DataFrames resultantes
6. **Concatenação de DataFrames**
   - União dos DataFrames de pessoas saudáveis e com artrite/reumatismo
7. **Visualização gráfica**
   - Plotagem de histogramas das idades dos grupos analisados

## O que o Notebook Está Fazendo

O notebook tem como objetivo analisar dados da PNS 2019 para pessoas com mais de 60 anos, segmentando em grupos:
- Pessoas sem doenças crônicas
- Pessoas com artrite/reumatismo
- Pessoas com artrite/reumatismo puro (sem outras doenças crônicas)

Após o processamento, são gerados histogramas para comparar a distribuição de idades entre os grupos.

## Sugestões de Melhoria
- Substituir `plt.plot` por `plt.show()` para exibir o gráfico.
- Adicionar mais comentários e documentação para facilitar a manutenção.
- Considerar salvar os DataFrames filtrados para análises futuras.
