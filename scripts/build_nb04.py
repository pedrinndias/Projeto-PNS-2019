"""
Gera o notebook 04_eliminacao_outliers.ipynb de forma idempotente.

Notebook dedicado à etapa de eliminação de outliers, conforme metodologia
discutida com o orientador (Prof. Luis Enrique Zárate) e baseada nos
trabalhos do laboratório LICAP:

- Cancella & Zárate 2025 (Artrite-Depressão)   — mesma temática do projeto
- Silva & Zárate 2024 (Depressão em adultos)   — abordagem em dois estágios
- Melo, Gomes & Zárate 2024 (DPOC)             — IQR × 1,5 clássico

Metodologia híbrida adotada:

  Estágio 1 — z-score > 4         → remoção de instâncias (erros absurdos)
  Estágio 2 — IQR × 1,5 por classe → substituição por NaN + re-imputação
  Exceção  — Renda per capita      → corte por média ± 2σ (assimetria forte)
"""
from __future__ import annotations
import json, uuid
from pathlib import Path

NB_PATH = Path(__file__).resolve().parents[1] / "notebooks" / "04_eliminacao_outliers.ipynb"


def _cid() -> str:
    return uuid.uuid4().hex[:12]


def md(*lines: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": _cid(),
        "metadata": {},
        "source": [l if l.endswith("\n") else l + "\n" for l in lines][:-1] + [lines[-1]],
    }


def code(*lines: str) -> dict:
    return {
        "cell_type": "code",
        "id": _cid(),
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [l if l.endswith("\n") else l + "\n" for l in lines][:-1] + [lines[-1]],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Conteúdo do notebook
# ─────────────────────────────────────────────────────────────────────────────

cells: list[dict] = []

cells.append(md(
"""# Notebook 04 — Eliminação de Outliers

**Projeto:** Mineração de Dados em Saúde · PNS 2019
**Estudo:** Artrite e Reumatismo em Idosos Brasileiros
**Pesquisador:** Pedro Dias Soares
**Orientador:** Prof. Dr. Luis Enrique Zárate — PUC Minas
**Periódico-alvo:** Journal of Health Informatics (JHI/SBIS)

---

## Por que esta etapa existe?

A eliminação de outliers foi solicitada pelo orientador como **etapa
metodologicamente isolada**, em notebook próprio, para que cada decisão
seja auditável e rastreável. Outliers em bases epidemiológicas
(idade = 250 anos, peso = 7 kg, IMC = 200) distorcem média, IQR, e
quaisquer estimativas que alimentam o classificador.

## Metodologia híbrida (estilo LICAP)

Baseada em três trabalhos do orientador sobre a PNS 2019:

| Etapa | Critério | O que faz | Inspirado em |
|-------|----------|-----------|--------------|
| 1 | **z-score > 4** | Remove instâncias com valores absurdos (erros de digitação) | Silva & Zárate 2024 |
| 2 | **IQR × 1,5 por classe** | Substitui valores extremos por NaN; re-imputa pela média/moda da classe | Melo et al. 2024 (DPOC), Cancella & Zárate 2025 |
| 3 | **Renda: média ± 2σ** | Tratamento específico para a assimetria forte de `VDF004` | Cancella & Zárate 2025 |

## Fluxo do notebook

| # | Etapa | O que faz |
|---|-------|-----------|
| 1 | Configuração | Imports, caminhos, constantes |
| 2 | Carregamento | Lê SQLite (artrite pura + saudáveis) e converte tipos |
| 3 | Inventário | Identifica variáveis contínuas e discretas tratáveis |
| 4 | Diagnóstico | Boxplots e estatísticas por classe (antes) |
| 5 | Estágio 1 | z-score > 4 → remoção de instâncias |
| 6 | Estágio 2 | IQR × 1,5 por classe → NaN |
| 7 | Exceção | Renda: média ± 2σ |
| 8 | Re-imputação | Média (numéricas) / moda (categóricas) por classe |
| 9 | Sanidade | Boxplots depois + comparação antes/depois |
| 10 | Exportação | CSV limpo + relatório JSON de rastreabilidade |

> Convenção de cor: <span style="color:#C0392B">**vermelho = Com Artrite**</span>, <span style="color:#27AE60">**verde = Saudável**</span>.
"""
))

cells.append(md(
"""## 1 · Configuração do ambiente

- **`Z_LIMITE = 4`** — z-score máximo aceitável no Estágio 1 (segue Silva 2024).
- **`IQR_MULT = 1.5`** — multiplicador IQR no Estágio 2 (Tukey clássico, padrão LICAP).
- **`SIGMA_RENDA = 2`** — desvios-padrão aceitos para `VDF004` no Estágio 3 (segue Cancella 2025).
- **`RANDOM_STATE = 42`** — semente para reprodutibilidade.

Por classe: todos os limites são recalculados separadamente para
`Saudável` e `Com Artrite`, preservando diferenças clínicas reais entre
os grupos."""
))

cells.append(code(
"""# Bibliotecas-padrão
import sqlite3, os, math, warnings, json   # I/O, matemática, supressão de warnings, JSON
# Manipulação de tabela e cálculo numérico
import pandas as pd                         # DataFrames
import numpy as np                          # operações vetoriais
# Visualização
import matplotlib.pyplot as plt             # plots base
import seaborn as sns                       # boxplots estilizados
# Estatística
from scipy import stats                     # z-score

warnings.filterwarnings('ignore')           # silencia avisos esperados (qcut, divisão por zero)

# ── Caminhos (relativos a notebooks/) ─────────────────────────────────
PASTA_DB       = '../data/database/'                       # bancos SQLite por subgrupo
DIR_RESULTADOS = '../data/results/outliers/'               # saídas DESTE notebook
DIR_FIGURAS    = DIR_RESULTADOS + 'figuras/'               # PNGs comparativos
DIR_TABELAS    = DIR_RESULTADOS + 'tabelas/'               # CSVs de log
for pasta in [DIR_RESULTADOS, DIR_FIGURAS, DIR_TABELAS]:   # cria pastas se não existirem
    os.makedirs(pasta, exist_ok=True)

# ── Hiperparâmetros do pipeline de outliers ───────────────────────────
RANDOM_STATE = 42       # semente fixa para reprodutibilidade
Z_LIMITE     = 4        # Estágio 1 — z-score máximo (Silva 2024)
IQR_MULT     = 1.5      # Estágio 2 — multiplicador IQR (Tukey/Cancella 2025/Melo 2024)
SIGMA_RENDA  = 2        # Estágio 3 — desvios-padrão para Renda (Cancella 2025)

# ── Paleta cromática consistente entre notebooks ──────────────────────
COR_ARTRITE  = '#C0392B'  # vermelho
COR_SAUDAVEL = '#27AE60'  # verde

# ── Estilo dos plots ──────────────────────────────────────────────────
sns.set_theme(style='whitegrid', font_scale=1.1)
plt.rcParams.update({
    'figure.dpi': 120,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# ── Helpers de I/O ────────────────────────────────────────────────────
def salvar_fig(nome):                                       # salva figura ativa
    caminho = DIR_FIGURAS + nome
    plt.savefig(caminho, dpi=150, bbox_inches='tight')
    print(f'  ✅ Figura → {caminho}')

def salvar_tab(df, nome):                                   # salva log em CSV (utf-8-sig p/ Excel BR)
    caminho = DIR_TABELAS + nome
    df.to_csv(caminho, index=False, encoding='utf-8-sig')
    print(f'  ✅ Tabela → {caminho}')

print('Configuração ok.')
print(f'  Z_LIMITE    : {Z_LIMITE}σ (Estágio 1)')
print(f'  IQR_MULT    : {IQR_MULT}×IQR por classe (Estágio 2)')
print(f'  SIGMA_RENDA : {SIGMA_RENDA}σ para VDF004 (Estágio 3)')
"""
))

cells.append(md(
"""## 2 · Carregamento dos dados

Para que esta etapa seja **auditável de forma isolada**, lemos os bancos
SQLite originais gerados no NB01 — **antes** de qualquer tratamento de
outliers feito anteriormente. Assim, qualquer revisor consegue rodar
este notebook do zero e reproduzir cada decisão.

Bancos lidos:

- `idosos_artrite_puro.db` (494 indivíduos)
- `idosos_saudaveis.db` (4 332 indivíduos)

Em seguida convertemos os campos numéricos (que vêm como texto no SQLite)
para tipos apropriados."""
))

cells.append(code(
"""# Variáveis contínuas — alvo principal do tratamento de outliers
VARS_CONTINUAS = [
    'P00104',   # Peso aferido (kg)
    'P00404',   # Altura aferida (cm)
    'VDF004',   # Renda per capita (quintil 1–7) — tratamento ESPECIAL
]

# Variáveis discretas — recebem IQR (sem z-score, pois faixa é limitada)
VARS_DISCRETAS = [
    'C008',     # Idade (anos)
    'P04501',   # Televisão (horas/dia)
    'P00901',   # Verduras/legumes (dias/sem.)
    'P015',     # Peixe (dias/sem.)
    'P018',     # Frutas (dias/sem.)
    'P01101',   # Carne vermelha (dias/sem.)
    'P02501',   # Doces/ultraprocessados (dias/sem.)
    'P02002',   # Refrigerante (dias/sem.)
    'P02001',   # Suco em pó/caixinha (dias/sem.)
    'P023',     # Leite (dias/sem.)
    'P01601',   # Suco de fruta natural (dias/sem.)
    'P02602',   # Lanche rápido/almoço (dias/sem.)
]

# Variáveis categóricas mantidas no DataFrame (NÃO recebem tratamento de outlier)
VARS_CATEGORICAS = [
    'C006',    # Sexo
    'VDD004A', # Escolaridade
    'N001',    # Autoavaliação de saúde
    'Q079',    # Variável-alvo (artrite Sim/Não)
]

TODAS_VARS = VARS_CONTINUAS + VARS_DISCRETAS + VARS_CATEGORICAS
VARS_NUM   = VARS_CONTINUAS + VARS_DISCRETAS   # alvo da etapa de outliers

print(f'Contínuas (z-score + IQR): {len(VARS_CONTINUAS)}')
print(f'Discretas (IQR somente)  : {len(VARS_DISCRETAS)}')
print(f'Categóricas (preservadas): {len(VARS_CATEGORICAS)}')
"""
))

cells.append(code(
"""def carregar_subgrupo(arquivo_db: str, rotulo_classe: str) -> pd.DataFrame:
    \"\"\"Lê um banco SQLite e retorna um DataFrame com a coluna 'Classe'.\"\"\"
    caminho = os.path.join(PASTA_DB, arquivo_db)              # caminho completo
    conn    = sqlite3.connect(caminho)                        # abre conexão
    df      = pd.read_sql_query('SELECT * FROM pns_idosos', conn)  # lê tabela inteira
    conn.close()                                              # fecha sempre
    # Filtra apenas as colunas de interesse, ignorando ausentes no SQLite
    cols_ok = [c for c in TODAS_VARS if c in df.columns]
    df = df[cols_ok].copy()
    df['Classe'] = rotulo_classe                              # rotula o subgrupo
    return df

# Carrega os dois subgrupos
df_artrite   = carregar_subgrupo('idosos_artrite_puro.db', 'Com Artrite')
df_saudaveis = carregar_subgrupo('idosos_saudaveis.db',     'Saudável')

# Junta verticalmente
df_raw = pd.concat([df_saudaveis, df_artrite], ignore_index=True)

print('=' * 70)
print('  Subgrupos carregados')
print('=' * 70)
print(f'  Com Artrite : {(df_raw["Classe"] == "Com Artrite").sum():>5,}')
print(f'  Saudável    : {(df_raw["Classe"] == "Saudável").sum():>5,}')
print(f'  Total       : {len(df_raw):>5,}')
print(f'  Colunas     : {df_raw.shape[1]}')
"""
))

cells.append(code(
"""# ── Converte numéricas (vêm como texto do SQLite) ────────────────────
for col in VARS_NUM:
    if col not in df_raw.columns:
        continue                                              # pula coluna ausente
    if col in ('P00104', 'P00404'):                           # peso/altura usam vírgula decimal
        df_raw[col] = pd.to_numeric(
            df_raw[col].astype(str).str.replace(',', '.', regex=False),
            errors='coerce',
        )
    elif col == 'P04501':                                     # \"3 horas\" → extrai \"3\"
        direto    = pd.to_numeric(df_raw[col], errors='coerce')
        via_regex = df_raw[col].astype(str).str.extract(r'(\\d+\\.?\\d*)')[0]
        df_raw[col] = direto.fillna(pd.to_numeric(via_regex, errors='coerce'))
    else:
        df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce')

# ── Categóricas: normaliza strings vazias para NaN real ──────────────
for col in VARS_CATEGORICAS:
    if col in df_raw.columns:
        df_raw[col] = df_raw[col].astype(str).str.strip()
        df_raw[col] = df_raw[col].replace({'nan': np.nan, 'None': np.nan, '': np.nan})

# ── Diagnóstico rápido das numéricas ─────────────────────────────────
print('Resumo das numéricas (após conversão):')
print(df_raw[VARS_NUM].describe().T[['count','mean','std','min','max']].round(2))
"""
))

cells.append(md(
"""## 3 · Inventário das variáveis tratáveis

Esta etapa **lista explicitamente** quais variáveis entram em cada
estágio. O resumo evita ambiguidade na hora de defender a metodologia
no artigo."""
))

cells.append(code(
"""# Filtra apenas as numéricas que sobreviveram à conversão (alguns SQLite
# podem ter colunas faltantes em subgrupos com poucas instâncias)
VARS_CONT_OK = [v for v in VARS_CONTINUAS if v in df_raw.columns]
VARS_DISC_OK = [v for v in VARS_DISCRETAS if v in df_raw.columns]
VARS_NUM_OK  = VARS_CONT_OK + VARS_DISC_OK

# Monta tabela de inventário
inventario = []
for v in VARS_NUM_OK:
    inventario.append({
        'Variável'    : v,
        'Tipo'        : 'Contínua' if v in VARS_CONT_OK else 'Discreta',
        'n_válidos'   : int(df_raw[v].notna().sum()),
        '% Missing'   : round(100 * df_raw[v].isna().mean(), 2),
        'Mín'         : round(df_raw[v].min(), 2) if df_raw[v].notna().any() else None,
        'Máx'         : round(df_raw[v].max(), 2) if df_raw[v].notna().any() else None,
        'Estratégia'  : ('z-score+IQR' if v in VARS_CONT_OK and v != 'VDF004'
                         else ('média±2σ' if v == 'VDF004' else 'IQR somente')),
    })
tab_inventario = pd.DataFrame(inventario)
salvar_tab(tab_inventario, 'etapa3_inventario_variaveis.csv')
tab_inventario
"""
))

cells.append(md(
"""## 4 · Diagnóstico inicial — boxplots por classe (antes)

Visualiza a distribuição **antes** do tratamento. Esta é a foto que
vai para o artigo como “estado bruto” — útil para o revisor enxergar
a magnitude dos extremos."""
))

cells.append(code(
"""# Variáveis prioritárias para visualizar
VARS_VIZ = [v for v in ['P00104','P00404','C008','VDF004',
                        'P02501','P02002','P018','P00901']
            if v in df_raw.columns]
ROTULOS = {
    'P00104': 'Peso (kg)',        'P00404': 'Altura (cm)',
    'C008'  : 'Idade (anos)',     'VDF004': 'Renda per capita (quintil)',
    'P02501': 'Doces/ultraproc.', 'P02002': 'Refrigerante (dias/sem.)',
    'P018'  : 'Frutas (dias/sem.)','P00901': 'Verduras (dias/sem.)',
}

n_cols = 4
n_rows = math.ceil(len(VARS_VIZ) / n_cols)
fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols*4.5, n_rows*4))
axes = axes.flatten()

for i, col in enumerate(VARS_VIZ):
    ax = axes[i]
    sns.boxplot(
        data=df_raw, x='Classe', y=col, hue='Classe', ax=ax,
        palette={'Com Artrite': COR_ARTRITE, 'Saudável': COR_SAUDAVEL},
        order=['Saudável', 'Com Artrite'],
        width=0.5, linewidth=1.2,
        flierprops=dict(marker='o', markersize=2.5, alpha=0.5),
    )
    ax.set_title(ROTULOS.get(col, col), fontweight='bold')
    ax.set_xlabel(''); ax.set_ylabel('')
    if ax.get_legend(): ax.get_legend().remove()

for j in range(len(VARS_VIZ), len(axes)):
    axes[j].set_visible(False)

fig.suptitle('Etapa 4 — Distribuição ANTES do tratamento de outliers',
             fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
salvar_fig('etapa4_boxplots_antes.png')
plt.show()
"""
))

cells.append(md(
r"""## 5 · Estágio 1 — z-score > 4 (remoção de instâncias)

Critério inspirado em Silva & Zárate (2024). Calculamos o z-score
**por classe** para cada contínua e removemos linhas com valores
absurdos (|z| > 4). Esses são tipicamente erros de digitação:

- Idade = 250
- Peso = 7 kg
- Altura = 30 cm

Diferente do Estágio 2, aqui **removemos a instância inteira**, não
apenas o valor: um registro com erro grosseiro num campo provavelmente
tem outros campos comprometidos."""
))

cells.append(code(
"""df_step1 = df_raw.copy()                                       # cópia para trabalhar
mask_remover = pd.Series(False, index=df_step1.index)           # registros a remover
log_zscore   = []                                               # log linha por variável

for col in VARS_CONT_OK:                                         # SÓ contínuas (discretas têm escala limitada)
    n_removidos_var = 0
    for classe in df_step1['Classe'].unique():                  # por classe
        idx   = df_step1['Classe'] == classe                    # linhas dessa classe
        serie = df_step1.loc[idx, col]                          # valores
        if serie.notna().sum() < 10:                            # poucos dados → pula
            continue
        z = np.abs(stats.zscore(serie, nan_policy='omit'))      # |z| por valor
        z_full = pd.Series(np.nan, index=serie.index)           # série alinhada com NaN onde for missing
        z_full.loc[serie.notna()] = z
        out = (z_full > Z_LIMITE).fillna(False)                 # True onde |z|>4
        n_removidos_var += int(out.sum())
        mask_remover |= idx & out                               # acumula registros a remover

    log_zscore.append({
        'Variável'  : col,
        'Critério'  : f'|z| > {Z_LIMITE}',
        'n_removidos': n_removidos_var,
    })

n_antes = len(df_step1)
df_step1 = df_step1.loc[~mask_remover].copy()                   # remove de fato
n_depois = len(df_step1)

tab_zscore = pd.DataFrame(log_zscore)
salvar_tab(tab_zscore, 'etapa5_log_zscore.csv')

print(f'  Instâncias antes : {n_antes:,}')
print(f'  Instâncias depois: {n_depois:,}')
print(f'  Removidas        : {n_antes - n_depois:,} ({100*(n_antes-n_depois)/n_antes:.2f}%)')
print()
print('  Log por variável:')
print(tab_zscore.to_string(index=False))
"""
))

cells.append(md(
r"""## 6 · Estágio 2 — IQR × 1,5 por classe (substituição por NaN)

Método clássico de Tukey, adotado pelo LICAP em Melo et al. 2024 (DPOC)
e Cancella & Zárate 2025 (artrite-depressão).

Para cada variável numérica (contínua **ou** discreta), exceto
`VDF004` que tem tratamento específico no Estágio 3:

$$
\\text{Limites} = [Q_1 - 1{,}5 \\cdot \\text{IQR},\\; Q_3 + 1{,}5 \\cdot \\text{IQR}]
$$

Valores fora dos limites viram **NaN** e serão re-imputados na Etapa 8
pela média (numérica) ou moda (categórica) **da classe**, preservando
diferenças entre saudáveis e com artrite.

### Por que NaN em vez de remover a linha?

No Estágio 1, valores absurdos são erros de digitação → a linha inteira
é suspeita. No Estágio 2, “fora do IQR” inclui variação biológica
legítima (obesidade severa, baixa estatura) → preservar a linha e só
suavizar o valor é mais conservador metodologicamente."""
))

cells.append(code(
"""df_step2 = df_step1.copy()                              # parte do output do Estágio 1
log_iqr   = []                                           # log por variável

# Variáveis que recebem IQR: todas as numéricas EXCETO VDF004 (Estágio 3)
VARS_IQR = [v for v in VARS_NUM_OK if v != 'VDF004']

for col in VARS_IQR:
    mask_outlier = pd.Series(False, index=df_step2.index)  # máscara acumulada
    detalhes_classe = {}                                    # limites por classe (para log)

    for classe in df_step2['Classe'].unique():              # por classe
        idx   = df_step2['Classe'] == classe
        serie = df_step2.loc[idx, col].dropna()
        if len(serie) < 10:                                 # poucos dados → pula
            continue
        q1, q3 = serie.quantile(0.25), serie.quantile(0.75)
        iqr    = q3 - q1
        if iqr == 0:                                        # constante → sem outliers
            continue
        lim_inf = q1 - IQR_MULT * iqr
        lim_sup = q3 + IQR_MULT * iqr
        detalhes_classe[classe] = (round(lim_inf, 2), round(lim_sup, 2))
        # marca outliers (apenas dentro da classe)
        mask_outlier |= idx & ((df_step2[col] < lim_inf) | (df_step2[col] > lim_sup))

    n_out = int(mask_outlier.sum())
    if n_out > 0:
        df_step2.loc[mask_outlier, col] = np.nan            # substitui por NaN
        n_validos = int(df_step2[col].notna().sum() + n_out)
        pct = 100 * n_out / n_validos if n_validos else 0
        print(f'  {col:10s} {n_out:4d} outliers → NaN ({pct:5.2f}%)  '
              f'limites: {detalhes_classe}')

    log_iqr.append({
        'Variável'    : col,
        'n_outliers'  : n_out,
        '% outliers'  : round(100*n_out/max(1, int(df_step2[col].notna().sum() + n_out)), 2),
        'Limites_Saudavel'  : str(detalhes_classe.get('Saudável', '—')),
        'Limites_ComArtrite': str(detalhes_classe.get('Com Artrite', '—')),
    })

tab_iqr = pd.DataFrame(log_iqr)
salvar_tab(tab_iqr, 'etapa6_log_iqr.csv')
print(f'\\n  Total de outliers substituídos por NaN: {tab_iqr[\"n_outliers\"].sum():,}')
"""
))

cells.append(md(
r"""## 7 · Estágio 3 — Renda per capita: média ± 2σ

A variável `VDF004` (renda per capita em quintis) tem distribuição
fortemente assimétrica à direita, refletindo as desigualdades
socioeconômicas brasileiras. O método IQR seria ou excessivamente
permissivo (deixa rendas absurdas) ou cortaria parte legítima dos
quintis superiores.

Seguindo Cancella & Zárate (2025), aplicamos corte por
**média ± 2 desvios-padrão**, calculados **por classe**. Valores fora
desse intervalo viram NaN.

> Em quintis discretos (1–7), o efeito prático geralmente é remover só
> valores claramente fora da escala — útil principalmente se entrar
> uma versão monetária no futuro."""
))

cells.append(code(
"""df_step3 = df_step2.copy()
log_renda = []

if 'VDF004' in df_step3.columns:
    detalhes = {}
    mask_renda = pd.Series(False, index=df_step3.index)

    for classe in df_step3['Classe'].unique():
        idx   = df_step3['Classe'] == classe
        serie = df_step3.loc[idx, 'VDF004'].dropna()
        if len(serie) < 10:
            continue
        media = serie.mean()
        std   = serie.std()
        lim_inf = media - SIGMA_RENDA * std
        lim_sup = media + SIGMA_RENDA * std
        detalhes[classe] = {
            'média': round(media, 3),
            'std'  : round(std, 3),
            'lim_inf': round(lim_inf, 3),
            'lim_sup': round(lim_sup, 3),
        }
        mask_renda |= idx & ((df_step3['VDF004'] < lim_inf) | (df_step3['VDF004'] > lim_sup))

    n_out_renda = int(mask_renda.sum())
    if n_out_renda > 0:
        df_step3.loc[mask_renda, 'VDF004'] = np.nan
    log_renda.append({
        'Variável': 'VDF004',
        'Critério': f'média ± {SIGMA_RENDA}σ por classe',
        'n_outliers': n_out_renda,
        'detalhes': str(detalhes),
    })
    print(f'  VDF004 — {n_out_renda} outliers substituídos por NaN')
    for c, d in detalhes.items():
        print(f'    {c:12s}: média={d[\"média\"]} σ={d[\"std\"]}  → [{d[\"lim_inf\"]}, {d[\"lim_sup\"]}]')
else:
    print('  ⚠️  VDF004 ausente no DataFrame — Estágio 3 ignorado.')

tab_renda = pd.DataFrame(log_renda)
if not tab_renda.empty:
    salvar_tab(tab_renda, 'etapa7_log_renda.csv')
"""
))

cells.append(md(
"""## 8 · Re-imputação dos NaN gerados pelos Estágios 2 e 3

Os Estágios 2 e 3 transformam valores extremos em NaN, mas o
classificador não tolera NaN. Imputamos:

- **Numéricas** → média da classe correspondente.
- **Categóricas** → moda da classe correspondente.

Esta é a mesma estratégia já adotada no NB03, garantindo consistência
metodológica entre as etapas."""
))

cells.append(code(
"""df_step4 = df_step3.copy()
log_imp   = []

# Numéricas → média por classe
for col in VARS_NUM_OK:
    n_imputados = 0
    for classe in df_step4['Classe'].unique():
        idx = df_step4['Classe'] == classe
        sub = df_step4.loc[idx, col]
        if sub.notna().sum() == 0:                            # tudo NaN → não há média
            continue
        media_classe = sub.mean()
        nan_idx = idx & df_step4[col].isna()
        n_imputados += int(nan_idx.sum())
        df_step4.loc[nan_idx, col] = media_classe
    log_imp.append({
        'Variável'   : col,
        'Tipo'       : 'numérica',
        'Método'     : 'média por classe',
        'n_imputados': n_imputados,
    })

# Categóricas → moda por classe (Q079 é a variável-alvo; pulamos)
for col in [c for c in VARS_CATEGORICAS if c in df_step4.columns and c != 'Q079']:
    n_imputados = 0
    for classe in df_step4['Classe'].unique():
        idx = df_step4['Classe'] == classe
        sub = df_step4.loc[idx, col]
        if sub.notna().sum() == 0:
            continue
        moda = sub.mode(dropna=True)
        if moda.empty:
            continue
        nan_idx = idx & df_step4[col].isna()
        n_imputados += int(nan_idx.sum())
        df_step4.loc[nan_idx, col] = moda.iloc[0]
    log_imp.append({
        'Variável'   : col,
        'Tipo'       : 'categórica',
        'Método'     : 'moda por classe',
        'n_imputados': n_imputados,
    })

tab_imp = pd.DataFrame(log_imp)
salvar_tab(tab_imp, 'etapa8_log_imputacao.csv')

nan_residual = int(df_step4[VARS_NUM_OK].isna().sum().sum())
print(f'  Total imputado    : {tab_imp[\"n_imputados\"].sum():,}')
print(f'  NaN residual em X : {nan_residual} (esperado: 0)')
"""
))

cells.append(md(
"""## 9 · Sanidade — boxplots depois e comparação antes/depois

Painéis lado a lado: antes (cinza pálido) vs depois (cores cheias).
A caixa (Q1–Q3) deve manter a forma; só os pontos extremos somem."""
))

cells.append(code(
"""n_cols = 4
n_rows = math.ceil(len(VARS_VIZ) / n_cols)
fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols*4.5, n_rows*4))
axes = axes.flatten()

for i, col in enumerate(VARS_VIZ):
    ax = axes[i]
    df_a = df_raw[['Classe', col]].copy();  df_a['Etapa'] = 'Antes'
    df_d = df_step4[['Classe', col]].copy(); df_d['Etapa'] = 'Depois'
    df_plot = pd.concat([df_a, df_d], ignore_index=True)
    sns.boxplot(
        data=df_plot, x='Etapa', y=col, hue='Classe', ax=ax,
        palette={'Com Artrite': COR_ARTRITE, 'Saudável': COR_SAUDAVEL},
        order=['Antes', 'Depois'],
        width=0.5, linewidth=1.2,
        flierprops=dict(marker='o', markersize=2, alpha=0.4),
    )
    ax.set_title(ROTULOS.get(col, col), fontweight='bold')
    ax.set_xlabel(''); ax.set_ylabel('')
    if i > 0 and ax.get_legend(): ax.get_legend().remove()

for j in range(len(VARS_VIZ), len(axes)):
    axes[j].set_visible(False)

fig.suptitle('Etapa 9 — Comparação antes/depois do tratamento de outliers',
             fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
salvar_fig('etapa9_boxplots_antes_depois.png')
plt.show()
"""
))

cells.append(code(
"""# Comparação de estatísticas-resumo: antes vs depois
resumo = []
for col in VARS_NUM_OK:
    for classe in ['Saudável', 'Com Artrite']:
        antes  = df_raw.loc[df_raw['Classe'] == classe, col].dropna()
        depois = df_step4.loc[df_step4['Classe'] == classe, col].dropna()
        if antes.empty or depois.empty:
            continue
        resumo.append({
            'Variável'  : col,
            'Classe'    : classe,
            'n_antes'   : len(antes),
            'n_depois'  : len(depois),
            'média_antes' : round(antes.mean(), 2),
            'média_depois': round(depois.mean(), 2),
            'std_antes'   : round(antes.std(), 2),
            'std_depois'  : round(depois.std(), 2),
        })

tab_resumo = pd.DataFrame(resumo)
salvar_tab(tab_resumo, 'etapa9_comparacao_antes_depois.csv')
tab_resumo
"""
))

cells.append(md(
"""## 10 · Exportação e rastreabilidade

Salva o dataset limpo + relatório JSON com **todas** as decisões.
Este JSON alimenta diretamente a seção *Métodos* do artigo."""
))

cells.append(code(
"""# ── Dataset limpo (entrada para o NB05 de modelagem ML) ──────────────
caminho_csv = DIR_RESULTADOS + 'dataset_sem_outliers.csv'
df_step4.to_csv(caminho_csv, index=False, encoding='utf-8-sig')
print(f'  ✅ Dataset → {caminho_csv}')
print(f'     Dimensões: {df_step4.shape[0]:,} × {df_step4.shape[1]}')
print(f'     Distribuição da classe (Classe):')
print(df_step4['Classe'].value_counts().to_string())

# ── Relatório de rastreabilidade ─────────────────────────────────────
n_antes_total  = len(df_raw)
n_depois_total = len(df_step4)

relatorio = {
    'projeto'    : 'Artrite e Reumatismo em Idosos Brasileiros — PNS 2019',
    'pesquisador': 'Pedro Dias Soares',
    'orientador' : 'Prof. Dr. Luis Enrique Zárate — PUC Minas',
    'notebook'   : '04_eliminacao_outliers',
    'metodologia': 'Híbrido z-score + IQR + média±σ (Silva 2024 + Cancella 2025 + Melo 2024)',
    'parametros' : {
        'Z_LIMITE'   : Z_LIMITE,
        'IQR_MULT'   : IQR_MULT,
        'SIGMA_RENDA': SIGMA_RENDA,
        'RANDOM_STATE': RANDOM_STATE,
        'imputacao_numerica'  : 'média por classe',
        'imputacao_categorica': 'moda por classe',
    },
    'rastreabilidade': {
        'estagio_1_zscore': {
            'criterio'            : f'|z| > {Z_LIMITE} por classe',
            'instancias_removidas': int(n_antes_total - len(df_step1)),
            'detalhes'            : tab_zscore.to_dict('records'),
        },
        'estagio_2_iqr': {
            'criterio'            : f'IQR × {IQR_MULT} por classe → NaN',
            'total_outliers'      : int(tab_iqr['n_outliers'].sum()),
            'detalhes'            : tab_iqr.to_dict('records'),
        },
        'estagio_3_renda': {
            'criterio'            : f'média ± {SIGMA_RENDA}σ por classe',
            'detalhes'            : tab_renda.to_dict('records') if not tab_renda.empty else [],
        },
        'estagio_4_imputacao': {
            'total_imputados'     : int(tab_imp['n_imputados'].sum()),
            'detalhes'            : tab_imp.to_dict('records'),
        },
        'totais': {
            'n_antes'     : n_antes_total,
            'n_depois'    : n_depois_total,
            'perda_pct'   : round(100 * (n_antes_total - n_depois_total) / n_antes_total, 2),
            'distribuicao_final': df_step4['Classe'].value_counts().to_dict(),
        },
    },
}

caminho_json = DIR_RESULTADOS + 'relatorio_outliers.json'
with open(caminho_json, 'w', encoding='utf-8') as fp:
    json.dump(relatorio, fp, indent=2, ensure_ascii=False, default=str)
print(f'  ✅ Relatório → {caminho_json}')
"""
))

cells.append(code(
"""print('=' * 80)
print('  ✅  NOTEBOOK 04 — ELIMINAÇÃO DE OUTLIERS CONCLUÍDO')
print('=' * 80)
print(f'  Metodologia: z-score (|z|>{Z_LIMITE}) → IQR (×{IQR_MULT}) → Renda (±{SIGMA_RENDA}σ)')
print(f'  Tudo \"por classe\" (Saudável vs Com Artrite).')
print()
print('  RESULTADOS:')
print(f'  [Estágio 1] Instâncias removidas (z-score): {n_antes_total - len(df_step1):,}')
print(f'  [Estágio 2] Outliers substituídos (IQR)   : {int(tab_iqr[\"n_outliers\"].sum()):,}')
if not tab_renda.empty:
    print(f'  [Estágio 3] Renda (média±σ)               : {int(tab_renda[\"n_outliers\"].iloc[0]):,}')
print(f'  [Estágio 4] Valores imputados             : {int(tab_imp[\"n_imputados\"].sum()):,}')
print(f'  Dataset final: {df_step4.shape[0]:,} × {df_step4.shape[1]} (perda: {100*(n_antes_total-n_depois_total)/n_antes_total:.2f}%)')
print()
print('  ARTEFATOS GERADOS:')
print(f'  • {DIR_RESULTADOS}dataset_sem_outliers.csv')
print(f'  • {DIR_RESULTADOS}relatorio_outliers.json')
print(f'  • {DIR_FIGURAS}etapa4_boxplots_antes.png')
print(f'  • {DIR_FIGURAS}etapa9_boxplots_antes_depois.png')
print(f'  • {DIR_TABELAS}*.csv  (logs de cada estágio)')
print()
print('  Próximo → Notebook 05: modelagem ML (mover NB04 antigo para NB05)')
print('=' * 80)
"""
))


# ─────────────────────────────────────────────────────────────────────────────
# Envelope nbformat
# ─────────────────────────────────────────────────────────────────────────────

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.12",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

NB_PATH.parent.mkdir(parents=True, exist_ok=True)
NB_PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"Notebook escrito em: {NB_PATH}")
print(f"Total de células: {len(cells)}")
