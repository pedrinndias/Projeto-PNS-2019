# -*- coding: utf-8 -*-
"""Gera o fluxograma do pipeline KDD (10 etapas) para o artigo.

Uso (da raiz do projeto):  python scripts/build_fluxograma_pipeline.py
Gera: Documentos_organizacao/figuras_artigo/fluxograma_pipeline_kdd.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "Documentos_organizacao" / "figuras_artigo"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "fluxograma_pipeline_kdd.png"

# ── Etapas: (numero, titulo, descricao curta, fase) ──────────────────────
ETAPAS = [
    (1,  "Entendimento do Problema",
         "Definição do escopo e da pergunta de pesquisa (PICOS)", "A"),
    (2,  "Modelagem Conceitual (CAPTO)",
         "Entendimento do domínio e construção do mapa conceitual", "A"),
    (3,  "Seleção Conceitual de Atributos",
         "Escolha das variáveis da PNS 2019 a partir do mapa conceitual", "A"),
    (4,  "Tratamento de Dados Ausentes",
         "Resolução de skip patterns e auditoria de missing real", "B"),
    (5,  "Análise e Remoção de Outliers",
         "Método IQR × 3,0 calculado por classe", "B"),
    (6,  "Preparação dos Dados",
         "Fusão de atributos (IMC, escores) e discretização ordinal", "B"),
    (7,  "Seleção de Atributos",
         "Filtragem por entropia / wrappers", "C"),
    (8,  "Balanceamento das Classes",
         "Random Under Sampler aplicado ao conjunto de treino", "C"),
    (9,  "Modelos e Parametrização",
         "Decision Tree, Naive Bayes, Random Forest, AdaBoost", "D"),
    (10, "Treinamento e Teste",
         "Validação cruzada 10-fold e avaliação no conjunto de teste", "D"),
]

# ── Fases: cor sólida, cor de preenchimento clara, rótulo ────────────────
FASES = {
    "A": ("#1F3764", "#E8EDF6", "FASE 1\nEntendimento\ndo Problema\ne do Domínio"),
    "B": ("#2E75B6", "#E4EFF8", "FASE 2\nPré-\nProcessamento\ndos Dados"),
    "C": ("#1E7A34", "#E4F3E8", "FASE 3\nPreparação\npara a\nMineração"),
    "D": ("#B75E09", "#FBEEDD", "FASE 4\nModelagem\ne Avaliação"),
}

# ── Layout ───────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8.2, 13.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 13.6)
ax.axis("off")

BOX_X = 3.0          # borda esquerda das caixas de etapa
BOX_W = 6.4          # largura das caixas
BOX_H = 0.86         # altura das caixas
GAP   = 0.33         # espaço vertical entre caixas
TOP_Y = 12.30        # topo da primeira caixa

# Título da figura
ax.text(5.0, 13.20, "Processo de Descoberta de Conhecimento (KDD)",
        ha="center", va="center", fontsize=14, fontweight="bold", color="#1F3764")
ax.text(5.0, 12.82, "Pipeline metodológico em 10 etapas — Artrite e Reumatismo · PNS 2019",
        ha="center", va="center", fontsize=9.5, color="#595959", style="italic")

centros_y = []
for i, (num, titulo, desc, fase) in enumerate(ETAPAS):
    cor_solida, cor_fill, _ = FASES[fase]
    top = TOP_Y - i * (BOX_H + GAP)
    cy = top - BOX_H / 2
    centros_y.append((cy, fase))

    # Caixa da etapa
    caixa = FancyBboxPatch(
        (BOX_X, top - BOX_H), BOX_W, BOX_H,
        boxstyle="round,pad=0.02,rounding_size=0.10",
        linewidth=1.6, edgecolor=cor_solida, facecolor=cor_fill, zorder=2,
    )
    ax.add_patch(caixa)

    # Badge numérico (círculo)
    badge_cx = BOX_X + 0.52
    circ = plt.Circle((badge_cx, cy), 0.30, color=cor_solida, zorder=3)
    ax.add_patch(circ)
    ax.text(badge_cx, cy, str(num), ha="center", va="center",
            fontsize=12, fontweight="bold", color="white", zorder=4)

    # Título e descrição
    txt_x = BOX_X + 1.05
    ax.text(txt_x, cy + 0.17, titulo, ha="left", va="center",
            fontsize=10.5, fontweight="bold", color="#222222", zorder=4)
    ax.text(txt_x, cy - 0.20, desc, ha="left", va="center",
            fontsize=8.2, color="#444444", zorder=4)

    # Seta para a próxima etapa
    if i < len(ETAPAS) - 1:
        y_ini = top - BOX_H
        y_fim = y_ini - GAP
        seta = FancyArrowPatch(
            (BOX_X + BOX_W / 2, y_ini), (BOX_X + BOX_W / 2, y_fim + 0.02),
            arrowstyle="-|>", mutation_scale=16, linewidth=1.6,
            color="#7F7F7F", zorder=1,
        )
        ax.add_patch(seta)

# ── Colchetes de fase à esquerda ─────────────────────────────────────────
for fase, (cor_solida, _, rotulo) in FASES.items():
    ys = [cy for cy, f in centros_y if f == fase]
    y_topo = max(ys) + BOX_H / 2
    y_base = min(ys) - BOX_H / 2
    x_col = 2.55
    # linha vertical do colchete
    ax.plot([x_col, x_col], [y_base, y_topo], color=cor_solida, linewidth=3.2,
            solid_capstyle="round", zorder=2)
    # rótulo da fase
    ax.text(1.15, (y_topo + y_base) / 2, rotulo, ha="center", va="center",
            fontsize=8.0, fontweight="bold", color=cor_solida, linespacing=1.35)

# Rodapé
ax.text(5.0, 0.20,
        "Etapas 1–3 e a seleção conceitual seguem a metodologia CAPTO (Zárate et al., 2023).",
        ha="center", va="center", fontsize=7.8, color="#777777", style="italic")

plt.tight_layout()
plt.savefig(OUT_PATH, dpi=200, bbox_inches="tight", facecolor="white")
print(f"[OK] Fluxograma gerado: {OUT_PATH}")
