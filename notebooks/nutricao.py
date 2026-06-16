"""Eixo nutricional do projeto PNS 2019 — IRNI, padrões alimentares (k-means) e
contagem de comorbidades para o Desenho 3 (NB03c).

Lógica centralizada (fonte única) para evitar duplicação entre o NB03c (base persistida,
descritiva) e o NB06 (in-fold, dentro da CV) — mesmo princípio que motivou mover mapas/skips
para o config.toml. Ver docs/spec_nutricao_desenho3.md.

Convenções:
- IRNI = soma(peso_item * z_item), z ajustado SÓ no treino (in-fold). + pró-inflamatório / − anti.
- Dois esquemas de peso (graded, direcao) lidos do config.toml [nutricao.irni.*].
- Cluster k-means rotulado de forma ORDINAL pelo escore pró-inflamatório do centróide
  (0 = mais protetor ... k-1 = mais pró-inflamatório), reaproveitando os pesos de direção.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

# As 13 comorbidades do estudo (as 14 doenças do Módulo Q menos a artrite-alvo Q079).
# Q084 (problema de coluna) NÃO entra: não é filtro de coorte e varia nos controles.
COMORBIDADES_13 = ['Q00201', 'Q03001', 'Q060', 'Q06306', 'Q068', 'Q074', 'Q088',
                   'Q092', 'Q11006', 'Q11604', 'Q120', 'Q124', 'Q128']


# ───────────────────────────── helpers de leitura ──────────────────────────────
def pesos_irni(cfg, esquema):
    """Retorna o dict item->peso do config.toml. esquema ∈ {'graded','direcao'}."""
    if esquema not in ('graded', 'direcao'):
        raise ValueError("esquema deve ser 'graded' ou 'direcao'")
    return dict(cfg['nutricao']['irni'][esquema])


def eh_sim(val):
    """True quando o valor representa 'Sim'/código 1 na PNS (texto OU numérico)."""
    if pd.isna(val):
        return False
    return str(val).strip().lower() in ('sim', '1', '1.0', 's')


# ──────────────────────────────────── IRNI ─────────────────────────────────────
def fit_zscore(df, itens):
    """Ajusta (média, desvio) por item — chamar SÓ no treino (in-fold).
    desvio 0 (item constante) vira 1.0 para não dividir por zero."""
    cols = [c for c in itens if c in df.columns]
    x = df[cols].apply(pd.to_numeric, errors='coerce')
    mu = x.mean()
    sd = x.std(ddof=0).replace(0, 1.0)
    return {'mu': mu, 'sd': sd, 'itens': cols}


def transform_irni(df, pesos, stats):
    """IRNI = soma(peso_i * z_i), usando z ajustado no treino (stats de fit_zscore).
    Itens de peso 0 (frango, leite) não contribuem. Itens ausentes são ignorados."""
    itens = [c for c in stats['itens'] if c in df.columns and pesos.get(c, 0) != 0]
    if not itens:
        return pd.Series(0.0, index=df.index)
    x = df[itens].apply(pd.to_numeric, errors='coerce')
    z = (x - stats['mu'][itens]) / stats['sd'][itens]
    w = pd.Series({c: float(pesos[c]) for c in itens})
    return z.mul(w, axis=1).sum(axis=1, min_count=1)


def calcular_irni_descritivo(df, pesos):
    """Conveniência para a base persistida (NB03c): ajusta o z-score na base inteira
    (alvo-cego) e calcula o IRNI. No NB06 use fit_zscore/transform_irni IN-FOLD."""
    stats = fit_zscore(df, list(pesos.keys()))
    return transform_irni(df, pesos, stats)


# ─────────────────────────── comorbidades (Desenho 3) ──────────────────────────
def contar_comorbidades(df, dieteticas, comorbidades=COMORBIDADES_13):
    """Retorna (n_total, n_naodieteticas, indicadores_df).
    dieteticas = comorbidades de manejo dietético a excluir da 2ª contagem
    (hipertensão/diabetes/colesterol/cardíaca)."""
    presentes = [c for c in comorbidades if c in df.columns]
    ind = pd.DataFrame({c: df[c].map(eh_sim) for c in presentes}, index=df.index)
    n_total = ind.sum(axis=1)
    nao_diet_cols = [c for c in presentes if c not in set(dieteticas)]
    n_naodiet = ind[nao_diet_cols].sum(axis=1) if nao_diet_cols else pd.Series(0, index=df.index)
    return n_total.astype(int), n_naodiet.astype(int), ind


def alvo_desenho3(df, comorbidades=COMORBIDADES_13):
    """Label do Desenho 3: 1 = tem >=1 comorbidade; 0 = artrite isolada."""
    n_total, _, _ = contar_comorbidades(df, dieteticas=[], comorbidades=comorbidades)
    return (n_total >= 1).astype(int)


# ─────────────────────────── cluster alimentar (k-means) ───────────────────────
def _escore_pro_centroides(centros_z, itens, pesos_direcao):
    """Para cada centróide (em espaço z), escore pró-inflamatório = soma(z * direção).
    Usa os pesos de DIREÇÃO (±1) para ordenar os clusters de protetor → pró."""
    w = np.array([float(pesos_direcao.get(c, 0)) for c in itens])
    return centros_z @ w


def escolher_k(Z, k_min, k_max, random_state):
    """Escolhe k por maior silhueta no intervalo [k_min, k_max]. Retorna (k, silhueta, tabela)."""
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    tabela = {}
    melhor = (None, -1.0)
    for k in range(k_min, k_max + 1):
        if k >= len(Z):
            continue
        labels = KMeans(n_clusters=k, random_state=random_state, n_init=10).fit_predict(Z)
        sil = silhouette_score(Z, labels)
        tabela[k] = round(float(sil), 4)
        if sil > melhor[1]:
            melhor = (k, sil)
    return melhor[0], melhor[1], tabela


def fit_cluster_alimentar(df_train, itens, pesos_direcao, k=None,
                          k_min=2, k_max=6, random_state=42):
    """Ajusta o k-means SÓ no treino. Retorna um modelo-dict com tudo p/ aplicar e rotular.
    Os clusters são reordenados de 0 (mais protetor) a k-1 (mais pró-inflamatório) pelo
    escore pró do centróide, tornando a feature ORDINAL e interpretável."""
    from sklearn.cluster import KMeans
    cols = [c for c in itens if c in df_train.columns]
    stats = fit_zscore(df_train, cols)
    Z = ((df_train[cols].apply(pd.to_numeric, errors='coerce') - stats['mu']) / stats['sd']).values
    sil_tab = {}
    if k is None:
        k, _sil, sil_tab = escolher_k(Z, k_min, k_max, random_state)
    km = KMeans(n_clusters=k, random_state=random_state, n_init=10).fit(Z)
    pro = _escore_pro_centroides(km.cluster_centers_, cols, pesos_direcao)
    # ordem crescente de pró → cluster id antigo recebe rótulo ordinal novo
    ordem = np.argsort(pro)                      # ids antigos do mais protetor ao mais pró
    remap = {int(old): novo for novo, old in enumerate(ordem)}
    return {'km': km, 'cols': cols, 'stats': stats, 'remap': remap,
            'k': k, 'silhueta': sil_tab, 'pro_centroides': pro}


def transform_cluster_alimentar(df, modelo):
    """Aplica o k-means treinado e devolve o rótulo ORDINAL (0..k-1) por linha."""
    cols, stats, km, remap = modelo['cols'], modelo['stats'], modelo['km'], modelo['remap']
    Z = ((df[cols].apply(pd.to_numeric, errors='coerce') - stats['mu']) / stats['sd']).values
    brutos = km.predict(Z)
    return pd.Series([remap[int(b)] for b in brutos], index=df.index, name='Cluster_Alimentar')


# ──────────────────────────────────── testes ───────────────────────────────────
def _autoteste():
    rng = np.random.default_rng(42)
    itens = ["P02501", "P02602", "P02002", "P02001", "P01101", "P006",
             "P013", "P018", "P00901", "P015", "P01601", "P023"]
    pro = ["P02501", "P02602", "P02002", "P02001", "P01101"]       # +
    anti = ["P018", "P00901", "P015", "P01601", "P006"]            # −
    n = 400
    base = pd.DataFrame({c: rng.integers(0, 8, n).astype(float) for c in itens})
    # cria dois perfis: metade come MUITO pró/pouco anti; metade o contrário
    grupo_pro = np.arange(n) < n // 2
    for c in pro:
        base.loc[grupo_pro, c] = rng.integers(5, 8, grupo_pro.sum())
        base.loc[~grupo_pro, c] = rng.integers(0, 3, (~grupo_pro).sum())
    for c in anti:
        base.loc[grupo_pro, c] = rng.integers(0, 3, grupo_pro.sum())
        base.loc[~grupo_pro, c] = rng.integers(5, 8, (~grupo_pro).sum())

    pesos_graded = {"P02501": 2, "P02602": 1, "P02002": 1, "P02001": 1, "P01101": 1,
                    "P006": -1, "P013": 0, "P018": -2, "P00901": -2, "P015": -2,
                    "P01601": -1, "P023": 0}
    pesos_dir = {k: (1 if v > 0 else -1 if v < 0 else 0) for k, v in pesos_graded.items()}

    # (1) IRNI: grupo pró deve ter IRNI MAIOR que grupo anti, nos dois esquemas
    for nome, pesos in [("graded", pesos_graded), ("direcao", pesos_dir)]:
        irni = calcular_irni_descritivo(base, pesos)
        m_pro, m_anti = irni[grupo_pro].mean(), irni[~grupo_pro].mean()
        assert m_pro > m_anti, f"IRNI {nome}: pró deveria > anti ({m_pro:.2f} vs {m_anti:.2f})"
        print(f"  [IRNI {nome}] média pró={m_pro:+.2f} > anti={m_anti:+.2f}  ✓  (peso 0 não contribui)")

    # (1b) in-fold: z ajustado no treino e aplicado ao teste (sem refit)
    tr, te = base.iloc[:300], base.iloc[300:]
    stats = fit_zscore(tr, list(pesos_graded))
    irni_te = transform_irni(te, pesos_graded, stats)
    assert irni_te.notna().all() and len(irni_te) == 100
    print("  [IRNI in-fold] z do treino aplicado ao teste: 100 valores, sem NaN  ✓")

    # (2) comorbidades: monta Q* sintético e confere total vs não-dietética
    dq = pd.DataFrame({c: rng.choice(['Sim', 'Não'], n) for c in COMORBIDADES_13})
    dieteticas = ["Q00201", "Q03001", "Q060", "Q06306"]
    n_tot, n_nd, ind = contar_comorbidades(dq, dieteticas)
    esperado_nd = ind.drop(columns=dieteticas).sum(axis=1)
    assert (n_nd == esperado_nd).all() and (n_tot >= n_nd).all()
    assert (n_tot == ind.sum(axis=1)).all()
    print(f"  [comorbidades] total e não-dietética coerentes (média total={n_tot.mean():.1f}, "
          f"não-diet={n_nd.mean():.1f})  ✓")
    # alvo D3
    y = alvo_desenho3(dq)
    assert set(y.unique()) <= {0, 1}
    print(f"  [alvo D3] 1=tem comorbidade: {int(y.sum())}/{len(y)}  ✓")

    # (3) cluster: deve achar k=2 e separar pró × anti; rótulo ordinal cresce com 'pró'
    modelo = fit_cluster_alimentar(base, itens, pesos_dir, k_min=2, k_max=5, random_state=42)
    lab = transform_cluster_alimentar(base, modelo)
    # o grupo pró deve cair majoritariamente no maior rótulo ordinal
    rot_pro = lab[grupo_pro].mode().iloc[0]
    rot_anti = lab[~grupo_pro].mode().iloc[0]
    assert rot_pro > rot_anti, f"cluster: rótulo do grupo pró ({rot_pro}) deveria > anti ({rot_anti})"
    print(f"  [cluster] k={modelo['k']} silhueta={modelo['silhueta']} | rótulo pró={rot_pro} > anti={rot_anti}  ✓")
    print("\n✅ Todos os autotestes passaram.")


if __name__ == '__main__':
    _autoteste()
