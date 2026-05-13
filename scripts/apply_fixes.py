"""Aplica correções automatizadas nos notebooks do projeto.

Uso (rodar da raiz do projeto):
    python scripts/apply_fixes.py

Pode ser re-executado idempotentemente — checa se cada fix já foi aplicado.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"


def _load(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(path: Path, nb: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")


def _src(cell) -> str:
    s = cell.get("source", "")
    return "".join(s) if isinstance(s, list) else s


def _set_src(cell, text: str) -> None:
    cell["source"] = text.splitlines(keepends=True)


def _replace_in_cell(cell, old: str, new: str) -> bool:
    src = _src(cell)
    if old not in src:
        return False
    _set_src(cell, src.replace(old, new))
    return True


def fix_nb01() -> int:
    path = NB_DIR / "01_extracao_pre_processamento.ipynb"
    nb = _load(path)
    changed = 0
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        # gc importado mas não usado
        if _replace_in_cell(
            cell,
            "import os\n# Importa o garbage collector para liberar memória RAM se necessário.\nimport gc\n",
            "import os\n",
        ):
            changed += 1
    if changed:
        _save(path, nb)
    return changed


def fix_nb02() -> int:
    path = NB_DIR / "02_analise_exploratoria_bivariada.ipynb"
    nb = _load(path)
    changed = 0
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        src = _src(cell)

        # Fix 1: Sexo aceita 'Masculino'/'Feminino' (além de '1'/'2'/'homem'/'mulher')
        if _replace_in_cell(
            cell,
            "    mask_m = df_geral['C006'].astype(str).str.strip().str.lower().isin(['1', 'homem'])  # Máscara para homens\n"
            "    mask_f = df_geral['C006'].astype(str).str.strip().str.lower().isin(['2', 'mulher'])  # Máscara para mulheres",
            "    mask_m = df_geral['C006'].astype(str).str.strip().str.lower().isin(['1', 'homem', 'masculino'])  # Máscara para homens\n"
            "    mask_f = df_geral['C006'].astype(str).str.strip().str.lower().isin(['2', 'mulher', 'feminino'])  # Máscara para mulheres",
        ):
            changed += 1

        # Fix 2: Bootstrap 500 -> 2000 (IC mais estável para n pequeno)
        if _replace_in_cell(
            cell,
            "             s2.sample(len(s2), replace=True).median() for _ in range(500)]",
            "             s2.sample(len(s2), replace=True).median() for _ in range(2000)]",
        ):
            changed += 1

        # Fix 3: χ²/Fisher na Tab 2-B ignorando NaN em vez de tratá-lo como categoria
        if _replace_in_cell(
            cell,
            "    # Calcular p-valor global para a variável (χ² ou Fisher)\n"
            "    serie_all = df_biv[col].astype(str).str.strip()  # Converte coluna para string, remove espaços",
            "    # Calcular p-valor global para a variável (χ² ou Fisher)\n"
            "    serie_all = df_biv[col].dropna().astype(str).str.strip()  # Remove NaN antes de converter para string (evita categoria 'nan')",
        ):
            changed += 1

        # Fix 4: Proteção do mode() vazio na Tab 2-C
        if _replace_in_cell(
            cell,
            "    mod1 = serie[df_biv['Classe']=='Com Artrite'].mode().iloc[0]  # Moda em Artrite\n"
            "    mod2 = serie[df_biv['Classe']=='Saudável'].mode().iloc[0]  # Moda em Saudável",
            "    m1 = serie[df_biv['Classe']=='Com Artrite'].dropna().mode()  # Moda em Artrite (vazio se 100% NaN)\n"
            "    m2 = serie[df_biv['Classe']=='Saudável'].dropna().mode()  # Moda em Saudável (vazio se 100% NaN)\n"
            "    if m1.empty or m2.empty: continue  # Sem moda calculável → pula variável\n"
            "    mod1, mod2 = m1.iloc[0], m2.iloc[0]",
        ):
            changed += 1

        # Fix 5: VARS_QUAL na Tab 2-B também limpa NaN nos grupos
        if _replace_in_cell(
            cell,
            "    serie_art = df_biv[df_biv['Classe']=='Com Artrite'][col].astype(str).str.strip()  # Dados do grupo Artrite\n"
            "    serie_sau = df_biv[df_biv['Classe']=='Saudável'][col].astype(str).str.strip()  # Dados do grupo Saudável",
            "    serie_art = df_biv[df_biv['Classe']=='Com Artrite'][col].dropna().astype(str).str.strip()  # Dados do grupo Artrite (sem NaN)\n"
            "    serie_sau = df_biv[df_biv['Classe']=='Saudável'][col].dropna().astype(str).str.strip()  # Dados do grupo Saudável (sem NaN)",
        ):
            changed += 1

    if changed:
        _save(path, nb)
    return changed


def fix_nb03() -> int:
    path = NB_DIR / "03_preprocessamento_v3.ipynb"
    nb = _load(path)
    changed = 0
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue

        # Fix 1: get_dummies com dtype=int (evita bool que confunde select_dtypes)
        if _replace_in_cell(
            cell,
            "    dummies = pd.get_dummies(df_step6[cols_ohe], prefix=cols_ohe,\n"
            "                             drop_first=True, dummy_na=False)",
            "    dummies = pd.get_dummies(df_step6[cols_ohe], prefix=cols_ohe,\n"
            "                             drop_first=True, dummy_na=False, dtype=int)",
        ):
            changed += 1

        # Fix 2: substituição de .codes.replace(-1, 0) (ndarray sem .replace)
        if _replace_in_cell(
            cell,
            "    for col in cols_nao_num:\n"
            "        X[col] = pd.Categorical(X[col]).codes.replace(-1, 0)",
            "    for col in cols_nao_num:\n"
            "        codes = pd.Categorical(X[col]).codes\n"
            "        X[col] = np.where(codes == -1, 0, codes).astype(int)",
        ):
            changed += 1

        # Fix 3: IMC bins corrigidos para OMS (25, 30 em vez de 24.9, 29.9)
        if _replace_in_cell(
            cell,
            "    df_step5['IMC_cat'] = pd.cut(df_step5['IMC'], bins=[0,18.5,24.9,29.9,100],\n"
            "                                  labels=[0,1,2,3], include_lowest=True).astype(float)",
            "    df_step5['IMC_cat'] = pd.cut(df_step5['IMC'], bins=[0,18.5,25,30,100],\n"
            "                                  labels=[0,1,2,3], include_lowest=True, right=False).astype(float)",
        ):
            changed += 1

        # Fix 4: guard para VARS_VIZ_OUT vazio (i indefinido)
        if _replace_in_cell(
            cell,
            "for j in range(i+1, len(axes)): axes[j].set_visible(False)",
            "if VARS_VIZ_OUT:\n"
            "    for j in range(len(VARS_VIZ_OUT), len(axes)): axes[j].set_visible(False)",
        ):
            changed += 1

        # Fix 5: % outliers sobre observações válidas
        if _replace_in_cell(
            cell,
            "        print(f'  {col:12s}: {n_out:4d} outliers → NaN ({100*n_out/len(df_step2):.2f}%)')",
            "        n_validos = int(df_step2[col].notna().sum() + n_out)  # pré-substituição\n"
            "        pct_val = 100 * n_out / n_validos if n_validos else 0\n"
            "        print(f'  {col:12s}: {n_out:4d} outliers → NaN ({pct_val:.2f}% dos válidos)')",
        ):
            changed += 1

        if _replace_in_cell(
            cell,
            "    log_outliers.append({'Variável': col, 'n_outliers': n_out,\n"
            "                         '% outliers': round(100*n_out/len(df_step2), 2),",
            "    log_outliers.append({'Variável': col, 'n_outliers': n_out,\n"
            "                         '% outliers': round(100*n_out/max(1, int(df_step2[col].notna().sum() + n_out)), 2),",
        ):
            changed += 1

        # Fix 6: salvar etapa9 com nome correto (era etapa8 no v3 — bug de nomenclatura)
        if _replace_in_cell(
            cell,
            "salvar_fig('etapa9_diagnostico_dataset_final.png')",
            "salvar_fig('etapa9_diagnostico_dataset_final.png')",
        ):
            pass  # já está OK
        if _replace_in_cell(
            cell,
            "salvar_fig('etapa8_diagnostico_dataset_final.png')",
            "salvar_fig('etapa9_diagnostico_dataset_final.png')",
        ):
            changed += 1

    if changed:
        _save(path, nb)
    return changed


def main() -> None:
    n1 = fix_nb01()
    n2 = fix_nb02()
    n3 = fix_nb03()
    print(f"nb01: {n1} fixes aplicados")
    print(f"nb02: {n2} fixes aplicados")
    print(f"nb03: {n3} fixes aplicados")


if __name__ == "__main__":
    main()
