// ============================================================================
// Apresentação COMPLETA — Discretização (NB04) · PNS 2019 · Artrite em idosos
// Dados 100% reais de data/results/discretizacao*/  |  pptxgenjs
// ============================================================================
const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.layout = "LAYOUT_WIDE";                 // 13.3 x 7.5"
p.author = "Pedro Dias Soares";
p.title  = "Discretização — PNS 2019 Artrite";
const W = 13.3, H = 7.5;

// ── paleta ──────────────────────────────────────────────────────────────
const NAVY="1E2761", NAVY2="2A3470", INK="2B2B2B", ICE="CADCFC", GREY="6B7280",
      ART="C0392B", SAU="27AE60", GOLD="E8A33D", LIGHT="F4F6FB", WHITE="FFFFFF",
      LINEC="E3E8F5";
const HF="Georgia", BF="Calibri";
const FIG="figuras/";
const sh=()=>({type:"outer",color:"000000",blur:7,offset:3,angle:135,opacity:0.16});

// ── helpers de layout ───────────────────────────────────────────────────
let N=0;
function slide(){ const s=p.addSlide(); s.background={color:WHITE}; return s; }
function kicker(s,t,c=GOLD){ s.addText(t.toUpperCase(),{x:0.7,y:0.5,w:12,h:0.32,
  fontFace:BF,fontSize:12,bold:true,color:c,charSpacing:3,margin:0}); }
function title(s,t,c=NAVY,size=30,w=12.0){ s.addText(t,{x:0.7,y:0.85,w,h:0.95,
  fontFace:HF,fontSize:size,bold:true,color:c,margin:0}); }
function foot(s){ N++;
  s.addText("NB04 · Discretização — PNS 2019 · Artrite em idosos ≥60",
    {x:0.7,y:H-0.42,w:9,h:0.3,fontFace:BF,fontSize:9,color:GREY,margin:0});
  s.addText(String(N),{x:W-1.0,y:H-0.42,w:0.4,h:0.3,fontFace:BF,fontSize:9,
    color:GREY,align:"right",margin:0}); }
function figFit(mw,mh,ratio){ let w=mw,h=w/ratio; if(h>mh){h=mh;w=h*ratio;} return [w,h]; }
function card(s,x,y,w,h,bar,fill=LIGHT){ s.addShape(p.shapes.RECTANGLE,{x,y,w,h,
  fill:{color:fill},line:{color:LINEC,width:1},shadow:sh()});
  s.addShape(p.shapes.RECTANGLE,{x,y,w:0.09,h,fill:{color:bar}}); }
function takeaway(s,txt,y=6.35){            // faixa "leitura do resultado"
  s.addShape(p.shapes.RECTANGLE,{x:0.7,y,w:11.9,h:0.78,fill:{color:"EEF6F0"},line:{color:SAU,width:1}});
  s.addText([{text:"O que isso significa:  ",options:{bold:true,color:SAU}},
             {text:txt,options:{color:INK}}],
    {x:0.95,y:y+0.04,w:11.4,h:0.7,fontFace:BF,fontSize:13,valign:"middle",margin:0,lineSpacingMultiple:1.08}); }

// ════════════════════════════════════════════════════════════════════════
// 1 · CAPA
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=p.addSlide(); s.background={color:NAVY};
  s.addShape(p.shapes.RECTANGLE,{x:0,y:0,w:0.28,h:H,fill:{color:GOLD}});
  s.addText("MINERAÇÃO DE DADOS EM SAÚDE · PNS 2019",{x:0.9,y:1.35,w:11,h:0.4,
    fontFace:BF,fontSize:15,bold:true,color:ICE,charSpacing:4,margin:0});
  s.addText("Discretização das variáveis",{x:0.9,y:1.95,w:11.7,h:1.0,
    fontFace:HF,fontSize:48,bold:true,color:WHITE,margin:0});
  s.addText("Notebook 04 — a 7ª etapa do KDD aplicada ao estudo da artrite em idosos",
    {x:0.9,y:3.1,w:11.5,h:0.6,fontFace:BF,fontSize:19,color:ICE,margin:0});
  s.addText("Processo completo · fundamentação · resultados interpretados nos dois desenhos de estudo",
    {x:0.9,y:3.7,w:11.2,h:0.5,fontFace:BF,fontSize:14,italic:true,color:"AEB9D9",margin:0});
  s.addShape(p.shapes.LINE,{x:0.9,y:5.5,w:4.2,h:0,line:{color:GOLD,width:1.5}});
  s.addText([{text:"Pedro Dias Soares",options:{bold:true,color:WHITE,breakLine:true}},
    {text:"Orientador: Prof. Dr. Luis Enrique Zárate — PUC Minas (LICAP)",options:{color:ICE}}],
    {x:0.9,y:5.65,w:11,h:0.9,fontFace:BF,fontSize:14,lineSpacingMultiple:1.15,margin:0});
})();

// ════════════════════════════════════════════════════════════════════════
// 2 · AGENDA
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Roteiro");
  title(s,"O que esta apresentação cobre");
  const items=[
    ["1","Contexto","Onde a discretização se encaixa no processo KDD do projeto"],
    ["2","O conceito","O que é discretizar e por que é necessário (slide Introdução 12)"],
    ["3","O método","O padrão de discretização dos artigos do orientador"],
    ["4","O processo","As 6 etapas executadas no NB04, passo a passo"],
    ["5","Os resultados","Cada faixa, cada gráfico e o que significam para o trabalho"],
    ["6","O achado","A confirmação empírica do data leakage no Desenho 2"],
  ];
  const x0=0.7,y0=1.95,cw=5.95,ch=1.35,gx=0.4,gy=0.25;
  items.forEach((it,i)=>{
    const cx=x0+(i%2)*(cw+gx), cy=y0+Math.floor(i/2)*(ch+gy);
    card(s,cx,cy,cw,ch,NAVY);
    s.addShape(p.shapes.OVAL,{x:cx+0.28,y:cy+0.42,w:0.5,h:0.5,fill:{color:NAVY}});
    s.addText(it[0],{x:cx+0.28,y:cy+0.42,w:0.5,h:0.5,fontFace:HF,fontSize:20,bold:true,
      color:WHITE,align:"center",valign:"middle",margin:0});
    s.addText(it[1],{x:cx+0.95,y:cy+0.2,w:cw-1.1,h:0.4,fontFace:HF,fontSize:17,bold:true,color:NAVY,margin:0});
    s.addText(it[2],{x:cx+0.95,y:cy+0.62,w:cw-1.2,h:0.6,fontFace:BF,fontSize:12.5,color:INK,margin:0,lineSpacingMultiple:1.03});
  });
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 3 · CONTEXTO — onde a discretização entra no KDD
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Contexto · processo KDD (Fayyad, 1996) — slide Introdução 6");
  title(s,"Onde a discretização se encaixa");
  s.addText("O projeto segue o processo de Descoberta de Conhecimento em Bases de Dados (KDD). A discretização é a 7ª etapa — a ponte entre preparar os dados e minerá-los.",
    {x:0.7,y:1.75,w:12.0,h:0.7,fontFace:BF,fontSize:15,color:INK,margin:0,lineSpacingMultiple:1.12});
  const steps=[
    ["01–03","Seleção & Pré-proc.","Skip patterns, missing, outliers, imputação","done"],
    ["04","Enriquecimento","IMC e escores (fusão de atributos)","done"],
    ["05","Codificação","One-Hot dos nominais (NB03)","done"],
    ["06","DISCRETIZAÇÃO","Contínuas → faixas ordinais (NB04)","here"],
    ["07","Mineração","ML: Reg.Log., Árvore, Random Forest (NB05)","next"],
  ];
  const x0=0.7,y0=2.85,bw=2.30,gap=0.20,bh=2.2;
  steps.forEach((st,i)=>{
    const cx=x0+i*(bw+gap);
    const isHere=st[3]==="here", isNext=st[3]==="next";
    const fill=isHere?ART:(isNext?WHITE:NAVY);
    s.addShape(p.shapes.RECTANGLE,{x:cx,y:y0,w:bw,h:bh,fill:{color:fill},
      line:{color:isNext?GREY:fill,width:isNext?1:0},shadow:sh()});
    const tc=isNext?GREY:WHITE;
    s.addText(st[0],{x:cx+0.15,y:y0+0.2,w:bw-0.3,h:0.4,fontFace:HF,fontSize:19,bold:true,
      color:isHere?WHITE:(isNext?ART:GOLD),align:"center",margin:0});
    s.addText(st[1],{x:cx+0.15,y:y0+0.72,w:bw-0.3,h:0.55,fontFace:HF,fontSize:13.5,bold:true,
      color:tc,align:"center",margin:0,lineSpacingMultiple:0.95});
    s.addText(st[2],{x:cx+0.15,y:y0+1.32,w:bw-0.3,h:0.78,fontFace:BF,fontSize:11,
      color:isNext?INK:(isHere?"FBE6E3":ICE),align:"center",margin:0,lineSpacingMultiple:1.0});
    if(i<steps.length-1) s.addShape(p.shapes.LINE,{x:cx+bw+0.02,y:y0+bh/2,w:gap-0.04,h:0,
      line:{color:GREY,width:1.5,endArrowType:"triangle"}});
  });
  s.addText("Você está aqui ▲  — a discretização recebe os dados limpos do NB03 e devolve um dataset pronto para o aprendizado.",
    {x:0.7,y:5.5,w:12,h:0.5,fontFace:BF,fontSize:13,italic:true,color:ART,margin:0});
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 4 · O CONCEITO — o que é discretização
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Conceito · slide Introdução 12 (Preparação dos dados)");
  title(s,"O que é discretização?");
  s.addShape(p.shapes.RECTANGLE,{x:0.7,y:1.8,w:12.0,h:1.0,fill:{color:NAVY}});
  s.addText("“O processo de discretização transforma dados quantitativos em dados qualitativos — atributos numéricos viram atributos discretos com um número finito de intervalos.”",
    {x:1.0,y:1.9,w:11.4,h:0.8,fontFace:HF,fontSize:15,italic:true,color:WHITE,valign:"middle",margin:0,lineSpacingMultiple:1.1});
  s.addText("— definição do slide Introdução 12 do curso",{x:1.0,y:2.78,w:11,h:0.3,fontFace:BF,fontSize:11,color:GREY,margin:0});
  // mini exemplo visual antes/depois
  const [w,h]=figFit(11.4,3.0,1409/559); const x=(W-w)/2;
  s.addImage({path:FIG+"fig_exemplo_idade.png",x,y:3.25,w,h});
  s.addText("Exemplo real do projeto: a idade contínua (à esquerda) torna-se 3 faixas ordinais (à direita).",
    {x:0.7,y:3.25+h+0.12,w:12,h:0.4,fontFace:BF,fontSize:12.5,italic:true,color:GREY,align:"center",margin:0});
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 5 · POR QUE discretizar (4 motivos)
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Conceito · justificativa");
  title(s,"Por que discretizar? — 4 razões");
  const cards=[
    ["Interpretabilidade","Algoritmos caixa-branca (Árvore, Naïve Bayes) — os usados pelo orientador — geram regras mais legíveis sobre faixas do que sobre números crus.",NAVY],
    ["Redução de dimensionalidade","O slide trata a discretização como técnica de redução de dimensionalidade: menos valores distintos, espaço de busca menor.",NAVY],
    ["Suavização de outliers","Valores extremos caem dentro de uma faixa e deixam de distorcer o modelo — argumento explícito do artigo de Hipertensão (CBIS'24).",ART],
    ["Significado clínico","Faixas como as da OMS carregam sentido médico; um corte automático pela mediana (ex.: 13 anos) não teria — argumento do artigo de DPOC.",ART],
  ];
  const x0=0.7,y0=1.95,cw=5.95,ch=2.05,gx=0.4,gy=0.3;
  cards.forEach((c,i)=>{
    const cx=x0+(i%2)*(cw+gx), cy=y0+Math.floor(i/2)*(ch+gy);
    card(s,cx,cy,cw,ch,c[2]);
    s.addText(c[0],{x:cx+0.3,y:cy+0.2,w:cw-0.55,h:0.5,fontFace:HF,fontSize:17,bold:true,color:c[2],margin:0});
    s.addText(c[1],{x:cx+0.3,y:cy+0.74,w:cw-0.55,h:1.2,fontFace:BF,fontSize:13,color:INK,margin:0,lineSpacingMultiple:1.08});
  });
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 6 · TIPOS de discretização (taxonomia do slide)
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Conceito · taxonomia do slide Introdução 12");
  title(s,"Tipos de discretização — e a nossa escolha");
  const rows=[
    ["Não-supervisionada × Supervisionada","Usa ou não o rótulo da classe para definir cortes","Não-supervisionada (cortes por domínio, não pela classe)"],
    ["Univariada × Multivariada","Uma variável por vez ou várias juntas","Univariada (cada variável tratada isoladamente)"],
    ["Por largura × Por frequência","Intervalos iguais ou com nº de amostras igual","Largura por domínio + frequência (quantis) p/ escores"],
    ["Estática × Dinâmica","Antes do modelo ou embutida nele","Estática (executada antes do NB05)"],
  ];
  let y=1.95; const x=0.7, w=12.0, rh=1.0;
  rows.forEach(r=>{
    s.addShape(p.shapes.RECTANGLE,{x,y,w,h:rh,fill:{color:LIGHT},line:{color:LINEC,width:1}});
    s.addText(r[0],{x:x+0.25,y:y+0.12,w:4.3,h:rh-0.24,fontFace:HF,fontSize:13.5,bold:true,color:NAVY,valign:"middle",margin:0,lineSpacingMultiple:1.0});
    s.addText(r[1],{x:x+4.7,y:y+0.12,w:3.7,h:rh-0.24,fontFace:BF,fontSize:12,color:GREY,valign:"middle",margin:0,lineSpacingMultiple:1.0});
    s.addShape(p.shapes.RECTANGLE,{x:x+8.5,y:y+0.12,w:3.35,h:rh-0.24,fill:{color:"EAF0FB"}});
    s.addText(r[2],{x:x+8.65,y:y+0.12,w:3.1,h:rh-0.24,fontFace:BF,fontSize:11.5,bold:true,color:NAVY,valign:"middle",margin:0,lineSpacingMultiple:1.0});
    y+=rh+0.12;
  });
  s.addText("Coluna azul = a opção adotada neste trabalho, idêntica ao padrão dos 6 artigos do orientador analisados.",
    {x:0.7,y:y+0.05,w:12,h:0.4,fontFace:BF,fontSize:12.5,italic:true,color:ART,margin:0});
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 7 · O MÉTODO (padrão dos artigos) — 3 pilares
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Método · 6 artigos do LICAP (AVC, Depressão, Artrite+Dep., TOC, DPOC, HAS)");
  title(s,"Como discretizamos — o padrão do orientador");
  const pill=[
    ["FAIXAS POR DOMÍNIO","Cortes de fontes oficiais — OMS, Guia de Atividade Física BR 2021. Não-supervisionado, univariado. É a regra geral.",NAVY],
    ["QUANTIS (exceção)","Só para escores compostos sem norma externa (Escore Inflamatório/Saudável). É o equal-frequency binning do slide.",GOLD],
    ["ENTROPIA → SELEÇÃO","Entropia e correlação NÃO definem cortes; servem para selecionar/remover atributos — exatamente como nos artigos.",ART],
  ];
  const x0=0.7,y0=2.0,cw=3.95,ch=2.55,gx=0.35;
  pill.forEach((c,i)=>{ const cx=x0+i*(cw+gx);
    s.addShape(p.shapes.RECTANGLE,{x:cx,y:y0,w:cw,h:ch,fill:{color:c[2]},shadow:sh()});
    s.addText(c[0],{x:cx+0.3,y:y0+0.3,w:cw-0.6,h:0.85,fontFace:HF,fontSize:18,bold:true,color:WHITE,margin:0});
    s.addText(c[1],{x:cx+0.3,y:y0+1.2,w:cw-0.6,h:1.2,fontFace:BF,fontSize:13,color:"F0F2FA",margin:0,lineSpacingMultiple:1.1});
  });
  s.addText([{text:"Convenção ordinal CAPTO:  ",options:{bold:true,color:NAVY}},
    {text:"“risco crescente = nível maior” (0 → k). Presente em todos os artigos analisados, favorece a leitura clínica das regras.",options:{color:INK}}],
    {x:0.7,y:4.9,w:12,h:0.7,fontFace:BF,fontSize:14,italic:true,margin:0,lineSpacingMultiple:1.1});
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 8 · DECISÃO DE PIPELINE (Opção A)
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); s.background={color:LIGHT}; kicker(s,"Decisão de arquitetura");
  title(s,"Opção A — uma única fonte de discretização");
  const bx=0.7,by=2.0,bw=5.85,bh=2.7;
  s.addShape(p.shapes.RECTANGLE,{x:bx,y:by,w:bw,h:bh,fill:{color:WHITE},line:{color:"E0E0E0",width:1},shadow:sh()});
  s.addText("PROBLEMA",{x:bx+0.3,y:by+0.18,w:bw-0.6,h:0.35,fontFace:BF,fontSize:13,bold:true,color:GREY,charSpacing:2,margin:0});
  s.addText([{text:"O NB03 já categorizava (Etapa 10) e o NB04 também iria discretizar.",options:{breakLine:true,bold:true,color:INK}},
    {text:"→ discretização em DOIS lugares — o mesmo risco de inconsistência que tivemos com os outliers.",options:{color:ART,italic:true}}],
    {x:bx+0.3,y:by+0.68,w:bw-0.6,h:1.8,fontFace:BF,fontSize:14,margin:0,lineSpacingMultiple:1.18});
  const cx=bx+bw+0.5;
  s.addShape(p.shapes.RECTANGLE,{x:cx,y:by,w:bw,h:bh,fill:{color:NAVY},shadow:sh()});
  s.addText("SOLUÇÃO (Opção A)",{x:cx+0.3,y:by+0.18,w:bw-0.6,h:0.35,fontFace:BF,fontSize:13,bold:true,color:ICE,charSpacing:2,margin:0});
  s.addText([{text:"NB03 e NB03b entregam as contínuas numéricas.",options:{breakLine:true,bold:true,color:WHITE}},
    {text:"O NB04 vira o único dono da discretização — com a fonte de cada corte e relatório JSON auditável.",options:{breakLine:true,color:"E8ECF8"}},
    {text:"→ rastreável, sem duplicação, fiel ao KDD.",options:{color:"7CE0A8",italic:true,bold:true}}],
    {x:cx+0.3,y:by+0.68,w:bw-0.6,h:1.9,fontFace:BF,fontSize:14,margin:0,lineSpacingMultiple:1.18});
  s.addText("Validação: notebook executado de ponta a ponta (nbclient) — 27 células sem erro; 3 bugs encontrados e corrigidos no processo.",
    {x:0.7,y:5.0,w:12,h:0.5,fontFace:BF,fontSize:13,italic:true,color:GREY,margin:0});
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 9 · O PROCESSO — as 6 etapas do NB04
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Processo · o que o notebook executa");
  title(s,"As 6 etapas do Notebook 04");
  const steps=[
    ["1","Inventário","Classifica colunas: contínuas a discretizar × já categóricas × numéricas sem faixa"],
    ["2","Diagnóstico","Histograma de cada contínua com os cortes marcados (slide Introdução 11/12)"],
    ["3","Faixas por domínio","Aplica pd.cut com limites OMS / Guia BR — gera as colunas *_cat ordinais"],
    ["4","Quantis","pd.qcut nos escores compostos (sem norma externa)"],
    ["5","Verificação","Prevalência da classe por faixa — a faixa discrimina?"],
    ["6","Seleção & Export","Entropia+correlação sinalizam atributos; grava CSV + relatório JSON"],
  ];
  const x0=0.7,y0=1.95,cw=5.95,ch=1.35,gx=0.4,gy=0.22;
  steps.forEach((st,i)=>{
    const cx=x0+(i%2)*(cw+gx), cy=y0+Math.floor(i/2)*(ch+gy);
    card(s,cx,cy,cw,ch, i===5?ART:NAVY);
    s.addShape(p.shapes.OVAL,{x:cx+0.28,y:cy+0.45,w:0.46,h:0.46,fill:{color:i===5?ART:NAVY}});
    s.addText(st[0],{x:cx+0.28,y:cy+0.45,w:0.46,h:0.46,fontFace:HF,fontSize:18,bold:true,color:WHITE,align:"center",valign:"middle",margin:0});
    s.addText(st[1],{x:cx+0.9,y:cy+0.16,w:cw-1.1,h:0.4,fontFace:HF,fontSize:15.5,bold:true,color:NAVY,margin:0});
    s.addText(st[2],{x:cx+0.9,y:cy+0.56,w:cw-1.15,h:0.7,fontFace:BF,fontSize:11.5,color:INK,margin:0,lineSpacingMultiple:1.02});
  });
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 9B · FUNDAMENTAÇÃO TEÓRICA DE CADA ETAPA (matriz etapa → referência)
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Fundamentação · cada etapa ancorada na teoria");
  title(s,"De onde vem cada decisão da discretização");
  const hd=t=>({text:t,options:{fill:{color:NAVY},color:WHITE,bold:true,valign:"middle",fontSize:12.5}});
  const data=[
    [hd("Etapa do NB04"),hd("Referência no SLIDE"),hd("Referência nos ARTIGOS do professor")],
    ["Discretizar (transformar contínuo→faixa)","Introdução 12 — definição e tipos de discretização","Todos os 6 artigos categorizam variáveis antes do ML"],
    ["Faixas por domínio (IMC, idade)","Introdução 12 — “intervalos pré-definidos” (não-superv.)","AVC, Depressão, DPOC, Hipertensão (OMS / NLM)"],
    ["Atividade física por frequência (proxy)","Introdução 12 — intervalos pré-definidos","Inspirado em Gonçalves & Zárate (2024) — P035 em dias/sem."],
    ["Quantis nos escores (equal-frequency)","Introdução 12 — “equal-frequency binning”","Rodrigues & Zárate (2024, TOC) — discretização por percentis"],
    ["Suavização de outliers pela faixa","Introdução 14 — Análise de Outliers","Carvalho & Zárate (2024, HAS) — afirma explicitamente"],
    ["Redução de dimensionalidade","Introdução 12 — discretização reduz dimensão","Cancella & Zárate (2025) — fusão/redução de atributos"],
    ["Entropia + correlação p/ SELEÇÃO","Introdução 15 — Análise de Entropia","Gonçalves & Zárate (2024); Silva & Zárate (2024)"],
    ["Ordinal “risco crescente = nível maior”","—","Método CAPTO — Zárate et al. (2023)"],
  ];
  s.addTable(data,{x:0.7,y:1.8,w:12.0,colW:[3.7,4.0,4.3],
    rowH:[0.48,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.48],fontFace:BF,fontSize:11.5,valign:"middle",
    border:{pt:0.5,color:"D9DEEA"},fill:{color:"FBFCFE"},color:INK});
  s.addText("Nenhuma faixa foi escolhida ao acaso: cada etapa cita um slide do curso E um artigo do orientador que a respalda.",
    {x:0.7,y:6.6,w:12,h:0.4,fontFace:BF,fontSize:12,italic:true,color:ART,margin:0});
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 10 · OS DOIS DESENHOS (tabela de números reais)
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Resultados · entradas reais (saída dos NB03/NB03b)");
  title(s,"Dois desenhos de estudo discretizados");
  const hd=t=>({text:t,options:{fill:{color:NAVY},color:WHITE,bold:true,align:"center",valign:"middle"}});
  const data=[
    [{text:"",options:{fill:{color:WHITE}}},hd("Desenho 1 — Artrite pura"),hd("Desenho 2 — Artrite + comorbidades")],
    [{text:"Registros × atributos",options:{bold:true,color:INK}},"4.826 × 46","8.357 × 54"],
    [{text:"Saudáveis (0)",options:{bold:true,color:SAU}},"4.332","4.332"],
    [{text:"Com artrite (1)",options:{bold:true,color:ART}},"494","4.025"],
    [{text:"Razão de desbalanceamento",options:{bold:true,color:INK}},"8,77 : 1  (severo → exige RUS)","1,08 : 1  (quase balanceado)"],
    [{text:"Features _cat criadas",options:{bold:true,color:INK}},"5","5"],
  ];
  s.addTable(data,{x:0.7,y:1.95,w:12.0,colW:[3.6,4.2,4.2],
    rowH:[0.55,0.5,0.5,0.5,0.6,0.5],fontFace:BF,fontSize:14,valign:"middle",align:"center",
    border:{pt:0.5,color:"D9DEEA"},fill:{color:"FBFCFE"}});
  takeaway(s,"as mesmas regras de faixa (clínicas) servem aos dois desenhos. O NB04 detecta sozinho as colunas de cada um — por isso o Desenho 2 mantém as variáveis Q* (doenças) e o Desenho 1 não.",5.4);
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 11 · INVENTÁRIO (etapa 1) — o que entrou em cada grupo
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Resultado · etapa 1 — inventário das 45 features (Desenho 1)");
  title(s,"Por que apenas 5 foram discretizadas?");
  const cols=[
    ["5  ·  DISCRETIZADAS",ART,"IMC, Idade (C008), Atividade física (P035), Escore Inflamatório, Escore Saudável","As únicas contínuas COM critério de faixa — por isso só 5. Não é uma seleção."],
    ["26  ·  JÁ CATEGÓRICAS",NAVY,"Dummies One-Hot do NB03 (sexo, plano de saúde, doenças Q*, consumo de sal…)","Já são categóricas — não há o que discretizar."],
    ["14  ·  NUMÉRICAS SEM FAIXA",GOLD,"Consumos alimentares brutos (dias/sem.), peso, altura, Razão Inf/Saud…","Sem norma externa de corte (não há “OMS de dias de feijão”) → seguem numéricas."],
  ];
  const x0=0.7,y0=1.95,cw=3.95,ch=3.4,gx=0.35;
  cols.forEach((c,i)=>{ const cx=x0+i*(cw+gx);
    s.addShape(p.shapes.RECTANGLE,{x:cx,y:y0,w:cw,h:0.85,fill:{color:c[1]}});
    s.addText(c[0],{x:cx+0.2,y:y0+0.16,w:cw-0.4,h:0.55,fontFace:HF,fontSize:17,bold:true,color:WHITE,align:"center",valign:"middle",margin:0});
    s.addShape(p.shapes.RECTANGLE,{x:cx,y:y0+0.85,w:cw,h:ch-0.85,fill:{color:LIGHT},line:{color:LINEC,width:1}});
    s.addText(c[2],{x:cx+0.25,y:y0+1.05,w:cw-0.5,h:1.5,fontFace:BF,fontSize:12.5,color:INK,margin:0,lineSpacingMultiple:1.1});
    s.addText(c[3],{x:cx+0.25,y:y0+2.55,w:cw-0.5,h:0.7,fontFace:BF,fontSize:11.5,italic:true,color:GREY,margin:0,lineSpacingMultiple:1.05});
  });
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 12 · TABELA DE CORTES + FONTES (etapa 3-4)
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Resultado · etapas 3–4 — cortes aplicados");
  title(s,"Cada faixa, sua fonte e a referência teórica");
  const hd=t=>({text:t,options:{fill:{color:NAVY},color:WHITE,bold:true,valign:"middle",fontSize:12.5}});
  const ref=t=>({text:t,options:{italic:true,color:NAVY,fontSize:11}});
  const data=[
    [hd("Variável"),hd("Método"),hd("Faixas (níveis ordinais)"),hd("Fonte do corte"),hd("Referência teórica")],
    ["IMC","domínio","Baixo·Normal·Sobrep.·Obesid.","OMS — IMC adultos",ref("Carvalho & Zárate (2024); Gonçalves & Zárate (2024)")],
    ["Idade (C008)","domínio","60–69 · 70–79 · 80+","Subdiv. do idoso",ref("Melo et al. (2024, DPOC); Carvalho & Zárate (2024)")],
    ["Ativ. física (P035) ⚠️","domínio","Pouco·Moder.·Ativo (dias/sem.)","Frequência — proxy*",ref("inspirado em Gonçalves & Zárate (2024) — ver ressalva")],
    ["Escore Inflamatório","quantis","Q1 · Q2 · Q3 · Q4","Quartis da amostra",ref("equal-frequency binning — slide Introdução 12")],
    ["Escore Saudável","quantis","Q1 · Q2 · Q3 · Q4","Quartis da amostra",ref("equal-frequency binning — slide Introdução 12")],
  ];
  s.addTable(data,{x:0.7,y:1.9,w:12.0,colW:[2.05,1.25,3.0,2.0,3.7],
    rowH:[0.52,0.58,0.58,0.58,0.58,0.58],fontFace:BF,fontSize:12.5,valign:"middle",
    border:{pt:0.5,color:"D9DEEA"},fill:{color:"FBFCFE"},color:INK});
  s.addText("* P035 é medido em dias/semana (o Guia BR usa minutos); a faixa é um proxy de frequência. Além disso, P035 teve alta imputação no NB03 — ver slide de ressalvas.",
    {x:0.7,y:5.55,w:12,h:0.35,fontFace:BF,fontSize:10.5,italic:true,color:GREY,margin:0});
  takeaway(s,"IMC e idade usam faixas oficiais (OMS) — réplica direta dos artigos do orientador; os escores usam equal-frequency (slide). Já a atividade física é um proxy por frequência, citado com a devida ressalva. Cada corte é ancorado e rastreável — não arbitrário.",6.0);
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 13 · RESULTADO: IMC distribuição (figura) + leitura
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Resultado · IMC discretizado (OMS)");
  title(s,"Resultado 1 — distribuição do IMC em faixas");
  const [w,h]=figFit(11.0,3.25,1409/572); const x=(W-w)/2;
  s.addImage({path:FIG+"fig_imc_oms.png",x,y:1.85,w,h});
  takeaway(s,"Sobrepeso + Obesidade dominam os dois desenhos (D1: 2.328/4.826; D2: 4.673/8.357). A faixa da OMS preserva o sentido clínico — um corte automático pela mediana não diria nada ao médico.",5.45);
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 14 · RESULTADO: GRADIENTE DE RISCO — IMC (a leitura forte)
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Resultado · validação clínica das faixas");
  title(s,"Resultado 2 — a faixa de IMC carrega risco?");
  const [w,h]=figFit(6.8,4.2,1066/603);
  s.addImage({path:FIG+"fig_grad_imc.png",x:0.7,y:1.95,w,h});
  const lx=0.7+w+0.5, lw=W-lx-0.7;
  s.addText("Leitura do gráfico",{x:lx,y:2.05,w:lw,h:0.4,fontFace:HF,fontSize:17,bold:true,color:NAVY,margin:0});
  s.addText([
    {text:"No Desenho 2, a prevalência de artrite sobe a cada faixa de excesso de peso:",options:{breakLine:true,color:INK}},
    {text:"Normal 38%  →  Sobrepeso 50%  →  Obesidade 67%.",options:{breakLine:true,bold:true,color:ART}},
    {text:"",options:{breakLine:true,fontSize:6}},
    {text:"(A faixa “Baixo peso” foge da tendência — 41% —, mas tem só 205 pessoas, o que explica a oscilação.)",options:{breakLine:true,italic:true,color:GREY,fontSize:12}},
    {text:"",options:{breakLine:true,fontSize:6}},
    {text:"Isso é o que a literatura médica espera — a faixa da OMS, mesmo não-supervisionada, capturou um gradiente de risco real.",options:{color:INK}},
  ],{x:lx,y:2.55,w:lw,h:2.7,fontFace:BF,fontSize:13.5,margin:0,lineSpacingMultiple:1.12});
  takeaway(s,"a discretização não destruiu informação — preservou a relação dose-resposta entre obesidade e artrite. É a prova de que o corte por domínio foi uma boa escolha.",6.35);
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 15 · RESULTADO: GRADIENTE DE RISCO — IDADE
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Resultado · validação clínica das faixas");
  title(s,"Resultado 3 — a faixa etária carrega risco?");
  const [w,h]=figFit(6.8,4.2,1071/603);
  s.addImage({path:FIG+"fig_grad_idade.png",x:0.7,y:1.95,w,h});
  const lx=0.7+w+0.5, lw=W-lx-0.7;
  s.addText("Leitura do gráfico",{x:lx,y:2.05,w:lw,h:0.4,fontFace:HF,fontSize:17,bold:true,color:NAVY,margin:0});
  s.addText([
    {text:"A faixa 80+ é a de maior risco nos dois desenhos:",options:{breakLine:true,color:INK}},
    {text:"Desenho 1:  9,7% · 9,5% · 15,2%  (salto no 80+)",options:{breakLine:true,bold:true,color:NAVY}},
    {text:"Desenho 2:  43% · 54% · 57%  (crescente, +14 pp)",options:{breakLine:true,bold:true,color:ART}},
    {text:"",options:{breakLine:true,fontSize:6}},
    {text:"A subdivisão 60–69 / 70–79 / 80+ separou grupos de risco distintos dentro da própria terceira idade — algo que a idade crua não evidenciaria.",options:{color:INK}},
  ],{x:lx,y:2.55,w:lw,h:2.7,fontFace:BF,fontSize:13.5,margin:0,lineSpacingMultiple:1.12});
  takeaway(s,"discretizar o idoso em 3 faixas (em vez de manter a idade crua) revelou que o grupo 80+ é claramente o mais afetado — uma informação acionável para o artigo.",6.35);
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 16 · RESULTADO: prevalência por faixa (figura D2) — perda de informação
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Resultado · verificação de perda de informação (slide Introdução 12)");
  title(s,"Resultado 4 — as faixas discriminam a classe?");
  const [w,h]=figFit(10.6,3.6,1539/559); const x=(W-w)/2;
  s.addImage({path:FIG+"fig_prevalencia_comorb.png",x,y:1.8,w,h});
  takeaway(s,"o vermelho (artrite) cresce de forma clara nas faixas de IMC; nos escores por quartil o padrão é mais irregular (ver slide seguinte). Proporções diferentes entre níveis = faixa informativa — “reduzir a perda de informação é o objetivo da discretização” (slide).",5.5);
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 17 · RESSALVA HONESTA — Escore Inflamatório + P035 vazio
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); s.background={color:LIGHT}; kicker(s,"Resultado · análise crítica (honestidade científica)");
  title(s,"Três pontos que merecem atenção");

  card(s,0.7,1.7,12.0,1.5,GOLD,WHITE);
  s.addText("1 · Escore Inflamatório por quartis NÃO mostrou gradiente limpo",{x:1.05,y:1.85,w:11.4,h:0.4,fontFace:HF,fontSize:15,bold:true,color:GOLD,margin:0});
  s.addText([
    {text:"Prevalência por quartil = 65→56→33→37% (sem monotonia). ",options:{color:INK}},
    {text:"Por quê: ",options:{bold:true,color:INK}},
    {text:"é soma de hábitos cortada por quartis da amostra (sem norma) e seus componentes têm 57–74% de imputação no NB03. Limitação a discutir.",options:{color:INK}},
  ],{x:1.05,y:2.28,w:11.4,h:0.85,fontFace:BF,fontSize:13,margin:0,lineSpacingMultiple:1.1});

  card(s,0.7,3.35,12.0,1.5,ART,WHITE);
  s.addText("2 · Atividade física (P035): faixa por dias/semana, não pelo Guia BR",{x:1.05,y:3.5,w:11.4,h:0.4,fontFace:HF,fontSize:15,bold:true,color:ART,margin:0});
  s.addText([
    {text:"O Guia de Atividade Física BR usa minutos/semana; a PNS (P035) registra dias/semana. ",options:{color:INK}},
    {text:"Por isso a faixa é um proxy de frequência — e P035 teve 72% de imputação no NB03. Tratamos como variável de apoio, não de destaque (não aparece nos gráficos de gradiente).",options:{color:INK}},
  ],{x:1.05,y:3.93,w:11.4,h:0.85,fontFace:BF,fontSize:13,margin:0,lineSpacingMultiple:1.1});

  card(s,0.7,5.0,12.0,1.5,NAVY,WHITE);
  s.addText("3 · A faixa “Sedentário” (P035 = 0) ficou vazia",{x:1.05,y:5.15,w:11.4,h:0.4,fontFace:HF,fontSize:15,bold:true,color:NAVY,margin:0});
  s.addText([
    {text:"Ninguém caiu no nível 0. ",options:{color:INK}},
    {text:"Por quê: ",options:{bold:true,color:INK}},
    {text:"quem não pratica já saiu pelo skip pattern no NB03 (via P034); os que chegam ao NB04 têm P035 ≥ 1. Não é bug — é coerência do pipeline, mas vale registrar.",options:{color:INK}},
  ],{x:1.05,y:5.58,w:11.4,h:0.85,fontFace:BF,fontSize:13,margin:0,lineSpacingMultiple:1.1});
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 18 · ACHADO PRINCIPAL — leakage (figura grande)
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"ACHADO PRINCIPAL · slide Consequência vs. Causalidade",ART);
  title(s,"Resultado 5 — entropia + correlação revelam o leakage",ART,28);
  const [w,h]=figFit(11.6,3.5,1751/665); const x=(W-w)/2;
  s.addImage({path:FIG+"fig_leakage.png",x,y:1.85,w,h});
  s.addShape(p.shapes.RECTANGLE,{x:0.7,y:1.85+h+0.18,w:12.0,h:0.95,fill:{color:"FBEEEC"},line:{color:ART,width:1}});
  s.addText([
    {text:"Desenho 1: ",options:{bold:true,color:NAVY}},
    {text:"correlação máxima com o alvo = 0,14.   ",options:{color:INK}},
    {text:"Desenho 2: ",options:{bold:true,color:ART}},
    {text:"hipertensão (Q00201) atinge 0,70 e foi sinalizada como “alta_corr_alvo” — uma variável-consequência usada para definir o próprio controle “saudável”.",options:{color:INK}},
  ],{x:0.95,y:1.85+h+0.30,w:11.5,h:0.7,fontFace:BF,fontSize:13.5,margin:0,lineSpacingMultiple:1.12,valign:"middle"});
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 19 · O QUE O LEAKAGE SIGNIFICA (slide só de interpretação)
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Interpretação · por que o achado importa",ART);
  title(s,"O que o data leakage significa para o trabalho");
  const cards=[
    ["O problema","No Desenho 2, o controle “saudável” foi definido como quem NÃO tem nenhuma doença Q*. Logo, hipertensão (uma Q*) prediz o alvo quase trivialmente — é consequência da definição, não causa da artrite.",ART],
    ["O conceito (slide)","O slide “Consequência vs. Causalidade” alerta: usar variáveis-consequência leva a modelos “Naïve”, com acurácia inflada e sem valor explicativo real.",NAVY],
    ["A evidência","A entropia+correlação do NB04 quantificou isso: 0,70 vs. 0,14. O número confirma, empiricamente, o risco que era só teórico.",NAVY],
    ["A ação no NB05","Treinar Modelo A (com Q*) e Modelo B (sem Q*) — análise de sensibilidade. Comparar mostra quanto da performance vinha do leakage.",SAU],
  ];
  const x0=0.7,y0=1.95,cw=5.95,ch=2.05,gx=0.4,gy=0.3;
  cards.forEach((c,i)=>{ const cx=x0+(i%2)*(cw+gx), cy=y0+Math.floor(i/2)*(ch+gy);
    card(s,cx,cy,cw,ch,c[2]);
    s.addText(c[0],{x:cx+0.3,y:cy+0.18,w:cw-0.55,h:0.45,fontFace:HF,fontSize:16,bold:true,color:c[2],margin:0});
    s.addText(c[1],{x:cx+0.3,y:cy+0.68,w:cw-0.55,h:1.3,fontFace:BF,fontSize:12.5,color:INK,margin:0,lineSpacingMultiple:1.08});
  });
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 20 · ADERÊNCIA À LITERATURA
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); s.background={color:LIGHT}; kicker(s,"Validação · slides + artigos do orientador");
  title(s,"Cada decisão ancorada na literatura");
  const rows=[
    ["IMC / Idade / Ativ. física por faixa de domínio","AVC, Depressão, DPOC, HAS — todos usam OMS / Guia BR",NAVY],
    ["Discretização suaviza outliers","Artigo de Hipertensão (CBIS'24), seção de preparação",NAVY],
    ["Entropia + correlação só para selecionar atributos","AVC e Depressão — etapa “Remoção por Entropia/Correlação”",NAVY],
    ["Hipertensão = variável-consequência (leakage)","Slide Consequência vs. Causalidade + aviso do NB03b",ART],
    ["Ordinal “risco crescente = nível maior”","Método CAPTO (Zárate et al., 2023), comum a todos",NAVY],
  ];
  let y=1.95; const x=0.7,w=12.0,rh=0.84;
  rows.forEach(r=>{
    s.addShape(p.shapes.RECTANGLE,{x,y,w,h:rh,fill:{color:WHITE},line:{color:LINEC,width:1}});
    s.addShape(p.shapes.RECTANGLE,{x,y,w:0.08,h:rh,fill:{color:r[2]}});
    s.addText(r[0],{x:x+0.3,y:y+0.06,w:6.7,h:rh-0.12,fontFace:BF,fontSize:14,bold:true,color:INK,valign:"middle",margin:0});
    s.addText(r[1],{x:x+7.1,y:y+0.06,w:w-7.3,h:rh-0.12,fontFace:BF,fontSize:12.5,italic:true,color:GREY,valign:"middle",margin:0});
    y+=rh+0.12;
  });
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 20B · REFERÊNCIAS
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=slide(); kicker(s,"Referências");
  title(s,"Fundamentação teórica");
  // Coluna A — Slides do curso
  s.addText("Slides da disciplina (Prof. Zárate)",{x:0.7,y:1.8,w:5.8,h:0.4,fontFace:HF,fontSize:15,bold:true,color:GOLD,margin:0});
  s.addText([
    {text:"Introdução 6 — O Processo (KDD). Etapas de Fayyad et al. (1996).",options:{bullet:true,breakLine:true}},
    {text:"Introdução 12 — Preparação dos dados. Definição, tipos e métodos de discretização (largura, frequência, supervisionada).",options:{bullet:true,breakLine:true}},
    {text:"Introdução 14 — Análise de Outliers.",options:{bullet:true,breakLine:true}},
    {text:"Introdução 15 — Análise de Entropia (seleção de atributos).",options:{bullet:true,breakLine:true}},
    {text:"Consequência vs. Causalidade — risco de variável-consequência.",options:{bullet:true}},
  ],{x:0.7,y:2.3,w:5.85,h:3.6,fontFace:BF,fontSize:12.5,color:INK,margin:0,lineSpacingMultiple:1.12,paraSpaceAfter:10});

  // Coluna B — Artigos do professor
  s.addText("Artigos do orientador (PNS 2019)",{x:6.85,y:1.8,w:5.8,h:0.4,fontFace:HF,fontSize:15,bold:true,color:ART,margin:0});
  s.addText([
    {text:"GONÇALVES, L. F. C.; ZÁRATE, L. E. Comparação de perfis de AVC entre idosos e adultos. SBBD Companion, 2024.",options:{bullet:true,breakLine:true}},
    {text:"SILVA, P. H. R.; ZÁRATE, L. E. Caracterização da depressão em adultos no Brasil. SBBD Companion, 2024.",options:{bullet:true,breakLine:true}},
    {text:"CANCELLA, L. F. R.; ZÁRATE, L. E. Perfil Artrite-Depressão. SBBD Companion, 2025.",options:{bullet:true,breakLine:true}},
    {text:"RODRIGUES, A. P. C.; ZÁRATE, L. E. Fatores socioambientais no TOC. SBBD, 2024.",options:{bullet:true,breakLine:true}},
    {text:"MELO, R. P. N.; GOMES, M. P. S.; ZÁRATE, L. E. ML no diagnóstico de DPOC. J. Health Inform. (CBIS), 2024.",options:{bullet:true,breakLine:true}},
    {text:"CARVALHO, N. M.; GOMES, M. P. S.; ZÁRATE, L. E. Mineração no diagnóstico de hipertensão. J. Health Inform. (CBIS), 2024.",options:{bullet:true,breakLine:true}},
    {text:"ZÁRATE, L. E. et al. CAPTO — método de entendimento de domínio. Concilium, v.23, p.922–941, 2023.",options:{bullet:true}},
  ],{x:6.85,y:2.3,w:5.85,h:4.0,fontFace:BF,fontSize:11.5,color:INK,margin:0,lineSpacingMultiple:1.08,paraSpaceAfter:5});
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════
// 21 · CONCLUSÃO / PRÓXIMOS PASSOS
// ════════════════════════════════════════════════════════════════════════
(()=>{ const s=p.addSlide(); s.background={color:NAVY};
  s.addShape(p.shapes.RECTANGLE,{x:0,y:0,w:0.28,h:H,fill:{color:GOLD}});
  s.addText("SÍNTESE",{x:0.9,y:0.7,w:8,h:0.4,fontFace:BF,fontSize:13,bold:true,color:GOLD,charSpacing:3,margin:0});
  s.addText("O que a discretização entregou",{x:0.9,y:1.1,w:11.4,h:0.8,fontFace:HF,fontSize:32,bold:true,color:WHITE,margin:0});
  const pts=[
    ["2 datasets prontos para o ML","4.826×46 e 8.357×54 features. A discretização criou 5 novas variáveis categóricas ordinais (IMC, idade, ativ. física e 2 escores)."],
    ["Faixas com sentido clínico e gradiente de risco","IMC e idade confirmaram dose-resposta (obesidade 67%, 80+ 57% no Desenho 2)."],
    ["Cortes rastreáveis e citáveis","Cada faixa tem fonte (OMS / Guia BR) no JSON — base direta da seção de Métodos."],
    ["Leakage comprovado com número","Hipertensão 0,70 vs. 0,14 — sustenta a análise de sensibilidade (Modelo A vs B)."],
  ];
  let y=2.15;
  pts.forEach((t,i)=>{
    s.addShape(p.shapes.OVAL,{x:0.95,y:y+0.02,w:0.4,h:0.4,fill:{color:GOLD}});
    s.addText(String(i+1),{x:0.95,y:y+0.02,w:0.4,h:0.4,fontFace:HF,fontSize:17,bold:true,color:NAVY,align:"center",valign:"middle",margin:0});
    s.addText(t[0],{x:1.55,y:y-0.04,w:10.8,h:0.42,fontFace:HF,fontSize:17,bold:true,color:WHITE,margin:0});
    s.addText(t[1],{x:1.55,y:y+0.4,w:10.8,h:0.6,fontFace:BF,fontSize:13,color:ICE,margin:0,lineSpacingMultiple:1.08});
    y+=1.08;
  });
  s.addShape(p.shapes.RECTANGLE,{x:0.9,y:6.45,w:11.5,h:0.72,fill:{color:NAVY2}});
  s.addText([{text:"Próximo passo → NB05 (Modelagem): ",options:{bold:true,color:WHITE}},
    {text:"Reg. Logística · Árvore · Random Forest · RUS na CV · F1-macro · Modelo A (com Q*) vs B (sem Q*).",options:{color:ICE}}],
    {x:1.15,y:6.56,w:11,h:0.5,fontFace:BF,fontSize:13,valign:"middle",margin:0});
})();

p.writeFile({fileName:"Apresentacao_NB04_Discretizacao_PNS2019_FINAL.pptx"}).then(f=>{
  console.log("✅ DECK GERADO:",f);
});
