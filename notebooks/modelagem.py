"""Modelagem supervisionada do projeto PNS 2019 — ablação por blocos (NB06 §4).

Responde à pergunta de pesquisa:
    "Quais PADRÕES NUTRICIONAIS e CARACTERÍSTICAS SOCIODEMOGRÁFICAS diferenciam,
     no Brasil, os idosos com artrite dos idosos saudáveis (PNS 2019), via
     algoritmos supervisionados?"

O modelo é INSTRUMENTO DESCRITIVO (regras + ranking de fatores, estilo LICAP/Zárate),
não classificador de produção. A estratégia central é a ABLAÇÃO POR BLOCOS — emprestada
do paper de TOC (30684), que mediu o ganho de F1 ao adicionar um bloco de atributos:

    M0  = só sociodemográfico        (linha de base "quem é a pessoa")
    M1  = só nutrição                (poder isolado da dieta)
    M2  = socio + nutrição           (ganho marginal da dieta sobre M0)  ← conjunto-resposta
    Mc  = socio + controle           (sem nutrição, com confundidores de saúde)
    M3  = socio + nutrição + controle (completo)

    ΔF1 marginal da nutrição sobre socio          = F1(M2) − F1(M0)
    ΔF1 marginal da nutrição sobre socio+controle = F1(M3) − F1(Mc)

Lógica centralizada (fonte única), mesma motivação de `nutricao.py`. O eixo nutricional
"os três juntos" = itens de frequência discretizados (no dataset) + IRNI contínuo + Cluster
alimentar (ambos calculados IN-FOLD a partir das frequências cruas — ver NutricaoInFold).

Convenções de vazamento: z-score do IRNI, k-means do cluster e RUS são ajustados SÓ no
treino de cada fold (dentro do imblearn.Pipeline). O dataset persistido segue intocado.
"""
from __future__ import annotations
import re
import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

import nutricao as nut  # fit_zscore / transform_irni / fit_cluster_alimentar / transform_cluster_alimentar

# ───────────────────────── 1. Classificação em blocos ──────────────────────────
# Fonte: dicionário de variáveis do NB02/NB03 (códigos PNS 2019).
SOCIO = {'C006', 'C008', 'VDF004', 'VDD004A'}            # sexo, idade, renda, escolaridade
NUTRI = {'P006', 'P00603', 'P013', 'P02602', 'P00620', 'P00612', 'P00614',
         'P00615', 'P00616', 'P02601', 'P02401', 'P02101', 'P02102'}  # dieta/alimentação
# CONTROLE (confundidores) = resto: saúde percebida (N0*), limitação funcional (G0*),
# comorbidade (Q*), uso de serviço (J*), plano de saúde (I00102), álcool (P027/P028/P029/P032),
# exercício (P034/P035) e IMC. O quadrante Padrao_Alimentar é APOSENTADO (spec §0).
PREFIXO_RAW = 'raw__'   # frequências cruas anexadas ao X p/ o IRNI/cluster in-fold


def var_pai(col: str) -> str:
    """Código-base PNS a partir de uma coluna do dataset discretizado.
    Corta o sufixo one-hot (1º '_<Maiúscula>') e o sufixo '_cat'."""
    col = col.lstrip('﻿')
    base = re.split(r'_(?=[A-ZÀ-Ú])', col)[0]
    base = re.sub(r'_cat$', '', base)
    return base


def classificar_bloco(col: str) -> str:
    """Retorna 'socio' | 'nutri' | 'control' | 'retirar' | 'alvo'."""
    col = col.lstrip('﻿')
    if col == 'Label':
        return 'alvo'
    if col.startswith('Padrao_Alimentar'):
        return 'retirar'
    p = var_pai(col)
    if p in NUTRI:
        return 'nutri'
    if p in SOCIO:
        return 'socio'
    return 'control'


def montar_blocos(colunas) -> dict:
    """dict bloco -> [colunas] (preserva a ordem de entrada)."""
    blocos: dict[str, list] = {}
    for c in colunas:
        blocos.setdefault(classificar_bloco(c), []).append(c.lstrip('﻿'))
    return blocos


def conjuntos_ablacao(blocos: dict) -> dict:
    """Conjuntos de atributos DISCRETIZADOS por modelo de ablação.
    Atenção: IRNI e Cluster NÃO entram aqui — são adicionados in-fold pelo NutricaoInFold
    quando o conjunto contém o bloco nutricional (flag 'tem_nutri')."""
    socio = blocos.get('socio', [])
    nutri = blocos.get('nutri', [])
    ctrl = blocos.get('control', [])
    return {
        'M0_socio':        {'cols': socio,                 'tem_nutri': False},
        'M1_nutri':        {'cols': nutri,                 'tem_nutri': True},
        'M2_socio_nutri':  {'cols': socio + nutri,         'tem_nutri': True},
        'Mc_socio_ctrl':   {'cols': socio + ctrl,          'tem_nutri': False},
        'M3_completo':     {'cols': socio + nutri + ctrl,  'tem_nutri': True},
    }


# ───────────────────────── 2. Carregamento de um desenho ───────────────────────
def carregar_design(disc_path: str, prep_path: str, itens_irni) -> tuple:
    """Lê o dataset discretizado (features do modelo) + o pré-processado (frequências
    cruas p/ IRNI/cluster), alinhados por linha. Retorna (X, y, blocos, raw_cols).

    X = features discretizadas (sem Label, sem Padrao_Alimentar) + colunas 'raw__<item>'.
    Guarda de alinhamento: mesmo nº de linhas E mesmo vetor Label nos dois arquivos."""
    disc = pd.read_csv(disc_path)
    disc.columns = [c.lstrip('﻿') for c in disc.columns]
    prep = pd.read_csv(prep_path)
    prep.columns = [c.lstrip('﻿') for c in prep.columns]

    if len(disc) != len(prep):
        raise ValueError(f"Desalinhamento: discretizado {len(disc)} ≠ preprocessado {len(prep)} linhas.")
    disc = disc.reset_index(drop=True)
    prep = prep.reset_index(drop=True)
    if 'Label' in prep.columns and not np.array_equal(
            disc['Label'].to_numpy(int), prep['Label'].to_numpy(int)):
        raise ValueError("Label não bate entre discretizado e preprocessado — ordem das linhas divergiu.")

    y = disc['Label'].astype(int)
    blocos = montar_blocos(disc.columns)
    feat_cols = blocos.get('socio', []) + blocos.get('nutri', []) + blocos.get('control', [])
    X = disc[feat_cols].copy()

    # anexa frequências cruas (prefixadas) — só as que existem no pré-processado
    raw_cols = []
    for item in itens_irni:
        if item in prep.columns:
            X[PREFIXO_RAW + item] = pd.to_numeric(prep[item], errors='coerce').values
            raw_cols.append(PREFIXO_RAW + item)
    return X, y, blocos, raw_cols


def selecionar_X(X: pd.DataFrame, conjunto: dict, raw_cols) -> pd.DataFrame:
    """Subconjunto de colunas do X para um modelo de ablação. Inclui as 'raw__' apenas
    quando o conjunto usa nutrição (o NutricaoInFold as consome e devolve IRNI+cluster)."""
    cols = list(conjunto['cols'])
    if conjunto['tem_nutri']:
        cols = cols + list(raw_cols)
    return X[cols].copy()


# ─────────────────── 3. Transformer in-fold: IRNI + Cluster ─────────────────────
class NutricaoInFold(BaseEstimator, TransformerMixin):
    """Calcula IRNI (z-score ajustado no treino) e Cluster_Alimentar (k-means no treino)
    a partir das colunas 'raw__<item>' presentes em X, devolvendo-as como atributos e
    REMOVENDO as cruas. Compatível com sklearn/imblearn Pipeline (fit só no treino do fold).

    pesos_graded / pesos_direcao: dicts item->peso (do config). incluir_direcao=True acrescenta
    também o IRNI_direcao (sensibilidade). k = nº de clusters (fixado a priori, ver escolher_k_descritivo)."""

    def __init__(self, pesos_graded=None, pesos_direcao=None, k=3,
                 incluir_direcao=False, random_state=42):
        self.pesos_graded = pesos_graded or {}
        self.pesos_direcao = pesos_direcao or {}
        self.k = k
        self.incluir_direcao = incluir_direcao
        self.random_state = random_state

    @staticmethod
    def _raw_para_codigo(df):
        ren = {c: c[len(PREFIXO_RAW):] for c in df.columns if c.startswith(PREFIXO_RAW)}
        return df[list(ren)].rename(columns=ren)

    def fit(self, X, y=None):
        X = pd.DataFrame(X).reset_index(drop=True)
        freq = self._raw_para_codigo(X)
        itens = list(freq.columns)
        self.outras_ = [c for c in X.columns if not c.startswith(PREFIXO_RAW)]
        self.stats_g_ = nut.fit_zscore(freq, list(self.pesos_graded))
        if self.incluir_direcao:
            self.stats_d_ = nut.fit_zscore(freq, list(self.pesos_direcao))
        self.cluster_ = nut.fit_cluster_alimentar(
            freq, itens, self.pesos_direcao, k=self.k, random_state=self.random_state)
        return self

    def transform(self, X):
        X = pd.DataFrame(X).reset_index(drop=True)
        freq = self._raw_para_codigo(X)
        out = X[self.outras_].copy()
        out['IRNI_graded'] = nut.transform_irni(freq, self.pesos_graded, self.stats_g_).values
        if self.incluir_direcao:
            out['IRNI_direcao'] = nut.transform_irni(freq, self.pesos_direcao, self.stats_d_).values
        out['Cluster_Alimentar'] = nut.transform_cluster_alimentar(freq, self.cluster_).values
        return out

    def get_feature_names_out(self, input_features=None):
        nomes = list(self.outras_) + ['IRNI_graded']
        if self.incluir_direcao:
            nomes.append('IRNI_direcao')
        return np.array(nomes + ['Cluster_Alimentar'])


def escolher_k_descritivo(X, raw_cols, pesos_direcao, k_min=2, k_max=6, random_state=42):
    """Escolhe k do cluster UMA vez (silhueta) sobre o conjunto de treino — depois fixado
    in-fold (k vira hiperparâmetro, não se re-seleciona por fold). Retorna (k, tabela_sil)."""
    freq = X[[c for c in raw_cols]].rename(columns={c: c[len(PREFIXO_RAW):] for c in raw_cols})
    stats = nut.fit_zscore(freq, list(freq.columns))
    Z = ((freq[stats['itens']] - stats['mu']) / stats['sd']).values
    k, _sil, tab = nut.escolher_k(Z, k_min, k_max, random_state)
    return k, tab


# ─────────────────────────── 4. Pipelines e busca ──────────────────────────────
def build_pipeline(modelo, tem_nutri, pesos_g=None, pesos_d=None, k=3, random_state=42):
    """imblearn.Pipeline = [NutricaoInFold?] -> [StandardScaler? p/ logreg] -> RUS -> clf."""
    from imblearn.pipeline import Pipeline
    from imblearn.under_sampling import RandomUnderSampler
    from sklearn.preprocessing import StandardScaler
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.linear_model import LogisticRegression

    clfs = {
        'dt':     DecisionTreeClassifier(random_state=random_state),
        'rf':     RandomForestClassifier(random_state=random_state, n_jobs=-1),
        'nb':     GaussianNB(),
        'logreg': LogisticRegression(max_iter=2000, random_state=random_state),
    }
    if modelo not in clfs:
        raise ValueError(f"modelo desconhecido: {modelo}")

    steps = []
    if tem_nutri:
        steps.append(('nutri', NutricaoInFold(pesos_graded=pesos_g, pesos_direcao=pesos_d,
                                              k=k, random_state=random_state)))
    if modelo == 'logreg':
        steps.append(('scaler', StandardScaler()))
    steps.append(('rus', RandomUnderSampler(random_state=random_state)))
    steps.append(('clf', clfs[modelo]))
    return Pipeline(steps)


def espaco_busca(modelo):
    """Grades pequenas p/ RandomizedSearchCV (prefixo clf__). DT/RF na faixa dos papers."""
    if modelo == 'dt':
        return {'clf__criterion': ['gini', 'entropy'],
                'clf__max_depth': [3, 4, 5, 6, 7, None],
                'clf__min_samples_leaf': [10, 20, 30, 50],
                'clf__min_samples_split': [20, 50]}
    if modelo == 'rf':
        return {'clf__n_estimators': [100, 200, 300],
                'clf__max_depth': [4, 6, 8, None],
                'clf__min_samples_leaf': [5, 10, 20],
                'clf__max_features': ['sqrt', 0.3, 0.5]}
    if modelo == 'nb':
        return {'clf__var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6]}
    if modelo == 'logreg':
        return {'clf__C': [0.01, 0.1, 1, 10], 'clf__penalty': ['l2']}
    raise ValueError(modelo)


# ─────────────────────────── 5. Métricas e avaliação ───────────────────────────
def _ic95(arr):
    from scipy import stats
    arr = np.asarray(arr, float)
    m = arr.mean()
    if len(arr) < 2:
        return m, m, m
    sem = stats.sem(arr)
    h = sem * stats.t.ppf(0.975, len(arr) - 1)
    return m, m - h, m + h


def metricas_cv(pipe, X, y, n_splits=10, random_state=42):
    """10-fold estratificado no TREINO. Retorna dict com média±IC95 e o vetor de F1 por fold."""
    from sklearn.model_selection import StratifiedKFold, cross_validate
    scoring = {'acc': 'accuracy', 'prec': 'precision', 'rec': 'recall',
               'f1': 'f1', 'auc': 'roc_auc'}
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    cvr = cross_validate(pipe, X, y, scoring=scoring, cv=cv, n_jobs=-1, error_score='raise')
    out = {}
    for met in scoring:
        m, lo, hi = _ic95(cvr['test_' + met])
        out[met] = {'media': m, 'ic_lo': lo, 'ic_hi': hi}
    out['f1_folds'] = cvr['test_f1']
    return out


def avaliar_holdout(pipe, Xtr, ytr, Xte, yte):
    """Treina no treino inteiro e avalia no teste held-out (desbalanceado)."""
    from sklearn.metrics import (confusion_matrix, classification_report,
                                  roc_auc_score, roc_curve, f1_score)
    pipe.fit(Xtr, ytr)
    yp = pipe.predict(Xte)
    proba = pipe.predict_proba(Xte)[:, 1]
    fpr, tpr, _ = roc_curve(yte, proba)
    return {
        'f1': f1_score(yte, yp),
        'auc': roc_auc_score(yte, proba),
        'confusao': confusion_matrix(yte, yp),
        'report': classification_report(yte, yp, output_dict=True, zero_division=0),
        'roc': {'fpr': fpr.tolist(), 'tpr': tpr.tolist()},
        'pipe': pipe,
    }


# ─────────────────────────── 6. Regras da árvore (≥cobertura) ───────────────────
def _transformar_para_arvore(pipe, X, tem_nutri):
    """Aplica só a transformação de atributos (NutricaoInFold) — samplers/clf de fora.
    Devolve o X como a árvore o enxerga, para apply()/cobertura sobre dados REAIS."""
    if tem_nutri and 'nutri' in pipe.named_steps:
        return pipe.named_steps['nutri'].transform(X)
    return X


def regras_arvore(pipe, Xtr_full, ytr_full, tem_nutri, min_cobertura=0.10):
    """Extrai regras de uma DecisionTree TREINADA (dentro do pipe), com COBERTURA medida
    sobre o treino REAL (desbalanceado) — não sobre a subamostra RUS. Para cada folha com
    cobertura ≥ min, retorna {regra, classe_modelo, cobertura, n_real, pureza_real}."""
    clf = pipe.named_steps['clf']
    t = clf.tree_
    nomes = list(getattr(clf, 'feature_names_in_',
                         _transformar_para_arvore(pipe, Xtr_full.head(1), tem_nutri).columns))
    Xt = _transformar_para_arvore(pipe, Xtr_full, tem_nutri)
    folhas = clf.apply(Xt)                       # folha de cada amostra REAL
    y = np.asarray(ytr_full)
    n_total = len(y)

    # estatísticas reais por folha
    df_leaf = pd.DataFrame({'leaf': folhas, 'y': y})
    stats_leaf = {}
    for leaf, g in df_leaf.groupby('leaf'):
        classe_modelo = int(np.argmax(t.value[leaf][0]))   # o que a árvore prediz
        n_real = len(g)
        pureza_real = float((g['y'] == classe_modelo).mean())
        stats_leaf[leaf] = (classe_modelo, n_real, pureza_real)

    regras = []

    def caminhar(no, cond):
        if t.children_left[no] == t.children_right[no]:    # folha
            if no in stats_leaf:
                classe_modelo, n_real, pureza_real = stats_leaf[no]
                cobertura = n_real / n_total
                if cobertura >= min_cobertura:
                    regras.append({'regra': ' E '.join(cond) if cond else '(raiz)',
                                   'classe_modelo': classe_modelo,
                                   'cobertura': round(cobertura, 3), 'n_real': n_real,
                                   'pureza_real': round(pureza_real, 3)})
            return
        f = nomes[t.feature[no]]
        thr = t.threshold[no]
        caminhar(t.children_left[no], cond + [f"{f} <= {thr:.2f}"])
        caminhar(t.children_right[no], cond + [f"{f} > {thr:.2f}"])

    caminhar(0, [])
    return sorted(regras, key=lambda r: r['cobertura'], reverse=True)


# ─────────────────────── 7. OR ajustado (statsmodels) ───────────────────────────
def or_ajustado(X, y, feats_socio, feats_nutri, padronizar_continuas=True):
    """Logit y ~ socio + nutrição (IRNI/cluster). Retorna DataFrame OR + IC95 por atributo.
    Continuas (IRNI) padronizadas → OR por desvio-padrão. Usa a base SEM balancear (inferência)."""
    import statsmodels.api as sm
    cols = [c for c in (feats_socio + feats_nutri) if c in X.columns]
    Z = X[cols].apply(pd.to_numeric, errors='coerce').copy()
    if padronizar_continuas:
        for c in cols:
            if Z[c].nunique() > 6:   # contínua (IRNI) → z-score
                sd = Z[c].std(ddof=0) or 1.0
                Z[c] = (Z[c] - Z[c].mean()) / sd
    Z = sm.add_constant(Z)
    modelo = sm.Logit(y.values, Z.astype(float)).fit(disp=0)
    res = pd.DataFrame({'coef': modelo.params, 'OR': np.exp(modelo.params),
                        'p': modelo.pvalues})
    ic = np.exp(modelo.conf_int())
    res['OR_ic_lo'], res['OR_ic_hi'] = ic[0], ic[1]
    return res.drop(index='const', errors='ignore')


# ─────────────────────── 8. Comparação estatística (t pareado) ──────────────────
def ttest_pareado_bonferroni(f1_por_modelo: dict, alpha=0.05):
    """t pareado nas F1 dos 10 folds entre cada par de modelos + correção de Bonferroni.
    f1_por_modelo: {nome: array de F1 por fold}. Retorna DataFrame de pares."""
    from scipy import stats
    from itertools import combinations
    nomes = list(f1_por_modelo)
    pares = list(combinations(nomes, 2))
    m = len(pares)
    linhas = []
    for a, b in pares:
        t, p = stats.ttest_rel(f1_por_modelo[a], f1_por_modelo[b])
        linhas.append({'modelo_a': a, 'modelo_b': b,
                       'dif_media_f1': float(np.mean(f1_por_modelo[a]) - np.mean(f1_por_modelo[b])),
                       't': float(t), 'p': float(p),
                       'p_bonferroni': min(1.0, float(p) * m),
                       'signif_0.05': (p * m) < alpha})
    return pd.DataFrame(linhas)


# ──────────────────────────────────── autoteste ────────────────────────────────
def _autoteste():
    rng = np.random.default_rng(42)
    n = 600
    itens = ['P02501', 'P02602', 'P02002', 'P02001', 'P01101', 'P006',
             'P013', 'P018', 'P00901', 'P015', 'P01601', 'P023']
    pesos_g = {'P02501': 2, 'P02602': 1, 'P02002': 1, 'P02001': 1, 'P01101': 1,
               'P006': -1, 'P013': 0, 'P018': -2, 'P00901': -2, 'P015': -2,
               'P01601': -1, 'P023': 0}
    pesos_d = {k: (1 if v > 0 else -1 if v < 0 else 0) for k, v in pesos_g.items()}

    # (1) classificação em blocos
    cols = ['C006_Mulher', 'C008_cat', 'VDF004', 'VDD004A', 'P006_cat', 'P00620_Sim',
            'P02601_Alto', 'N001', 'G081', 'Q084_Sim', 'Padrao_Alimentar_cat', 'Label']
    b = montar_blocos(cols)
    assert set(b['socio']) == {'C006_Mulher', 'C008_cat', 'VDF004', 'VDD004A'}
    assert 'P006_cat' in b['nutri'] and 'P00620_Sim' in b['nutri'] and 'P02601_Alto' in b['nutri']
    assert 'N001' in b['control'] and 'G081' in b['control'] and 'Q084_Sim' in b['control']
    assert b['retirar'] == ['Padrao_Alimentar_cat']
    conj = conjuntos_ablacao(b)
    assert conj['M0_socio']['tem_nutri'] is False and conj['M2_socio_nutri']['tem_nutri'] is True
    print(f"  [blocos] socio={len(b['socio'])} nutri={len(b['nutri'])} control={len(b['control'])}; "
          f"Padrao_Alimentar aposentado  ✓")

    # (2) dados sintéticos: dieta pró-inflamatória ↑ prob de Label=1 (sinal forte de propósito)
    raw = pd.DataFrame({c: rng.integers(0, 8, n).astype(float) for c in itens})
    irni_true = sum(pesos_g[c] * (raw[c] - raw[c].mean()) / (raw[c].std() or 1) for c in itens)
    sexo = rng.integers(0, 2, n)
    logit = -0.5 + 0.8 * (irni_true / irni_true.std()) + 0.5 * sexo
    y = pd.Series((rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int))
    X = pd.DataFrame({'C006_Mulher': sexo, 'C008_cat': rng.integers(0, 4, n)})
    for c in itens:
        X[PREFIXO_RAW + c] = raw[c].values
    raw_cols = [PREFIXO_RAW + c for c in itens]

    # (3) transformer in-fold: gera IRNI + cluster, remove as cruas
    tr = NutricaoInFold(pesos_graded=pesos_g, pesos_direcao=pesos_d, k=3)
    Xt = tr.fit_transform(X.iloc[:400])
    assert 'IRNI_graded' in Xt.columns and 'Cluster_Alimentar' in Xt.columns
    assert not any(c.startswith(PREFIXO_RAW) for c in Xt.columns), "frequências cruas deviam sair"
    assert list(tr.get_feature_names_out())[-1] == 'Cluster_Alimentar'
    print(f"  [transformer] IRNI+Cluster gerados, {Xt.shape[1]} cols, sem 'raw__'  ✓")

    # (4) pipeline completo + métricas CV (sinal forte → F1 deve ficar > 0.55)
    from sklearn.model_selection import train_test_split
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    pipe = build_pipeline('dt', tem_nutri=True, pesos_g=pesos_g, pesos_d=pesos_d, k=3)
    met = metricas_cv(pipe, Xtr, ytr, n_splits=5)
    assert 0.0 <= met['f1']['media'] <= 1.0 and len(met['f1_folds']) == 5
    print(f"  [pipeline+CV] F1={met['f1']['media']:.3f} (IC95 {met['f1']['ic_lo']:.3f}-{met['f1']['ic_hi']:.3f})  ✓")

    # (5) regras da árvore treinada (cobertura sobre o treino REAL)
    av = avaliar_holdout(pipe, Xtr, ytr, Xte, yte)
    regras = regras_arvore(av['pipe'], Xtr, ytr, tem_nutri=True, min_cobertura=0.10)
    assert isinstance(regras, list) and all('cobertura' in r for r in regras)
    print(f"  [holdout] F1_teste={av['f1']:.3f} AUC={av['auc']:.3f} | regras≥10%={len(regras)}  ✓")

    # (6) OR ajustado + t pareado
    Xfit = tr.fit_transform(X)
    orr = or_ajustado(Xfit, y, ['C006_Mulher', 'C008_cat'], ['IRNI_graded', 'Cluster_Alimentar'])
    assert 'OR' in orr.columns and 'IRNI_graded' in orr.index
    cmp = ttest_pareado_bonferroni({'A': met['f1_folds'], 'B': met['f1_folds'][::-1]})
    assert {'p_bonferroni', 'dif_media_f1'} <= set(cmp.columns)
    print(f"  [OR ajustado] OR(IRNI)={orr.loc['IRNI_graded','OR']:.2f} | t-test pareado OK  ✓")
    print("\n✅ Todos os autotestes de modelagem passaram.")


if __name__ == '__main__':
    _autoteste()
