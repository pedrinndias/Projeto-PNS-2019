# Spec — Eixo Nutricional (IRNI + Cluster) e Desenho 3 (NB03c)

> **Status:** PLANEJAMENTO — ainda **não implementado** em código nem consumido pelo pipeline.
> Este documento é o mapa para (a) codar NB03c/IRNI/cluster e (b) escrever a seção de Métodos do artigo.
> **Data:** 16/06/2026. **Autor do plano:** Pedro Dias Soares (orientação Prof. Luis Enrique Zárate).

## 0. Motivação

Nos Desenhos 1 e 2, a **nutrição saiu fraca e contraintuitiva**: nenhum alimento pró-inflamatório
atingiu significância, o quadrante "Pró-inflamatório" tem *menos* artrite (gradiente invertido) e, na
análise de entropia, a dieta fica longe do topo do ranking por SU. Causa provável: **causalidade reversa**
(o diagnóstico muda a dieta) + alta imputação dos itens alimentares (57–74%).

Para dar à nutrição um eixo **mais forte e defensável**, adotamos **três peças complementares**:

1. **IRNI** — índice *a priori* ponderado pela literatura (proxy adaptado do DII).
2. **Cluster alimentar (k-means)** — padrões *a posteriori* dirigidos pelos dados → 1 feature categórica.
3. **Desenho 3 (NB03c)** — recorte que segura a artrite constante para reduzir a causalidade reversa.

O antigo `Padrao_Alimentar_cat` (quadrantes por mediana) é **aposentado** (evita redundância/colinearidade
com IRNI+cluster, que reintroduziria a diluição de importância que estamos combatendo).

---

## 1. IRNI — Índice de Rastreamento Nutricional Inflamatório (a priori)

**Base conceitual:** *Dietary Inflammatory Index* — DII (Shivappa et al., *Public Health Nutr*, 2014).

**Ressalva honesta (declarar no artigo):** o DII original usa **quantidades de nutrientes (g/dia)**
normalizadas globalmente e cobre 45 parâmetros. A PNS só fornece **frequência (dias/semana)** e não tem
a maioria dos componentes (especiarias, ácidos graxos específicos, micronutrientes). Portanto o IRNI é um
**proxy adaptado e direcional** do DII — captura o eixo pró × anti-inflamatório, **não** o DII validado.
Enquadrar como *"índice inflamatório adaptado, inspirado no DII"*.

### 1.1 Dois esquemas de peso (testar AMBOS — sensibilidade embutida)

Positivo = pró-inflamatório; negativo = anti-inflamatório; 0 = neutro/ambíguo.
A decisão "graded vs direção" não é arbitrada a priori: **rodamos os dois** e mostramos que o resultado é
robusto (ou não) à escolha dos pesos. Isso é o que blinda o índice contra um revisor.

| Item | Var | `graded` | `direcao` | Razão |
|---|---|:--:|:--:|---|
| Doces/ultraprocessados | P02501 | +2 | +1 | açúcar + ultraprocessamento (forte) |
| Substituir almoço por lanche | P02602 | +1 | +1 | refeição ultraprocessada |
| Refrigerante | P02002 | +1 | +1 | açúcar |
| Suco em pó/caixinha | P02001 | +1 | +1 | açúcar + aditivos |
| Carne vermelha | P01101 | +1 | +1 | gordura saturada, ferro heme |
| Feijão | P006 | −1 | −1 | fibra, polifenóis |
| Frango | P013 | 0 | 0 | proteína magra ~neutra |
| Frutas | P018 | −2 | −1 | fibra, vit. C, flavonoides |
| Verduras/legumes | P00901 | −2 | −1 | fibra, carotenoides, magnésio |
| Peixe | P015 | −2 | −1 | ômega-3 (forte anti) |
| Suco de fruta natural | P01601 | −1 | −1 | vit. C/flavonoides, *com* açúcar (ressalva) |
| Leite | P023 | 0 | 0 | laticínio é ambíguo no DII |

**Itens ambíguos** (leite, frango) = peso 0 e declarados como tal no artigo.

### 1.2 Fórmula

```
IRNI = Σ_i ( peso_i × z_i )
```
onde `z_i` = frequência do item *i* **padronizada (z-score)**. Maior IRNI ⇒ dieta mais pró-inflamatória.

- **Padronização (z-score) e qualquer corte derivado do IRNI são ajustados IN-FOLD** (só no treino do
  fold), mesma regra da imputação e do cluster — evita vazamento treino/teste.
- **Embutidos (P00620):** carne processada = pró-inflamatório forte, mas é variável "dia anterior"
  (binária), escala diferente das frequências. **Decisão pendente:** (a) incluir como termo binário +2 à
  parte, ou (b) deixar fora do IRNI contínuo e citar como limitação. *Recomendação: (b) por coerência de escala.*

### 1.3 Saídas
- `IRNI_graded` e `IRNI_direcao` (duas colunas contínuas).
- Comparar as duas na seção de sensibilidade (correlação entre elas; estabilidade de sinal/importância).

---

## 2. Cluster alimentar — padrões a posteriori (k-means)

- **Entrada:** os mesmos 12 itens de frequência da §1.1, **padronizados (z-score)**.
- **k:** testar k = 2..6; escolher por **silhueta + cotovelo + interpretabilidade** (provável k=3:
  protetor / pró-inflamatório / misto).
- **Saída:** 1 feature categórica `Cluster_Alimentar`, com **rótulos atribuídos pelos centróides**
  (o cluster com itens pró altos = "pró-inflamatório", etc.).
- **Sutileza:** IDs do k-means não têm ordem nem rótulo fixo → **mapear cluster→rótulo pelos centróides a
  cada ajuste** (senão o rótulo "vira" entre execuções/folds).
- **Vazamento — distinguir os dois usos:**
  - **CV (métricas honestas):** k-means ajustado **só no treino do fold**; teste atribuído ao centróide
    mais próximo.
  - **Modelo final interpretável (a árvore que vai no artigo):** k-means ajustado no treino inteiro, 1 vez.
- `random_state = 42`.

---

## 3. Triangulação (IRNI + Cluster) e teste de honestidade

IRNI (a priori, contínuo) + Cluster (a posteriori, categórico) = as **duas escolas** de padrões alimentares
(Hu, *Curr Opin Lipidol*, 2002). Juntos = força metodológica, **desde que o quadrante-mediana seja aposentado**.

**Teste de honestidade (vai no artigo):** comparar a **SU (entropia) e a importância (árvore/RF)** do IRNI e
do `Cluster_Alimentar` contra a dos **12 itens isolados**. Se o agregado sobe no ranking, mostramos que a
agregação **concentrou** um sinal antes diluído entre features correlacionadas — e **não** que o inventamos.
Se mesmo assim a nutrição ficar embaixo, **isso é um achado** (coerente com causalidade reversa + corte
transversal), e é reportado como tal.

---

## 4. Desenho 3 (NB03c) — recorte intra-artrite

- **Coorte:** só idosos **com artrite** (494 puros + 4.025 com comorbidade = **4.519**).
- **Alvo:** tem ≥1 comorbidade → **1 = 4.025 vs 0 = 494** (desbalanceado ~**8,15:1**; minoria = artrite pura).
- **Anti-leakage (crítico):** as 13 comorbidades Q* e os exames condicionais **definem o alvo** → ficam fora
  das features (seriam preditores perfeitos). `n_comorbidades` é **derivado do alvo** → **não** é feature;
  entra apenas como **eixo de desfecho** na análise de gradiente (§4.2).

### 4.1 ⚠️ O confundidor central (e como trabalhá-lo)

Ao prever "tem comorbidade", parte do sinal alimentar reflete o **manejo dietético da própria comorbidade**
(hipertensão/diabetes têm orientação de dieta), **não** a artrite/inflamação. O Desenho 3 **troca** o
confundidor "artrite → dieta" por "**comorbidade → dieta**". Estratégia para separar os efeitos:

1. **Dupla contagem de comorbidade.** Definir dois contadores:
   - `n_comorb_total` — todas as 13.
   - `n_comorb_naodieteticas` — **excluindo** as de manejo dietético: hipertensão (Q00201), diabetes
     (Q03001), colesterol (Q060), doença cardíaca (Q06306). Restam: depressão (Q092), asma (Q074),
     câncer (Q120), AVC (Q068), renal (Q124), DPOC (Q11604), outra mental (Q11006), outra crônica (Q128),
     DORT (Q088).
   - **Teste-chave:** se o gradiente IRNI×carga **persiste com `n_comorb_naodieteticas`**, o sinal **não** é
     só manejo dietético. Se some, é majoritariamente manejo da comorbidade → declarado honestamente.
2. **Falsification / controle negativo.** Comparar IRNI entre *artríticos com só comorbidades não-dietéticas*
   vs *artrite pura*. Diferença residual aqui é mais limpa de confundimento dietético.
3. **Triangulação dos 3 desenhos** (tabela de consistência): D1 (puro vs saudável — sem confundidor de
   comorbidade, mas reverso de artrite + n pequeno), D2 (com comorbidade vs saudável — os dois confundidores),
   D3 (intra-artrite — segura a artrite, isola o gradiente de comorbidade). **Direção estável do sinal
   nutricional entre os três = robustez**; se inverte, aprende-se qual confundidor domina.

### 4.2 Entrega central do Desenho 3

O ganho **não** é o classificador (494 é pouco e enviesado), e sim o **gradiente associativo dose-resposta**:
> **IRNI × `n_comorbidades`** (total e não-dietética): *entre os artríticos, uma dieta mais pró-inflamatória
> acompanha maior carga de comorbidade?* — coerente, citável, e é o que justifica preservar `n_comorbidades`
> (hoje descartado no NB03b).

### 4.3 Pergunta de pesquisa do Desenho 3 (honesta)
*"Entre idosos brasileiros com artrite, padrões alimentares mais pró-inflamatórios estão associados a maior
carga de multimorbidade?"* — pergunta **distinta** de "dieta → artrite", e publicável por si só.

---

## 5. Defesa no artigo (esqueleto da subseção de Métodos)

1. Duas abordagens complementares — a priori (IRNI/DII, Shivappa 2014) e a posteriori (cluster, Hu 2002).
2. Critérios **fixados antes** de ver importância (variáveis, z-score, k por silhueta, pesos graded+direção).
3. **Sem vazamento** (z-score, cluster, cortes e imputação ajustados in-fold).
4. **Importância reportada, não engenheirada**; causalidade reversa + corte transversal como limitação.
5. Desenho 3 como **triangulação**, com o gradiente IRNI×carga como achado principal e o confundidor de
   comorbidade declarado + os testes de §4.1 (dupla contagem / falsification).

**Citações-âncora:** Shivappa et al. (2014, DII); Hu (2002, dietary patterns); Ribeiro & Zárate (2019, ESWA);
Louzada et al. (2015) e Claro et al. (2021) (ultraprocessados/Brasil); NOVA.

---

## 6. Plano de implementação (ordem proposta)

1. `config.toml`: seção `[nutricao.irni]` (dois esquemas) + `[nutricao.cluster]` — **já adicionada** (planejamento).
2. **NB03c** (`notebooks/03c_preprocessamento_desenho3.ipynb`): coorte intra-artrite, alvo "tem comorbidade",
   preserva `n_comorb_total` e `n_comorb_naodieteticas` (fora das features), anti-leakage das Q*.
3. **IRNI**: helper que lê os pesos do config e gera `IRNI_graded`/`IRNI_direcao` (z-score in-fold no NB06;
   versão descritiva na base persistida). Reusar nos 3 desenhos.
4. **Cluster**: k-means no NB06 (in-fold na CV; ajuste único no treino p/ a árvore final). Feature `Cluster_Alimentar`.
5. **Entropia/modelagem** (NB06 §3–8) passam a consumir IRNI + Cluster (e o quadrante sai).
6. Gradiente IRNI×carga (§4.2) + tabela de triangulação dos 3 desenhos.

> Pré-requisitos herdados: `imblearn` a instalar; reexecução do pipeline pendente (mapas ordinais).

---

## 7. Decisões em aberto
- [ ] Pesos do IRNI: rodar **graded e direção** (decidido) — confirmar tabela §1.1.
- [ ] Embutidos (P00620): dentro (binário +2) ou fora (recomendado). 
- [ ] k do cluster: por silhueta+interpretabilidade (provável 3) — confirmar após ver os dados.
- [ ] Desenho 3: classificador é secundário; entrega central = gradiente IRNI×carga (total e não-dietética).
