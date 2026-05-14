# -*- coding: utf-8 -*-
"""Gera o fluxograma do pipeline KDD (10 etapas) para o artigo — versão
compacta e horizontal, em 4 colunas de fase.

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

# ── Fases: (cor sólida, cor de preenchimento clara, rótulo curto) ────────
FASES = {
    "A": ("#1F3764", "#E8EDF6", "FASE 1  ·  Entendimento do\nProblema e do Domínio"),
    "B": ("#2E75B6", "#E4EFF8", "FASE 2  ·  Pré-Processamento\ndos Dados"),
    "C": ("#1E7A34", "#E4F3E8", "FASE 3  ·  Preparação\npara a Mineração"),
    "D": ("#B75E09", "#FBEEDD", "FASE 4  ·  Modelagem\ne Avaliação"),
}

# ── Etapas por fase: (numero, titulo curto) ─────────────────────────────
ETAPAS_POR_FASE = {
    "A": [(1, "Entendimento do Problema"),
          (2, "Modelagem Conceitual (CAPTO)"),
          (3, "Seleção Conceitual de Atributos")],
    "B": [(4, "Tratamento de Dados Ausentes"),
          (5, "Análise e Remoção de Outliers"),
          (6, "Preparação dos Dados")],
    "C": [(7, "Seleção de Atributos (entropia)"),
          (8, "Balanceamento das Classes (RUS)")],
    "D": [(9, "Modelos e Parametrização"),
          (10, "Treinamento e Teste")],
}

# ── Layout ───────────────────────────────────────────────────────────────
COL_W   = 4.85       # largura de cada coluna de fase
COL_GAP = 0.75       # espaço entre colunas
BOX_H   = 0.95       # altura de cada caixa de etapa
BOX_GAP = 0.30       # espaço vertical entre caixas
HEAD_H  = 0.85       # altura do cabeçalho da fase
COL_X0  = 0.35       # x da primeira coluna
TOP_Y   = 5.55       # topo da área das colunas (abaixo do título)

n_fases = len(FASES)
total_w = COL_X0 * 2 + n_fases * COL_W + (n_fases - 1) * COL_GAP

fig, ax = plt.subplots(figsize=(13.2, 4.6))
ax.set_xlim(0, total_w)
ax.set_ylim(0, 6.4)
ax.axis("off")

# Título
ax.text(total_w / 2, 6.12,
        "Processo de Descoberta de Conhecimento (KDD) — Pipeline Metodológico em 10 Etapas",
        ha="center", va="center", fontsize=12.5, fontweight="bold", color="#1F3764")

max_boxes = max(len(v) for v in ETAPAS_POR_FASE.values())  # 3

for ci, (fase, etapas) in enumerate(ETAPAS_POR_FASE.items()):
    cor_solida, cor_fill, rotulo = FASES[fase]
    cx0 = COL_X0 + ci * (COL_W + COL_GAP)
    cx_centro = cx0 + COL_W / 2

    # Cabeçalho da fase
    head = FancyBboxPatch(
        (cx0, TOP_Y - HEAD_H), COL_W, HEAD_H,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=0, facecolor=cor_solida, zorder=2,
    )
    ax.add_patch(head)
    ax.text(cx_centro, TOP_Y - HEAD_H / 2, rotulo, ha="center", va="center",
            fontsize=8.6, fontweight="bold", color="white", linespacing=1.25, zorder=3)

    # Caixas de etapa (centralizadas verticalmente na coluna)
    n = len(etapas)
    bloco_h = n * BOX_H + (n - 1) * BOX_GAP
    y_topo_bloco = TOP_Y - HEAD_H - 0.35
    # alinha o topo do bloco de todas as colunas
    for bi, (num, titulo) in enumerate(etapas):
        top = y_topo_bloco - bi * (BOX_H + BOX_GAP)
        cy = top - BOX_H / 2

        caixa = FancyBboxPatch(
            (cx0, top - BOX_H), COL_W, BOX_H,
            boxstyle="round,pad=0.02,rounding_size=0.07",
            linewidth=1.4, edgecolor=cor_solida, facecolor=cor_fill, zorder=2,
        )
        ax.add_patch(caixa)

        # Badge numérico
        badge_cx = cx0 + 0.42
        circ = plt.Circle((badge_cx, cy), 0.26, color=cor_solida, zorder=3)
        ax.add_patch(circ)
        ax.text(badge_cx, cy, str(num), ha="center", va="center",
                fontsize=9.5, fontweight="bold", color="white", zorder=4)

        # Título
        ax.text(cx0 + 0.82, cy, titulo, ha="left", va="center",
                fontsize=8.2, fontweight="bold", color="#222222", zorder=4)

        # Seta vertical para a próxima etapa da mesma fase
        if bi < n - 1:
            y_ini = top - BOX_H
            y_fim = y_ini - BOX_GAP
            ax.add_patch(FancyArrowPatch(
                (cx_centro, y_ini), (cx_centro, y_fim + 0.02),
                arrowstyle="-|>", mutation_scale=11, linewidth=1.3,
                color="#8C8C8C", zorder=1))

    # Seta horizontal para a próxima fase
    if ci < n_fases - 1:
        x_ini = cx0 + COL_W
        x_fim = x_ini + COL_GAP
        y_seta = TOP_Y - HEAD_H - 0.35 - BOX_H / 2  # altura da 1ª caixa
        ax.add_patch(FancyArrowPatch(
            (x_ini + 0.04, y_seta), (x_fim - 0.02, y_seta),
            arrowstyle="-|>", mutation_scale=15, linewidth=1.7,
            color="#595959", zorder=5))

# Rodapé curto
ax.text(total_w / 2, 0.22,
        "As etapas 1–3 seguem a metodologia CAPTO (Zárate et al., 2023). "
        "Fluxo: da esquerda para a direita; dentro de cada fase, de cima para baixo.",
        ha="center", va="center", fontsize=7.0, color="#888888", style="italic")

plt.tight_layout()
plt.savefig(OUT_PATH, dpi=220, bbox_inches="tight", facecolor="white")
print(f"[OK] Fluxograma gerado: {OUT_PATH}")
