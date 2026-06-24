// ============================================================================
// Apresentação — Modelagem supervisionada (NB06 §4) · Ablação por blocos
// PNS 2019 · Artrite em idosos · dados reais de data/results/modelagem/
// Mesma identidade visual dos decks NB04 / Desenho 3. pptxgenjs.
// ============================================================================
const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.layout = "LAYOUT_WIDE";
p.author = "Pedro Dias Soares";
p.title  = "Modelagem — Nutrição × Artrite · PNS 2019";
const W = 13.3, H = 7.5;

const NAVY="1E2761", NAVY2="2A3470", INK="2B2B2B", ICE="CADCFC", GREY="6B7280",
      ART="C0392B", SAU="27AE60", GOLD="E8A33D", LIGHT="F4F6FB", WHITE="FFFFFF",
      BLUE="2980B9", PURP="8E44AD", LINEC="E3E8F5";
const HF="Georgia", BF="Calibri", FIG="figuras/";
const sh=()=>({type:"outer",color:"000000",blur:7,offset:3,angle:135,opacity:0.16});

let N=0;
function slide(){ const s=p.addSlide(); s.background={color:WHITE}; return s; }
function kicker(s,t,c=GOLD){ s.addText(t.toUpperCase(),{x:0.7,y:0.5,w:12,h:0.32,
  fontFace:BF,fontSize:12,bold:true,color:c,charSpacing:3,margin:0}); }
function title(s,t,c=NAVY,size=30,w=12.2){ s.addText(t,{x:0.7,y:0.85,w,h:0.95,
  fontFace:HF,fontSize:size,bold:true,color:c,margin:0}); }
function foot(s){ N++;
  s.addText("NB06 §4 · Ablação por blocos — PNS 2019 · Artrite em idosos ≥60",
    {x:0.7,y:H-0.42,w:9,h:0.3,fontFace:BF,fontSize:9,color:GREY,margin:0});
  s.addText(String(N),{x:W-1.0,y:H-0.42,w:0.4,h:0.3,fontFace:BF,fontSize:9,
    color:GREY,align:"right",margin:0}); }
function figFit(mw,mh,ratio){ let w=mw,h=w/ratio; if(h>mh){h=mh;w=h*ratio;} return [w,h]; }
function fig(s,file,ratio,maxW,maxH,y){ const [w,h]=figFit(maxW,maxH,ratio);
  s.addImage({path:FIG+file,x:(W-w)/2,y,w,h,shadow:sh()}); return h; }
function card(s,x,y,w,h,bar,fill=LIGHT){ s.addShape(p.shapes.RECTANGLE,{x,y,w,h,
  fill:{color:fill},line:{color:LINEC,width:1},shadow:sh()});
  s.addShape(p.shapes.RECTANGLE,{x,y,w:0.09,h,fill:{color:bar}}); }
function takeaway(s,txt,y=6.35,cor=SAU,rot="O que isso significa:  "){
  s.addShape(p.shapes.RECTANGLE,{x:0.7,y,w:11.9,h:0.78,fill:{color:"EEF6F0"},line:{color:cor,width:1}});
  s.addText([{text:rot,options:{bold:true,color:cor}},{text:txt,options:{color:INK}}],
    {x:0.95,y:y+0.04,w:11.4,h:0.7,fontFace:BF,fontSize:13,valign:"middle",margin:0,lineSpacingMultiple:1.06}); }

// ═══════════════════════════════════════════════════════════════════ 1 CAPA
(()=>{ const s=p.addSlide(); s.background={color:NAVY};
  s.addShape(p.shapes.RECTANGLE,{x:0,y:0,w:0.28,h:H,fill:{color:GOLD}});
  s.addText("MINERAÇÃO DE DADOS EM SAÚDE · PNS 2019",{x:0.9,y:1.2,w:11,h:0.4,
    fontFace:BF,fontSize:15,bold:true,color:ICE,charSpacing:4,margin:0});
  s.addText("Nutrição e perfil sociodemográfico na artrite do idoso",{x:0.9,y:1.75,w:11.8,h:1.5,
    fontFace:HF,fontSize:38,bold:true,color:WHITE,margin:0,lineSpacingMultiple:0.98});
  s.addText("Modelagem supervisionada por ablação de blocos — o que diferencia idosos com artrite dos saudáveis?",
    {x:0.9,y:3.35,w:11.6,h:0.8,fontFace:BF,fontSize:18,color:ICE,margin:0,lineSpacingMultiple:1.05});
  s.addText("Árvore · Floresta · Naïve-Bayes · Regressão Logística  ·  IRNI + Cluster alimentar in-fold  ·  RUS",
    {x:0.9,y:4.25,w:11.6,h:0.5,fontFace:BF,fontSize:13,italic:true,color:"AEB9D9",margin:0});
  s.addShape(p.shapes.LINE,{x:0.9,y:5.5,w:4.2,h:0,line:{color:GOLD,width:1.5}});
  s.addText([{text:"Pedro Dias Soares",options:{bold:true,color:WHITE,breakLine:true}},
    {text:"Orientador: Prof. Dr. Luis Enrique Zárate — PUC Minas (LICAP)",options:{color:ICE}}],
    {x:0.9,y:5.65,w:11,h:0.9,fontFace:BF,fontSize:14,lineSpacingMultiple:1.15,margin:0});
})();

// ═══════════════════════════════════════════════════════════════════ 2 PERGUNTA
(()=>{ const s=slide(); kicker(s,"A pergunta de pesquisa");
  title(s,"O modelo é uma régua, não um diagnosticador");
  s.addShape(p.shapes.RECTANGLE,{x:0.7,y:1.95,w:11.9,h:1.25,fill:{color:LIGHT},line:{color:GOLD,width:1.3}});
  s.addText("“Quais padrões nutricionais e características sociodemográficas diferenciam, no Brasil, os idosos com artrite e reumatismo dos idosos saudáveis, segundo a PNS 2019 e com algoritmos supervisionados?”",
    {x:1.0,y:2.05,w:11.3,h:1.05,fontFace:HF,fontSize:16,italic:true,color:NAVY,valign:"middle",margin:0,lineSpacingMultiple:1.08});
  const cols=[
    ["A dieta separa os grupos?","Mede o poder do bloco nutricional — isolado e somado ao resto.",SAU],
    ["Quais fatores, e em que ordem?","Ranking por SU, importância Gini e Odds Ratio ajustado.",BLUE],
    ["A dieta resiste ao ajuste?","O sinal nutricional sobrevive ao controlar sexo, idade e saúde?",PURP],
  ];
  const x0=0.7,cw=3.85,gx=0.35,y0=3.55;
  cols.forEach((c,i)=>{ const cx=x0+i*(cw+gx); card(s,cx,y0,cw,2.0,c[2]);
    s.addText(c[0],{x:cx+0.28,y:y0+0.2,w:cw-0.5,h:0.7,fontFace:HF,fontSize:15.5,bold:true,color:c[2],margin:0,lineSpacingMultiple:1.0});
    s.addText(c[1],{x:cx+0.28,y:y0+0.95,w:cw-0.5,h:0.95,fontFace:BF,fontSize:12.5,color:INK,margin:0,lineSpacingMultiple:1.1}); });
  takeaway(s,"é um uso DESCRITIVO do supervisionado (regras + fatores), no estilo dos 6 trabalhos do grupo — não um classificador de produção.",6.35,NAVY,"Enquadramento:  ");
  foot(s);
})();

// ═══════════════════════════════════════════════════════════════════ 3 RELACIONADOS
(()=>{ const s=slide(); kicker(s,"Trabalhos relacionados · grupo LICAP (PNS 2019)");
  title(s,"Seis estudos, uma mesma receita");
  const hd=t=>({text:t,options:{fill:{color:NAVY},color:WHITE,bold:true,align:"center",valign:"middle",fontSize:11.5}});
  const data=[
    [hd("Estudo"),hd("Algoritmos"),hd("Desbalanço"),hd("Resultado")],
    ["DPOC (CBIS'24)","DT · NB · RF · MLP · AdaBoost","RUS","RF · F1 75%"],
    ["Hipertensão (CBIS'24)","J48 (regras) · RF","RUS","RF · F1 75%"],
    ["TOC (SBBD'24)","EBM · Árvore","RUS","+30,8% F1 ao somar bloco socioambiental"],
    ["AVC idoso×meia-idade (SBBD'24)","Árvore de Decisão","RUS","perfis distintos por faixa"],
    ["Depressão (SBBD'24)","DT · NB · RF","RUS","RF · F1 82%"],
    ["Artrite+Depressão (SBBD'25)","DT · RF","undersampling","76–80% (irmão deste estudo)"],
  ];
  s.addTable(data,{x:0.7,y:1.95,w:12.0,colW:[3.1,3.9,1.7,3.3],
    rowH:[0.46,0.4,0.4,0.46,0.4,0.4,0.46],fontFace:BF,fontSize:11.5,valign:"middle",align:"center",
    border:{pt:0.5,color:"D9DEEA"},fill:{color:"FBFCFE"},color:INK});
  takeaway(s,"todos usam CAPTO + faixas de domínio + RUS + Árvore/Floresta + F1 com IC95%. Adotamos a manobra do TOC — medir o GANHO ao acrescentar um bloco — para isolar a contribuição da nutrição.",6.0,BLUE,"Padrão herdado:  ");
  foot(s);
})();

// ═══════════════════════════════════════════════════════════════════ 4 MÉTODO
(()=>{ const s=slide(); kicker(s,"Método · ablação por blocos");
  title(s,"Cinco conjuntos para medir o peso da dieta");
  const hd=t=>({text:t,options:{fill:{color:NAVY},color:WHITE,bold:true,align:"center",valign:"middle",fontSize:12}});
  const data=[
    [hd("Conjunto"),hd("Atributos"),hd("O que mede")],
    [{text:"M0",options:{bold:true,color:BLUE,align:"center"}},"só sociodemográfico","linha de base “quem é a pessoa”"],
    [{text:"M1",options:{bold:true,color:SAU,align:"center"}},"só nutrição","poder isolado da dieta"],
    [{text:"M2",options:{bold:true,color:ART,align:"center"}},"socio + nutrição","ganho da dieta sobre M0 — conjunto-resposta"],
    [{text:"Mc",options:{bold:true,color:GREY,align:"center"}},"socio + controle (saúde, comorbidade…)","base sem dieta, com confundidores"],
    [{text:"M3",options:{bold:true,color:PURP,align:"center"}},"completo (socio+nutri+controle)","ganho da dieta sobre Mc"],
  ];
  s.addTable(data,{x:0.7,y:1.95,w:12.0,colW:[1.4,5.4,5.2],rowH:[0.5,0.5,0.5,0.55,0.6,0.5],
    fontFace:BF,fontSize:13,valign:"middle",align:"left",border:{pt:0.5,color:"D9DEEA"},fill:{color:"FBFCFE"},color:INK});
  s.addShape(p.shapes.RECTANGLE,{x:0.7,y:5.35,w:11.9,h:0.95,fill:{color:LIGHT},line:{color:GOLD,width:1}});
  s.addText([{text:"Resposta quantitativa:   ",options:{bold:true,color:NAVY}},
    {text:"ΔF1(nutrição) = F1(M2) − F1(M0)   e   F1(M3) − F1(Mc).   ",options:{color:INK}},
    {text:"Δ ≈ 0  ⇒  a dieta não diferencia além do resto.",options:{bold:true,color:ART}}],
    {x:0.95,y:5.45,w:11.4,h:0.75,fontFace:BF,fontSize:13.5,valign:"middle",margin:0,lineSpacingMultiple:1.05});
  takeaway(s,"DT (regras), RF (desempenho), NB e LogReg (OR) · RandomizedSearchCV · RUS in-fold · 10-fold F1±IC95 · teste held-out desbalanceado.",6.55,NAVY,"Protocolo:  ");
  foot(s);
})();

// ═══════════════════════════════════════════════════════════════════ 5 EIXO NUTRICIONAL
(()=>{ const s=slide(); kicker(s,"Como a nutrição entra no modelo");
  title(s,"O eixo nutricional “os três juntos”");
  const cols=[
    ["Itens de frequência","13 alimentos discretizados: feijão, frango, frutas, verduras, peixe, doces, refrigerante, tipo de leite, sal…","granularidade (qual alimento)",SAU],
    ["IRNI (contínuo)","Índice inflamatório adaptado do DII (Shivappa 2014): Σ pesoᵢ·zᵢ. Dois esquemas de peso (sensibilidade).","síntese pró/anti-inflamatória",BLUE],
    ["Cluster alimentar","k-means sobre os 12 itens → 1 rótulo ordinal (protetor→pró-inflamatório).","padrão a posteriori",PURP],
  ];
  const x0=0.7,cw=3.85,gx=0.35,y0=1.95;
  cols.forEach((c,i)=>{ const cx=x0+i*(cw+gx); card(s,cx,y0,cw,3.0,c[3]);
    s.addText(c[0],{x:cx+0.28,y:y0+0.2,w:cw-0.5,h:0.5,fontFace:HF,fontSize:16,bold:true,color:c[3],margin:0});
    s.addText(c[1],{x:cx+0.28,y:y0+0.8,w:cw-0.5,h:1.7,fontFace:BF,fontSize:12.5,color:INK,margin:0,lineSpacingMultiple:1.12});
    s.addText(c[2].toUpperCase(),{x:cx+0.28,y:y0+2.55,w:cw-0.5,h:0.35,fontFace:BF,fontSize:10.5,bold:true,color:GREY,charSpacing:1,margin:0}); });
  takeaway(s,"IRNI e Cluster são ajustados IN-FOLD (z-score e k-means só no treino de cada fold) — zero vazamento. O antigo quadrante Padrao_Alimentar foi aposentado (colinearidade).",5.5,NAVY,"Sem vazamento:  ");
  foot(s);
})();

// ═══════════════════════════════════════════════════════════════════ 6 DADOS
(()=>{ const s=slide(); kicker(s,"Dados, blocos e auditoria");
  title(s,"Dois desenhos, blocos e base limpa");
  const hd=t=>({text:t,options:{fill:{color:NAVY},color:WHITE,bold:true,align:"center",valign:"middle",fontSize:12}});
  const data=[
    [hd(""),hd("Desenho 1 — Artrite pura"),hd("Desenho 2 — Artrite+comorbidades")],
    [{text:"N (0/1)",options:{bold:true,color:INK}},"4.826  (4.332 / 494)","8.357  (4.332 / 4.025)"],
    [{text:"Balanço",options:{bold:true,color:INK}},"desbalanceado 8,8:1","≈ equilibrado 1,08:1"],
    [{text:"Blocos (socio/nutri/control)",options:{bold:true,color:INK}},"4 / 13 / 21","4 / 12 / 19"],
  ];
  s.addTable(data,{x:0.7,y:1.95,w:12.0,colW:[3.0,4.5,4.5],rowH:[0.5,0.5,0.5,0.55],
    fontFace:BF,fontSize:13,valign:"middle",align:"center",border:{pt:0.5,color:"D9DEEA"},fill:{color:"FBFCFE"},color:INK});
  const aud=[
    ["0 NaN","nas features do modelo (base imputada)"],
    ["0 vazamento","nenhuma comorbidade-filtro entre as features"],
    ["splits","estratificados 80/20 (semente 42)"],
    ["IRNI íntegro","sem NaN; faixa −18 a +29 (z-score)"],
  ];
  let x=0.7; aud.forEach((a)=>{ const w=2.97;
    s.addShape(p.shapes.RECTANGLE,{x,y:4.3,w,h:1.25,fill:{color:"EEF6F0"},line:{color:SAU,width:1}});
    s.addText(a[0],{x:x+0.15,y:4.42,w:w-0.3,h:0.4,fontFace:HF,fontSize:15,bold:true,color:SAU,align:"center",margin:0});
    s.addText(a[1],{x:x+0.15,y:4.85,w:w-0.3,h:0.6,fontFace:BF,fontSize:11,color:INK,align:"center",margin:0,lineSpacingMultiple:1.05});
    x+=w+0.1; });
  takeaway(s,"auditoria de dados aprovada (sem NaN, sem leakage, sem feature constante). Caveat honesto: os itens alimentares têm 57–74% de imputação herdada — limita a força do sinal nutricional.",5.85,GOLD,"Auditoria:  ");
  foot(s);
})();

// ═══════════════════════════════════════════════════════════════════ 7 ΔF1
(()=>{ const s=slide(); kicker(s,"Resultado 1 · ganho marginal da nutrição");
  title(s,"Acrescentar dieta não move o F1");
  fig(s,"modelagem_ablacao_f1.png",2.88,12.0,4.05,1.85);
  takeaway(s,"ΔF1 da nutrição ≈ 0 nos dois desenhos (D1 −0,01; D2 +0,01) e IC95% sobrepostos. Só-nutrição (M1, verde) é a barra mais baixa; o salto de desempenho vem do CONTROLE de saúde (Mc/M3), não da dieta.",6.3,ART);
  foot(s);
})();

// ═══════════════════════════════════════════════════════════════════ 8 ROC/CONFUSÃO
(()=>{ const s=slide(); kicker(s,"Resultado 2 · teste held-out (Floresta)");
  title(s,"As curvas ROC de M0, M2 e M3 se sobrepõem");
  const [w,h]=figFit(5.2,4.55,1.154);
  s.addImage({path:FIG+"modelagem_confusao_roc.png",x:0.7,y:1.95,w,h,shadow:sh()});
  const xr=6.4;
  s.addText("Leitura",{x:xr,y:2.0,w:6.0,h:0.4,fontFace:HF,fontSize:17,bold:true,color:NAVY,margin:0});
  const pts=[
    ["D1 (artrite pura)","AUC 0,60 (M0) → 0,63 (M2): a dieta acrescenta ~0,02. F1 baixo (≈0,23) pela base 8,8:1 — AUC é a métrica honesta aqui."],
    ["D2 (com comorbidades)","AUC 0,71 (M0) ≈ 0,72 (M2): nutrição não desloca a curva. Recall da artrite alto (base equilibrada)."],
    ["Em ambos","a curva de M2 (socio+nutrição) cola na de M0 (só socio) — a dieta não amplia a separação."],
  ];
  let y=2.55; pts.forEach(t=>{
    s.addShape(p.shapes.OVAL,{x:xr,y:y+0.05,w:0.16,h:0.16,fill:{color:GOLD}});
    s.addText(t[0],{x:xr+0.3,y:y-0.05,w:6.0,h:0.35,fontFace:HF,fontSize:13.5,bold:true,color:NAVY,margin:0});
    s.addText(t[1],{x:xr+0.3,y:y+0.32,w:6.0,h:1.0,fontFace:BF,fontSize:12,color:INK,margin:0,lineSpacingMultiple:1.1});
    y+=1.35; });
  foot(s);
})();

// ═══════════════════════════════════════════════════════════════ 8b ANÁLISE DE ERRO
(()=>{ const s=slide(); kicker(s,"Resultado 2 · análise de erro (Desenho 1)");
  title(s,"Por que a F1 do Desenho 1 é baixa");
  s.addText([{text:"Matriz: ",options:{bold:true,color:GREY}},
    {text:"recall 0,65 (acha 64 dos 99 doentes) · precisão 0,15 · ",options:{color:INK}},
    {text:"375 falsos-positivos",options:{bold:true,color:ART}},
    {text:" — o erro é quase todo FP.",options:{color:INK}}],
    {x:0.7,y:1.62,w:12,h:0.35,fontFace:BF,fontSize:13,margin:0});
  const [w,h]=figFit(11.4,3.85,2.71);
  s.addImage({path:FIG+"modelagem_analise_erro.png",x:(W-w)/2,y:2.05,w,h,shadow:sh()});
  s.addShape(p.shapes.RECTANGLE,{x:0.7,y:6.1,w:11.9,h:1.05,fill:{color:"FBEEEC"},line:{color:ART,width:1}});
  s.addText([{text:"Não é bug — é a base rate.  ",options:{bold:true,color:ART}},
    {text:"Nenhum limiar supera F1≈0,24 (teto = AUC 0,63). Sem RUS a acurácia chega a 90%, mas o recall é ZERO — não identifica nenhum doente. O RUS aceita 375 falsos-positivos para enxergar 2/3 dos 99 artríticos: consequência de 10% de prevalência + sinal nutricional fraco, não do algoritmo.",options:{color:INK}}],
    {x:0.95,y:6.18,w:11.4,h:0.9,fontFace:BF,fontSize:12,valign:"middle",margin:0,lineSpacingMultiple:1.05});
  foot(s);
})();

// ═══════════════════════════════════════════════════════════════════ 9 IMPORTÂNCIA
(()=>{ const s=slide(); kicker(s,"Resultado 3 · importância por bloco (Floresta · M3)");
  title(s,"O topo do ranking é sexo e saúde, não comida");
  fig(s,"modelagem_importancia_bloco.png",2.5,12.0,4.2,1.9);
  takeaway(s,"as variáveis de maior importância são de CONTROLE (autoavaliação de saúde, consultas, problema de coluna) e SOCIO (sexo, azul). As verdes (nutrição) aparecem no fim — coerente com a entropia (§3) e com o Δ ≈ 0.",6.3,BLUE);
  foot(s);
})();

// ═══════════════════════════════════════════════════════════════════ 10 OR AJUSTADO
(()=>{ const s=slide(); kicker(s,"Resultado 4 · Odds Ratio ajustado (dieta net de socio)");
  title(s,"Sexo domina; IRNI e Cluster não são fatores");
  const hd=t=>({text:t,options:{fill:{color:NAVY},color:WHITE,bold:true,align:"center",valign:"middle",fontSize:12}});
  const r=(v)=>({text:v,options:{align:"center"}});
  const data=[
    [hd("Fator (ajustado)"),hd("OR — Desenho 1"),hd("OR — Desenho 2"),hd("Leitura")],
    [{text:"Sexo (mulher)",options:{bold:true,color:ART}},r("2,50 ***"),r("4,74 ***"),{text:"forte e consistente",options:{align:"center",color:ART,bold:true}}],
    [{text:"Idade (faixa)",options:{bold:true,color:NAVY}},r("1,20 **"),r("1,31 ***"),r("cresce com a idade")],
    [{text:"IRNI (índice infl.)",options:{bold:true,color:SAU}},r("0,93  (ns)"),r("1,02  (ns)"),r("sem associação")],
    [{text:"Cluster alimentar",options:{bold:true,color:SAU}},r("1,03  (ns)"),r("0,74 *** ⟲"),{text:"D2: invertido (reverso)",options:{align:"center",color:GREY}}],
  ];
  s.addTable(data,{x:0.7,y:1.95,w:12.0,colW:[3.3,2.9,2.9,2.9],rowH:[0.5,0.55,0.5,0.5,0.55],
    fontFace:BF,fontSize:12.5,valign:"middle",align:"center",border:{pt:0.5,color:"D9DEEA"},fill:{color:"FBFCFE"},color:INK});
  s.addText("*** p<0,001   ** p<0,01   ns = não significativo   ⟲ = direção contraintuitiva (mais pró-inflamatório → menos doença)",
    {x:0.7,y:4.85,w:12,h:0.3,fontFace:BF,fontSize:10.5,italic:true,color:GREY,margin:0});
  takeaway(s,"ser mulher idosa multiplica a chance de artrite por 2,5–4,7×. O IRNI nunca é significativo; o único sinal de dieta (Cluster, D2) é INVERTIDO — assinatura de causalidade reversa, não de proteção.",5.4,ART);
  foot(s);
})();

// ═══════════════════════════════════════════════════════════════════ 11 REGRAS
(()=>{ const s=slide(); kicker(s,"Resultado 5 · regras da árvore (cobertura ≥ 10%)");
  title(s,"As regras descrevem perfil, não dieta");
  card(s,0.7,1.95,11.9,1.6,SAU);
  s.addText("Desenho 1 — perfil SAUDÁVEL (pureza ≈ 0,95)",{x:1.0,y:2.1,w:11,h:0.4,fontFace:HF,fontSize:14.5,bold:true,color:SAU,margin:0});
  s.addText([{text:"SE  ",options:{bold:true,color:GREY}},
    {text:"homem  E  come feijão (≥ faixa)  E  mais escolaridade",options:{color:INK}},
    {text:"   → Saudável   (cobre 12%).",options:{bold:true,color:SAU}}],
    {x:1.0,y:2.6,w:11,h:0.8,fontFace:BF,fontSize:13.5,margin:0,lineSpacingMultiple:1.1});
  card(s,0.7,3.75,11.9,2.1,ART);
  s.addText("Desenho 2 — perfil ARTRITE",{x:1.0,y:3.9,w:11,h:0.4,fontFace:HF,fontSize:14.5,bold:true,color:ART,margin:0});
  s.addText([{text:"SE  ",options:{bold:true,color:GREY}},
    {text:"mulher  E  60–69 anos  E  menor escolaridade  E  IRNI > −4,5",options:{color:INK}},
    {text:"   → Artrite   (cobre 20%, pureza 0,56).",options:{bold:true,color:ART,breakLine:true}}],
    {x:1.0,y:4.35,w:11,h:0.7,fontFace:BF,fontSize:13.5,margin:0,lineSpacingMultiple:1.1});
  s.addText("As variáveis nutricionais (feijão, sal, tipo de leite, IRNI) entram como ramos secundários — nunca como o eixo da regra. O eixo é sexo + idade + escolaridade.",
    {x:1.0,y:5.0,w:11,h:0.7,fontFace:BF,fontSize:12,italic:true,color:INK,margin:0,lineSpacingMultiple:1.1});
  takeaway(s,"mesmo no modelo de regras (a entrega descritiva do estilo LICAP), a dieta é coadjuvante: as folhas de maior cobertura são definidas por características da pessoa.",6.05,NAVY);
  foot(s);
})();

// ═══════════════════════════════════════════════════════════════════ 12 MODELOS
(()=>{ const s=slide(); kicker(s,"Comparação de modelos · conjunto-resposta M2");
  title(s,"Modelos empatam — a Árvore é competitiva");
  const hd=t=>({text:t,options:{fill:{color:NAVY},color:WHITE,bold:true,align:"center",valign:"middle",fontSize:12}});
  const r=(v)=>({text:v,options:{align:"center"}});
  const data=[
    [hd("Modelo (F1 ± IC95, 10-fold)"),hd("Desenho 1"),hd("Desenho 2")],
    [{text:"Floresta Aleatória",options:{align:"center"}},r("0,222"),r("0,700")],
    [{text:"Árvore de Decisão",options:{align:"center",bold:true,color:NAVY}},r("0,224"),r("0,690")],
    [{text:"Regressão Logística",options:{align:"center"}},r("0,231"),r("0,692")],
    [{text:"Naïve-Bayes",options:{align:"center"}},r("0,214"),r("0,528")],
  ];
  s.addTable(data,{x:0.7,y:1.95,w:8.0,colW:[3.8,2.1,2.1],rowH:[0.55,0.5,0.5,0.5,0.5],
    fontFace:BF,fontSize:12.5,valign:"middle",align:"center",border:{pt:0.5,color:"D9DEEA"},fill:{color:"FBFCFE"},color:INK});
  card(s,8.95,1.95,3.65,2.55,GOLD,WHITE);
  s.addText("t pareado + Bonferroni",{x:9.2,y:2.1,w:3.2,h:0.4,fontFace:HF,fontSize:14,bold:true,color:NAVY,margin:0});
  s.addText("Sem diferença prática relevante entre Árvore, Floresta e Logística. A Árvore — a mais interpretável — é a escolha, como nos papers do grupo.",
    {x:9.2,y:2.6,w:3.2,h:1.8,fontFace:BF,fontSize:12,color:INK,margin:0,lineSpacingMultiple:1.12});
  takeaway(s,"o desempenho baixo no D1 é da base desbalanceada (8,8:1), não dos modelos; no D2 (equilibrado) o F1 sobe para ~0,70. Em nenhum caso a nutrição é o que sustenta o número.",5.05,NAVY);
  foot(s);
})();

// ═══════════════════════════════════════════════════════════════════ 13 ENTROPIA
(()=>{ const s=slide(); kicker(s,"Checagem independente · entropia (NB06 §3)");
  title(s,"A entropia já apontava o mesmo");
  fig(s,"entropia_ranking_su.png",2.143,11.0,3.7,1.95);
  takeaway(s,"o ranking por Incerteza Simétrica (independente do classificador) coloca autoavaliação de saúde, sexo e uso de serviço no topo; a maioria dos itens alimentares fica perto de zero. Três lentes — entropia, Gini e OR — convergem.",6.0,BLUE,"Triangulação:  ");
  foot(s);
})();

// ═══════════════════════════════════════════════════════════════════ 14 DISCUSSÃO
(()=>{ const s=slide(); kicker(s,"Discussão · a resposta à pergunta");
  title(s,"O que diferencia idoso com artrite do saudável");
  const cols=[
    ["DIFERENCIAM","Sexo feminino (OR 2,5–4,7), idade mais avançada e o estado de saúde (comorbidades, limitação funcional, autoavaliação ruim).",SAU,"✓"],
    ["NÃO DIFERENCIAM","Os padrões nutricionais: ΔF1/ΔAUC ≈ 0 ao acrescentar a dieta; IRNI nunca significativo; itens no fim do ranking.",ART,"✕"],
    ["O ÚNICO SINAL DE DIETA","É invertido (D2): dieta mais pró-inflamatória associada a MENOS doença → causalidade reversa, não proteção.",GREY,"⟲"],
  ];
  let y=1.95; cols.forEach(c=>{ card(s,0.7,y,11.9,1.5,c[2]);
    s.addShape(p.shapes.OVAL,{x:0.95,y:y+0.45,w:0.6,h:0.6,fill:{color:c[2]}});
    s.addText(c[3],{x:0.95,y:y+0.45,w:0.6,h:0.6,fontFace:HF,fontSize:22,bold:true,color:WHITE,align:"center",valign:"middle",margin:0});
    s.addText(c[0],{x:1.75,y:y+0.18,w:10.6,h:0.42,fontFace:HF,fontSize:15.5,bold:true,color:c[2],margin:0});
    s.addText(c[1],{x:1.75,y:y+0.6,w:10.6,h:0.8,fontFace:BF,fontSize:12.5,color:INK,margin:0,lineSpacingMultiple:1.1});
    y+=1.62; });
  foot(s);
})();

// ═══════════════════════════════════════════════════════════════════ 15 LIMITAÇÕES
(()=>{ const s=slide(); kicker(s,"Limitações · leitura honesta");
  title(s,"Por que o nulo nutricional é esperado");
  const items=[
    ["Imputação alta dos itens","57–74% das frequências alimentares foram imputadas → o sinal individual fica diluído."],
    ["Corte transversal","A PNS é uma foto; não capta a dieta de anos antes do diagnóstico (latência da artrite)."],
    ["Causalidade reversa","O diagnóstico muda a dieta (manejo) → contamina a associação, como mostra o Cluster invertido."],
    ["Sem tipologia forte","As silhuetas do k-means são baixas (~0,10): não há padrões alimentares naturais nítidos."],
    ["IRNI ≠ DII validado","Proxy adaptado (frequência, não g/dia; 12 itens) — captura direção, não a magnitude do DII."],
    ["F1 baixo no D1","Efeito do desbalanço 8,8:1 (não do modelo); por isso reportamos também AUC e IC95%."],
  ];
  const x0=0.7,cw=5.95,gx=0.3; let y=1.95;
  items.forEach((t,i)=>{ const cx=x0+(i%2)*(cw+gx); if(i%2===0&&i>0)y+=1.45; const cy=1.95+Math.floor(i/2)*1.45;
    card(s,cx,cy,cw,1.25,GOLD);
    s.addText(t[0],{x:cx+0.28,y:cy+0.14,w:cw-0.5,h:0.4,fontFace:HF,fontSize:13.5,bold:true,color:NAVY,margin:0});
    s.addText(t[1],{x:cx+0.28,y:cy+0.55,w:cw-0.5,h:0.65,fontFace:BF,fontSize:11.5,color:INK,margin:0,lineSpacingMultiple:1.08}); });
  foot(s);
})();

// ═══════════════════════════════════════════════════════════════════ 16 CONCLUSÃO
(()=>{ const s=p.addSlide(); s.background={color:NAVY};
  s.addShape(p.shapes.RECTANGLE,{x:0,y:0,w:0.28,h:H,fill:{color:GOLD}});
  s.addText("CONCLUSÃO",{x:0.9,y:0.7,w:8,h:0.4,fontFace:BF,fontSize:13,bold:true,color:GOLD,charSpacing:3,margin:0});
  s.addText("Quem tem artrite é mulher idosa com pior saúde — não quem come pior",
    {x:0.9,y:1.1,w:11.5,h:1.2,fontFace:HF,fontSize:27,bold:true,color:WHITE,margin:0,lineSpacingMultiple:1.0});
  const pts=[
    ["A nutrição não diferencia os grupos","ΔF1/ΔAUC ≈ 0 ao acrescentar a dieta, nos dois desenhos e ajustando por confundidores."],
    ["O que separa é sociodemográfico + saúde","Sexo feminino, idade e estado de saúde concentram todo o poder discriminante."],
    ["Achado, não falha","Mostrar com rigor o limite do dado transversal é mais defensável que afirmar “dieta causa artrite”."],
    ["Coerente com todo o projeto","Casa com a entropia (§3), o Desenho 3 e a literatura — nulo honesto e triangulado."],
  ];
  let y=2.55;
  pts.forEach((t,i)=>{
    s.addShape(p.shapes.OVAL,{x:0.95,y:y+0.02,w:0.4,h:0.4,fill:{color:GOLD}});
    s.addText(String(i+1),{x:0.95,y:y+0.02,w:0.4,h:0.4,fontFace:HF,fontSize:17,bold:true,color:NAVY,align:"center",valign:"middle",margin:0});
    s.addText(t[0],{x:1.55,y:y-0.04,w:10.9,h:0.42,fontFace:HF,fontSize:16.5,bold:true,color:WHITE,margin:0});
    s.addText(t[1],{x:1.55,y:y+0.4,w:10.9,h:0.55,fontFace:BF,fontSize:12.5,color:ICE,margin:0,lineSpacingMultiple:1.05});
    y+=1.0;
  });
})();

// ═══════════════════════════════════════════════════════════════════ 17 REFERÊNCIAS
(()=>{ const s=slide(); kicker(s,"Referências e reprodutibilidade");
  title(s,"Fontes e artefatos");
  const refs=[
    "Shivappa N. et al. (2014). Designing and developing a literature-derived, population-based Dietary Inflammatory Index. Public Health Nutr.",
    "Zárate L. E. et al. (2023). CAPTO — a method for understanding problem domains for data science projects. SBBD.",
    "Cancella L. F., Zárate L. E. (2025). Caracterizando o perfil Artrite-Depressão da população brasileira (PNS 2019). SBBD.",
    "Rodrigues A. P., Zárate L. E. (2024). Fatores socioambientais na identificação do TOC (PNS 2019). SBBD.",
    "IBGE (2020). Pesquisa Nacional de Saúde 2019 — microdados.",
  ];
  let y=1.95; refs.forEach(r=>{ s.addShape(p.shapes.RECTANGLE,{x:0.7,y,w:0.09,h:0.62,fill:{color:GOLD}});
    s.addText(r,{x:0.95,y,w:11.7,h:0.62,fontFace:BF,fontSize:11.5,color:INK,valign:"middle",margin:0,lineSpacingMultiple:1.05}); y+=0.72; });
  s.addShape(p.shapes.RECTANGLE,{x:0.7,y:5.7,w:11.9,h:1.0,fill:{color:LIGHT},line:{color:LINEC,width:1}});
  s.addText([{text:"Reprodutibilidade:  ",options:{bold:true,color:NAVY}},
    {text:"notebooks/06_modelagem_ml.ipynb + notebooks/modelagem.py (com autoteste) · parâmetros em config.toml [modelagem] · artefatos em data/results/modelagem/ · semente 42.",options:{color:INK}}],
    {x:0.95,y:5.8,w:11.4,h:0.8,fontFace:BF,fontSize:12,valign:"middle",margin:0,lineSpacingMultiple:1.08});
  foot(s);
})();

p.writeFile({fileName:"Apresentacao_Modelagem_Ablacao_PNS2019.pptx"}).then(f=>{
  console.log("✅ DECK GERADO:",f);
});
