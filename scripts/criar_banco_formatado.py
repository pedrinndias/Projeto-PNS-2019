import os  # Manipulação de caminhos e diretórios
import pandas as pd  # Manipulação de dados tabulares
import sqlite3  # Banco de dados SQLite
import glob  # Busca de arquivos por padrão

PASTA_DO_SCRIPT = os.path.dirname(os.path.abspath(__file__))  # Caminho da pasta deste script
if 'scripts' in PASTA_DO_SCRIPT.lower():  # Se o script está na pasta scripts
    DIRETORIO_RAIZ = os.path.dirname(PASTA_DO_SCRIPT)  # Define o diretório raiz
else:
    DIRETORIO_RAIZ = PASTA_DO_SCRIPT  # Caso contrário, o próprio diretório do script

PASTA_RAW = os.path.join(DIRETORIO_RAIZ, 'data', 'raw')  # Pasta de dados brutos
PASTA_DB = os.path.join(DIRETORIO_RAIZ, 'data', 'database')  # Pasta do banco de dados

def encontrar_csv():  # Busca o arquivo CSV principal da PNS 2019
    arquivos = glob.glob(os.path.join(PASTA_RAW, '*[pP][nN][sS]*2019*.csv'))  # Busca arquivos que contenham 'pns' e '2019'
    if arquivos:
        return arquivos[0]  # Retorna o primeiro encontrado
    return None  # Se não encontrar, retorna None

ARQUIVO_CSV = encontrar_csv()  # Caminho do arquivo CSV principal
ARQUIVO_BANCO = os.path.join(PASTA_DB, 'pns_master_formatado.db')  # Caminho do banco de dados SQLite

def encontrar_dicionario():  # Busca o arquivo de dicionário de dados
    arquivos = glob.glob(os.path.join(PASTA_RAW, '*dicionario*'))  # Busca arquivos que contenham 'dicionario'
    if arquivos:
        return arquivos[0]  # Retorna o primeiro encontrado
    return None  # Se não encontrar, retorna None

ARQUIVO_DIC = encontrar_dicionario()  # Caminho do dicionário de dados

def criar_banco_formatado():  # Função principal para criar o banco de dados formatado
    print("1. Lendo o dicionario de dados para criar o mapa de traducao...")  # Mensagem de status
    
    if not ARQUIVO_DIC:  # Verifica se o dicionário foi encontrado
        print("Erro: Arquivo do dicionario nao encontrado na pasta data/raw.")  # Mensagem de erro
        return  # Encerra a função
        
    if not ARQUIVO_CSV or not os.path.exists(ARQUIVO_CSV):  # Verifica se o CSV foi encontrado
        print("Erro: Arquivo CSV principal da PNS 2019 nao encontrado na pasta data/raw.")  # Mensagem de erro
        return  # Encerra a função

    if ARQUIVO_DIC.endswith('.csv'):  # Se o dicionário for CSV
        df_dic = pd.read_csv(ARQUIVO_DIC, skiprows=2)  # Lê o dicionário como CSV pulando as duas primeiras linhas
    else:
        df_dic = pd.read_excel(ARQUIVO_DIC, skiprows=2)  # Lê o dicionário como Excel pulando as duas primeiras linhas

    df_dic['Unnamed: 2'] = df_dic['Unnamed: 2'].ffill()  # Preenche valores ausentes na coluna 'Unnamed: 2' com o valor anterior
    df_dic = df_dic.dropna(subset=['Tipo ', 'Descrição'])  # Remove linhas sem tipo ou descrição

    def limpar_codigo(val):  # Função para limpar e padronizar códigos
        try:
            return str(int(float(val)))  # Tenta converter para inteiro e depois string
        except:
            return str(val).strip()  # Se falhar, retorna o valor como string sem espaços

    df_dic['clean_code'] = df_dic['Tipo '].apply(limpar_codigo)  # Aplica a limpeza de código

    mapa_traducao = {}  # Dicionário para mapear variáveis e códigos para descrições
    for var, group in df_dic.groupby('Unnamed: 2'):  # Agrupa por variável
        cod_to_desc = dict(zip(group['clean_code'], group['Descrição']))  # Cria dicionário código->descrição
        mapa_traducao[str(var).upper()] = cod_to_desc  # Adiciona ao mapa de tradução

    print(f"Dicionario mapeou {len(mapa_traducao)} variaveis com sucesso.")  # Mensagem de sucesso

    print("2. Descobrindo o separador do CSV (virgula ou ponto e virgula)...")  # Mensagem de status
    with open(ARQUIVO_CSV, 'r', encoding='utf-8', errors='ignore') as f:  # Abre o CSV para leitura
        primeira_linha = f.readline()  # Lê a primeira linha
        separador = ';' if ';' in primeira_linha else ','  # Define o separador

    print("3. Iniciando a leitura do CSV gigante e traducao (Isso pode demorar alguns minutos)...")  # Mensagem de status
    conn = sqlite3.connect(ARQUIVO_BANCO)  # Abre conexão com o banco de dados SQLite

    tamanho_lote = 20000  # Define o tamanho do lote para leitura em partes
    leitor_csv = pd.read_csv(
        ARQUIVO_CSV,  # Caminho do CSV
        chunksize=tamanho_lote,  # Lê em lotes
        dtype=str,  # Força leitura como string
        sep=separador,  # Usa o separador detectado
        encoding='utf-8',  # Define encoding
        on_bad_lines='skip'  # Ignora linhas problemáticas
    )

    lote_atual = 1  # Contador de lotes
    for chunk in leitor_csv:  # Para cada lote de dados
        print(f"Processando e formatando o lote {lote_atual}...")  # Mensagem de status
        
        chunk.columns = chunk.columns.str.upper()  # Padroniza nomes das colunas para maiúsculas
        colunas_para_traduzir = [c for c in chunk.columns if c in mapa_traducao]  # Seleciona colunas que precisam de tradução
        
        for col in colunas_para_traduzir:  # Para cada coluna a traduzir
            dicionario_da_coluna = mapa_traducao[col]  # Dicionário código->descrição da coluna
            
            chunk[col] = chunk[col].str.replace(r'\.0$', '', regex=True)  # Remove .0 do final dos códigos
            chunk[col] = chunk[col].str.strip()  # Remove espaços
            
            chunk[col] = chunk[col].map(dicionario_da_coluna).fillna(chunk[col])  # Traduz códigos para texto
            
        chunk.to_sql('pns_completa', conn, if_exists='append', index=False)  # Salva lote no banco de dados
        lote_atual += 1  # Incrementa o contador de lotes

    conn.close()  # Fecha a conexão com o banco de dados
    print("\nSucesso absoluto! O banco de dados foi criado e todos os codigos foram traduzidos para texto.")  # Mensagem final

if __name__ == '__main__':  # Executa a função principal se o script for chamado diretamente
    criar_banco_formatado()  # Chama a função principal