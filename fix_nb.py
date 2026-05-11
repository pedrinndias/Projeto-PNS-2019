import json
path = 'd:/Faculdade/Semestre 3/Mineração de Dados/Python/Projeto/Projeto_PNS/notebooks/02_analise_exploratoria_bivariada.ipynb'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

rep1_old = '    "return pd.to_numeric(serie, errors=\'coerce\') == 1\\n",'
rep1_new = '    "mask_num = pd.to_numeric(serie, errors=\'coerce\') == 1\\n",\n    "mask_str = serie.astype(str).str.strip().str.lower().isin([\'1\', \'01\', \'sim\', \'realizada\'])\\n",\n    "return mask_num | mask_str\\n",'

rep2_old = '    "    # Testa numérico (int 1, float 1.0) E string (\'1\', \'01\', \' 1\')\\n",\n    "    mask_num = pd.to_numeric(col, errors=\'coerce\') == 1\\n",\n    "    mask_str = col.astype(str).str.strip().isin([\'1\', \'01\'])\\n",\n    "    mask = mask_num | mask_str\\n",'
rep2_new = '    "    # Testa numérico (int 1, float 1.0) E string (\'1\', \'01\', \' 1\', \'realizada\')\\n",\n    "    mask_num = pd.to_numeric(col, errors=\'coerce\') == 1\\n",\n    "    mask_str = col.astype(str).str.strip().str.lower().isin([\'1\', \'01\', \'realizada\', \'sim\'])\\n",\n    "    mask = mask_num | mask_str\\n",'

rep3_old = '    "    mask_num = pd.to_numeric(col, errors=\'coerce\') == 1\\n",\n    "    mask_str = col.astype(str).str.strip().isin([\'1\', \'01\'])\\n",\n    "    mask = mask_num | mask_str\\n",'
rep3_new = '    "    mask_num = pd.to_numeric(col, errors=\'coerce\') == 1\\n",\n    "    mask_str = col.astype(str).str.strip().str.lower().isin([\'1\', \'01\', \'realizada\', \'sim\'])\\n",\n    "    mask = mask_num | mask_str\\n",'

rep4_old = '    "    mask_m = detectar_sim(df_geral[\'C006\'])\\n",\n    "    mask_f = pd.to_numeric(df_geral[\'C006\'], errors=\'coerce\') == 2\\n",'
rep4_new = '    "    mask_m = df_geral[\'C006\'].astype(str).str.strip().str.lower().isin([\'1\', \'homem\'])\\n",\n    "    mask_f = df_geral[\'C006\'].astype(str).str.strip().str.lower().isin([\'2\', \'mulher\'])\\n",'

rep5_old = '    "    for cod, nome in [(\'1\',\'Sem instrução\'),(\'2\',\'Fund. incompleto\'),\\n",\n    "                      (\'3\',\'Fund. completo/Médio\'),(\'4\',\'Superior\')]:\\n",\n    "        linhas.append(prevalencia(df_geral,\\n",\n    "                                  df_geral[\'VDD004A\'].astype(str).str.strip()==cod,\\n",\n    "                                  f\'Escol.: {nome}\'))\\n",'
rep5_new = '    "    df_geral[\'VDD_str\'] = df_geral[\'VDD004A\'].astype(str).str.strip().str.lower()\\n",\n    "    for sub, nome in [([\'sem instru\', \'1\'], \'Sem instrução\'),\\n",\n    "                      ([\'fundamental incompleto\', \'2\'], \'Fund. incompleto\'),\\n",\n    "                      ([\'fundamental completo\', \'dio completo\', \'dio incompleto\', \'3\'], \'Fund. completo/Médio\'),\\n",\n    "                      ([\'superior\', \'4\'], \'Superior\')]:\\n",\n    "        mask = df_geral[\'VDD_str\'].apply(lambda x: any(s in str(x) for s in sub))\\n",\n    "        linhas.append(prevalencia(df_geral, mask, f\'Escol.: {nome}\'))\\n",'

content = content.replace(rep1_old, rep1_new)
content = content.replace(rep2_old, rep2_new)
content = content.replace(rep3_old, rep3_new)
content = content.replace(rep4_old, rep4_new)
content = content.replace(rep5_old, rep5_new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
