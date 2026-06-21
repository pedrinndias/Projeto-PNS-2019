#!/usr/bin/env python
"""Garante os 4 bancos derivados (.db) que os notebooks NB02–06 leem em data/database/:
idosos_geral.db, idosos_artrite.db, idosos_artrite_puro.db, idosos_saudaveis.db
(cada um com a tabela `pns_idosos`).

Resolve os erros 'no such table: pns_completa' (NB01) e 'idosos_geral.db não encontrado'
/ KeyError 'Classe' (NB02), que ocorrem quando esses .db não existem.

Funciona em DOIS cenários, automaticamente:
  (A) se houver um banco MESTRE válido (pns_master_formatado.db com a tabela pns_completa),
      deriva os 4 grupos a partir dele — exatamente a lógica do NB01 (canônico); ou
  (B) se o mestre estiver ausente/vazio (o 'arquivo-fantasma' criado por um connect que
      falhou), reconstrói os 4 .db a partir dos CSVs em data/processed/csv/.

Rode UMA vez, da raiz do projeto:
    python notebooks/preparar_bancos.py
Depois: NB02 → NB02b → NB03 → NB03b → NB03c → NB04 → NB05 → NB06.
(Com este script, o NB01 fica dispensável.)
"""
import sqlite3
import sys
from pathlib import Path
import pandas as pd

BASE    = Path(__file__).resolve().parent.parent          # raiz do projeto (notebooks/ -> ..)
DB_DIR  = BASE / "data" / "database"
CSV_DIR = BASE / "data" / "processed" / "csv"
TABELA  = "pns_idosos"
MASTER  = DB_DIR / "pns_master_formatado.db"

# 14 doenças crônicas do Módulo Q (Q079 = artrite, a alvo). Igual ao NB01.
VARIAVEIS_DOENCAS = ['Q00201','Q03001','Q060','Q06306','Q068','Q074','Q079',
                     'Q088','Q092','Q11006','Q11604','Q120','Q124','Q128']
# CSV de origem -> .db de destino (cenário B)
MAP_CSV = {"idosos_geral.csv":"idosos_geral.db", "idosos_artrite.csv":"idosos_artrite.db",
           "idosos_artrite_puro.csv":"idosos_artrite_puro.db", "idosos_saudaveis.csv":"idosos_saudaveis.db"}
INV_CSV = {db: csv for csv, db in MAP_CSV.items()}   # .db de destino -> CSV de origem


def _tabelas(db_path):
    con = sqlite3.connect(db_path)
    try:
        return [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    finally:
        con.close()

def _eh_sim(val):
    if pd.isna(val): return False
    return str(val).strip().lower() in ('sim', '1')

def _eh_nao(val):
    if pd.isna(val): return False
    return str(val).strip().lower() in ('não', 'nao', '2')

def _gravar(df, db):
    dbp = DB_DIR / db
    if dbp.exists(): dbp.unlink()
    con = sqlite3.connect(dbp)
    try:
        df.to_sql(TABELA, con, if_exists="replace", index=False)
    finally:
        con.close()
    print(f"  ✅ {db:24s} {len(df):>7,} linhas × {df.shape[1]:>4} colunas")


def _db_valido(dbp):
    """True se o .db existe, não está vazio (0 byte = fantasma) e tem `pns_idosos` com linhas."""
    try:
        if not dbp.exists() or dbp.stat().st_size == 0:
            return False
        con = sqlite3.connect(dbp)
        try:
            if TABELA not in [r[0] for r in con.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'")]:
                return False
            return con.execute(f"SELECT COUNT(*) FROM {TABELA}").fetchone()[0] > 0
        finally:
            con.close()
    except Exception:
        return False


def _carregar_csv_robusto(csv_path):
    """Lê um CSV escolhendo o delimitador automaticamente.

    Os CSVs-semente da PNS usam ';' como separador e vírgula como decimal. Tentar ','
    primeiro pode 'ter sucesso' devolvendo UMA coluna (sem erro) num arquivo ';' — por isso
    NÃO basta pegar o primeiro que não falha. Aqui testamos ',', ';' e espaço e ficamos com
    o que produz MAIS colunas, garantindo que um arquivo ';' nunca vire um banco de 1 coluna."""
    melhor = None
    for sep in (";", ",", r"\s+"):
        try:
            df = pd.read_csv(csv_path, sep=sep, low_memory=False,
                             engine="python" if sep == r"\s+" else "c")
        except Exception:
            continue
        if melhor is None or df.shape[1] > melhor.shape[1]:
            melhor = df
    if melhor is None:
        raise RuntimeError(f"Não consegui ler {csv_path.name} com ',', ';' nem espaço.")
    return melhor


def _reconstruir_via_csv(dbs, verbose=True):
    """Reconstrói APENAS os .db pedidos a partir dos CSVs-semente. Levanta exceção (não sys.exit)
    para ser seguro de chamar dentro de um notebook."""
    if not CSV_DIR.exists():
        raise FileNotFoundError(
            f"Sem mestre válido e a pasta {CSV_DIR} não existe. É preciso o "
            f"pns_master_formatado.db REAL OU os idosos_*.csv em data/processed/csv/.")
    suspeitos = []
    for db in dbs:
        csv = INV_CSV.get(db)
        if csv is None:
            raise ValueError(f"Banco desconhecido para reconstrução: {db}")
        csv_path = CSV_DIR / csv
        if not csv_path.exists():
            raise FileNotFoundError(f"Falta o CSV-semente {csv_path} para reconstruir {db}.")
        df = _carregar_csv_robusto(csv_path)
        if df.shape[1] < 50:
            suspeitos.append(db)
        _gravar(df, db)
    if suspeitos and verbose:
        print(f"\n⚠️  {suspeitos} têm POUCAS colunas — se forem subconjuntos, os notebooks "
              "vão reclamar de coluna ausente (ex.: V0015/Q079). Aí você precisa do mestre REAL.")


def garantir_bancos(necessarios=None, verbose=True):
    """Bootstrap IDEMPOTENTE para os notebooks NB01–NB03c.

    Garante que os .db pedidos existam e sejam válidos, regenerando APENAS os que
    faltam — a partir do mestre (se válido) ou dos CSVs-semente. Não faz nada (rápido)
    quando os bancos já estão ok. Uso no topo do notebook:

        from preparar_bancos import garantir_bancos
        garantir_bancos(['idosos_artrite_puro.db', 'idosos_saudaveis.db'])

    `necessarios=None` garante os 4 bancos. Levanta FileNotFoundError se não houver
    como preparar (sem mestre e sem CSVs-semente)."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    necessarios = list(necessarios) if necessarios else list(MAP_CSV.values())

    # remove o 'arquivo-fantasma' do mestre (0 byte / sem a tabela pns_completa)
    if MASTER.exists() and 'pns_completa' not in _tabelas(MASTER):
        MASTER.unlink()
        if verbose:
            print(f"[bootstrap] removido {MASTER.name} INVÁLIDO (arquivo-fantasma).")

    faltam = [db for db in necessarios if not _db_valido(DB_DIR / db)]
    if not faltam:
        return                       # tudo certo — silencioso e rápido

    if verbose:
        print(f"[bootstrap] regenerando banco(s) ausente(s)/inválido(s): {faltam}")
    if MASTER.exists() and 'pns_completa' in _tabelas(MASTER):
        via_mestre()                 # mestre válido → deriva todos os grupos (cobre o subconjunto)
    else:
        _reconstruir_via_csv(faltam, verbose=verbose)

    ainda = [db for db in necessarios if not _db_valido(DB_DIR / db)]
    if ainda:
        raise FileNotFoundError(
            f"[bootstrap] não consegui preparar {ainda}. É preciso o mestre "
            f"pns_master_formatado.db em data/database/ OU os CSVs-semente em {CSV_DIR}.")
    if verbose:
        print("[bootstrap] ✅ bancos prontos.")


def via_mestre():
    """Cenário A — deriva os 4 grupos do banco mestre (lógica do NB01)."""
    print("Cenário A: banco mestre válido encontrado → derivando os 4 grupos (lógica do NB01).")
    con = sqlite3.connect(MASTER)
    try:
        df = pd.read_sql_query("SELECT * FROM pns_completa WHERE CAST(C008 AS INTEGER) >= 60", con)
    finally:
        con.close()
    faltam = [c for c in VARIAVEIS_DOENCAS if c not in df.columns]
    if faltam:
        sys.exit(f"ERRO: o mestre não tem as colunas de doença: {faltam}. Mestre incompleto?")
    mask_art = df['Q079'].apply(_eh_sim)
    outras = [c for c in VARIAVEIS_DOENCAS if c != 'Q079']
    try:    mask_out = df[outras].map(_eh_sim).any(axis=1)
    except AttributeError: mask_out = df[outras].applymap(_eh_sim).any(axis=1)
    try:    mask_sau = df[VARIAVEIS_DOENCAS].map(_eh_nao).all(axis=1)
    except AttributeError: mask_sau = df[VARIAVEIS_DOENCAS].applymap(_eh_nao).all(axis=1)
    _gravar(df,                         "idosos_geral.db")
    _gravar(df[mask_art],               "idosos_artrite.db")
    _gravar(df[mask_art & ~mask_out],   "idosos_artrite_puro.db")
    _gravar(df[mask_sau],               "idosos_saudaveis.db")


def via_csv():
    """Cenário B (CLI) — reconstrói os 4 .db a partir dos CSVs derivados."""
    print("Cenário B: sem mestre válido → reconstruindo a partir dos CSVs em data/processed/csv/.")
    try:
        _reconstruir_via_csv(list(MAP_CSV.values()))
    except (FileNotFoundError, RuntimeError, ValueError) as e:
        sys.exit(f"ERRO: {e}")


def main():
    print(f"Projeto: {BASE}\nBancos : {DB_DIR}\n")
    DB_DIR.mkdir(parents=True, exist_ok=True)

    mestre_valido = MASTER.exists() and ('pns_completa' in _tabelas(MASTER))
    if MASTER.exists() and not mestre_valido:
        MASTER.unlink()   # remove o 'arquivo-fantasma' (sem a tabela pns_completa)
        print(f"[limpeza] removido {MASTER.name} INVÁLIDO (não tinha a tabela pns_completa — "
              "era o arquivo-fantasma do connect que falhou).\n")

    if mestre_valido:
        via_mestre()
    else:
        via_csv()

    # Conferência rápida
    print("\nConferência (esperado: artrite=4025, pura=494, saudáveis=4332):")
    for db in ("idosos_geral.db","idosos_artrite.db","idosos_artrite_puro.db","idosos_saudaveis.db"):
        p = DB_DIR / db
        if not p.exists():
            print(f"  {db:24s}: AUSENTE"); continue
        con = sqlite3.connect(p)
        try:    n = con.execute(f"SELECT COUNT(*) FROM {TABELA}").fetchone()[0]
        finally: con.close()
        print(f"  {db:24s}: {n:,} registros")
    print("\n✅ Pronto. Rode em ordem (Restart Kernel + Run All em cada):")
    print("   NB02 → NB02b → NB03 → NB03b → NB03c → NB04 → NB05 → NB06")


if __name__ == "__main__":
    main()
