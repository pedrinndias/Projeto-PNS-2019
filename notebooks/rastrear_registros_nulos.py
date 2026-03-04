import pandas as pd
import numpy as np

def analisar_nulos_por_modulo(df, nome_dataframe):
    print(f"--- Análise de Dados Faltantes: {nome_dataframe} ---")
    print(f"Total de registros: {df.shape[0]} | Total de colunas: {df.shape[1]}\n")
    
    nulos_por_coluna = df.isnull().sum()
    df_nulos = pd.DataFrame({'Coluna': nulos_por_coluna.index, 'Qtd_Nulos': nulos_por_coluna.values})
    
    df_nulos['Modulo'] = df_nulos['Coluna'].str.extract(r'^([a-zA-Z])', expand=False).str.upper()
    
    # Organiza por módulo e por coluna dentro de cada módulo
    df_nulos_sorted = df_nulos.sort_values(by=['Modulo', 'Coluna'])
    print("Nulos por coluna (quantidade), organizado por módulo:")
    for modulo, grupo in df_nulos_sorted.groupby('Modulo'):
        print(f"\nMódulo {modulo}:")
        print(grupo[['Coluna', 'Qtd_Nulos']].to_string(index=False))
    print("\n" + "="*50 + "\n")
    
    resumo_modulo = df_nulos.groupby('Modulo')['Qtd_Nulos'].agg(['mean', 'sum', 'count']).reset_index()
    resumo_modulo.columns = ['Módulo', 'Média de Nulos', 'Total de Nulos', 'Qtd de Colunas no Módulo']
    
    print("Resumo por módulo:")
    print(resumo_modulo.sort_values(by='Módulo').to_string(index=False))
    print("\n" + "="*50 + "\n")

analisar_nulos_por_modulo(df_bem, "Pessoas Bem")
analisar_nulos_por_modulo(df_atri_reu, "Pessoas com Artrite")
analisar_nulos_por_modulo(df_atri_reu_puro, "Artrite Pura")