// ============================================================================
// Apresentação — Desenho 3 (intra-artrite) · Eixo nutricional sob controle
// PNS 2019 · Artrite em idosos · dados reais de data/results/preprocessing_desenho3/
// pptxgenjs
// ============================================================================
const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.layout = "LAYOUT_WIDE";                 // 13.3 x 7.5"
p.author = "Pedro Dias Soares";
p.title  = "Desenho 3 — Eixo nutricional · PNS 2019 Artrite";
const W = 13.3, H = 7.5;

// ── paleta (igual ao deck do NB04) ──────────────────────────────────────────
const NAVY="1E2761", NAVY2="2A3470", INK="2B2B2B", ICE="CADCFC", GREY="6B7280",
      ART="C0392B", SAU="27AE60", GOLD="E8A33D", LIGHT="F4F6FB", WHITE="FFFFFF",
      LINEC="E3E8F5";
const HF="Georgia", BF="Calibri";
const FIG="figuras/";
const sh=()=>({type:"outer",color:"000000",blur:7,offset:3,angle:135,opacity:0.16});

// ── helpers ─────────────────────────────────────────────────────────────────
let N=0;
function slide(){ const s=p.addSlide(); s.background={color:WHITE}; return s; }
function kicker(s,t,c=GOLD){ s.addText(t.toUpperCase(),{x:0.7,y:0.5,w:12,h:0.32,
  fontFace:BF,fontSize:12,bold:true,color:c,charSpacing:3,margin:0}); }
function title(s,t,c=NAVY,size=30,w=12.0){ s.addText(t,{x:0.7,y:0.85,w,h:0.95,
  fontFace:HF,fontSize:size,bold:true,color:c,margin:0}); }
function foot(s){ N++;
  s.addText("NB03c · Desenho 3 — PNS 2019 · Artrite em idosos ≥60",
    {x:0.7,y:H-0.42,w:9,h:0.3,fontFace:BF,fontSize:9,color:GREY,margin:0});
  s.addText(String(N),{x:W-1.0,y:H-0.42,w:0.4,h:0.3,fontFace:BF,fontSize:9,
    color:GREY,align:"right",margin:0}); }
function figFit(mw,mh,ratio){ let w=mw,h=w/ratio; if(h>mh){h=mh;w=h*ratio;} return [w,h]; }
function card(s,x,y,w,h,bar,fill=LIGHT){ s.addShape(p.shapes.RECTANGLE,{x,y,w,h,
  fill:{color:fill},line:{color:LINEC,width:1},shadow:sh()});
  s.addShape(p.shapes.RECTANGLE,{x,y,w:0.09,h,fill:{color:bar}}); }
function takeaway(s,txt,y=6.35,cor=SAU,rot="O que isso significa:  "){
  s.addShape(p.shapes.RECTANGLE,{x:0.7,y,w:11.9,h:0.78,fill:{color:"EEF6F0"},line:{color:cor,width:1}});
  s.addText([{text:rot,options:{bold:true,color:cor}},{text:txt,options:{color:INK}}],
    {x:0.95,y:y+0.04,w:11.4,h:0.7,fontFace:BF,fontSize:13,valign:"middle",margin:0,lineSpacingMultiple:1.08}); }

// ════════════════════════════════════════════════════════════════════════ 1 CAPA
(()=>{ const s=p.addSlide(); s.background={color:NAVY};
  s.addShape(p.shapes.RECTANGLE,{x:0,y:0,w:0.28,h:H,fill:{color:GOLD}});
  s.addText("MINERAÇÃO DE DADOS EM SAÚDE · PNS 2019",{x:0.9,y:1.3,w:11,h:0.4,
    fontFace:BF,fontSize:15,bold:true,color:ICE,charSpacing:4,margin:0});
  s.addText("Desenho 3 — o eixo nutricional sob controle",{x:0.9,y:1.9,w:11.7,h:1.5,
    fontFace:HF,fontSize:42,bold:true,color:WHITE,margin:0,lineSpacingMultiple:0.98});
  s.addText("Recorte intra-artrite: a dieta acompanha a carga de comorbidade?",
    {x:0.9,y:3.45,w:11.5,h:0.6,fontFace:BF,fontSize:19,color:ICE,margin:0});
  s.addText("IRNI (índice inflamatório adaptado) · controle negativo · triangulação dos três desenhos",
    {x:0.9,y:4.05,w:11.5,h:0.5,fontFace:BF,fontSize:14,italic:true,color:"AEB9D9",margin:0});
  s.addShape(p.shapes.LINE,{x:0.9,y:5.5,w:4.2,h:0,line:{color:GOLD,width:1.5}});
  s.addText([{text:"Pedro Dias Soares",options:{bold:true,color:WHITE,breakLine:true}},
    {text:"Orientador: Prof. Dr. Luis Enrique Zárate — PUC Minas (LICAP)",options:{color:ICE}}],
    {x:0.9,y:5.65,w:11,h:0.9,fontFace:BF,fontSize:14,lineSpacingMultiple:1.15,margin:0});
})();

// ════════════════════════════════════════════════════════════════════════ 2 RECAP
(()=>{ const s=slide(); kicker(s,"De onde viemos · o problema nutricional");
  title(s,"A nutrição saiu fraca nos Desenhos 1 e 2");
  card(s,0.7,1.95,5.95,2.6,SAU);
  s.addText("Desenho 1 — Artrite pura × Saudável",{x:1.0,y:2.12,w:5.4,h:0.4,fontFace:HF,fontSize:16,bold:true,color:SAU,margin:0});
  s.addText([
    {text:"Sem diferença alimentar relevante. ",options:{bold:true,color:INK,breakLine:true}},
    {text:"Dos 13 itens, só Frutas (medianas empatadas 5=5) e Feijão (1 dia) — e nenhum pró-inflamatório (refri, doces, carne) difere.",options:{color:INK}},
  ],{x:1.0,y:2.6,w:5.4,h:1.8,fontFace:BF,fontSize:13.5,margin:0,lineSpacingMultiple:1.12});
  card(s,6.95,1.95,5.95,2.6,ART);
  s.addText("Desenho 2 — Artrite+comorbidade × Saudável",{x:7.25,y:2.12,w:5.4,h:0.4,fontFace:HF,fontSize:16,bold:true,color:ART,margin:0});
  s.addText([
    {text:"Sinal forte, mas contraintuitivo. ",options:{bold:true,color:INK,breakLine:true}},
    {text:"10/13 itens significativos no sentido “mais saudável” nos artríticos (mais frutas/verduras, menos refri/carne) → causalidade reversa por manejo das comorbidades.",options:{color:INK}},
  ],{x:7.25,y:2.6,w:5.4,h:1.8,fontFace:BF,fontSize:13.5,margin:0,lineSpacingMultiple:1.12});
  s.addShape(p.shapes.RECTANGLE,{x:0.7,y:4.95,w:12.2,h:1.4,fill:{color:NAVY}});
  s.addText([{text:"A pergunta que sobra:  ",options:{bold:true,color:GOLD}},
    {text:"o sinal do D2 é causal ou é só efeito de comparar doentes com saudáveis? Para responder, é preciso ",options:{color:WHITE}},
    {text:"segurar a artrite constante",options:{bold:true,color:ICE}},
    {text:" — é isso que o Desenho 3 faz.",options:{color:WHITE}}],
    {x:1.0,y:5.12,w:11.6,h:1.05,fontFace:BF,fontSize:15,valign:"middle",margin:0,lineSpacingMultiple:1.1});
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════ 3 TRÊS DESENHOS
(()=>{ const s=slide(); kicker(s,"Estratégia · triangulação");
  title(s,"Três recortes, três confundidores diferentes");
  const cols=[
    ["DESENHO 1","Artrite pura × Saudável","Sem confundidor de comorbidade, mas reverso de artrite + n pequeno (494).",SAU],
    ["DESENHO 2","Artrite+comorb. × Saudável","Os dois confundidores juntos: artrite E comorbidade modificam a dieta.",ART],
    ["DESENHO 3","Intra-artrite (todos têm artrite)","Segura a artrite constante → isola o gradiente de comorbidade. É o foco de hoje.",NAVY],
  ];
  const x0=0.7,y0=2.0,cw=3.95,ch=3.3,gx=0.35;
  cols.forEach((c,i)=>{ const cx=x0+i*(cw+gx);
    s.addShape(p.shapes.RECTANGLE,{x:cx,y:y0,w:cw,h:0.8,fill:{color:c[3]}});
    s.addText(c[0],{x:cx+0.2,y:y0+0.16,w:cw-0.4,h:0.5,fontFace:HF,fontSize:18,bold:true,color:WHITE,align:"center",valign:"middle",margin:0});
    s.addShape(p.shapes.RECTANGLE,{x:cx,y:y0+0.8,w:cw,h:ch-0.8,fill:{color:LIGHT},line:{color:LINEC,width:1}});
    s.addText(c[1],{x:cx+0.25,y:y0+1.0,w:cw-0.5,h:0.9,fontFace:HF,fontSize:14,bold:true,color:c[3],margin:0,lineSpacingMultiple:1.0});
    s.addText(c[2],{x:cx+0.25,y:y0+1.95,w:cw-0.5,h:1.2,fontFace:BF,fontSize:13,color:INK,margin:0,lineSpacingMultiple:1.12});
  });
  takeaway(s,"se a direção do sinal nutricional for estável nos três recortes, é robustez; se mudar, aprende-se qual confundidor domina. O D3 é a peça que faltava para fechar a triangulação.",5.6,NAVY,"A lógica:  ");
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════ 4 COORTE D3
(()=>{ const s=slide(); kicker(s,"Resultado · a coorte do Desenho 3");
  title(s,"Quem entra: só idosos com artrite");
  const hd=t=>({text:t,options:{fill:{color:NAVY},color:WHITE,bold:true,align:"center",valign:"middle"}});
  const data=[
    [{text:"",options:{fill:{color:WHITE}}},hd("Alvo = 1 (tem ≥1 comorbidade)"),hd("Alvo = 0 (artrite isolada)")],
    [{text:"N",options:{bold:true,color:INK}},"3.531","494"],
    [{text:"Definição",options:{bold:true,color:INK}},"artrite + qualquer das 13 doenças Q*","artrite e nenhuma outra (= base do D1)"],
    [{text:"Proporção",options:{bold:true,color:INK}},"87,7%","12,3%  (razão 7,15 : 1)"],
  ];
  s.addTable(data,{x:0.7,y:2.0,w:12.0,colW:[2.6,4.7,4.7],rowH:[0.55,0.5,0.7,0.55],
    fontFace:BF,fontSize:14,valign:"middle",align:"center",border:{pt:0.5,color:"D9DEEA"},fill:{color:"FBFCFE"}});
  card(s,0.7,4.6,12.2,1.1,GOLD,WHITE);
  s.addText([{text:"Correção aplicada:  ",options:{bold:true,color:GOLD}},
    {text:"o alvo passou a contar as 13 comorbidades (faltavam Q088/DORT e Q128/outra crônica). Antes, 97 artríticos eram contados como “isolados” por engano (591); agora batem com os ",options:{color:INK}},
    {text:"494 canônicos",options:{bold:true,color:INK}},
    {text:" do idosos_artrite_puro.",options:{color:INK}}],
    {x:1.05,y:4.78,w:11.5,h:0.8,fontFace:BF,fontSize:13.5,valign:"middle",margin:0,lineSpacingMultiple:1.1});
  takeaway(s,"o alvo não é “tem artrite” (todos têm) — é “tem comorbidade”. Anti-leakage: as 13 doenças Q* que definem o alvo ficam fora das features. n_comorbidade é eixo de desfecho, não preditor.",5.9,NAVY,"Atenção:  ");
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════ 5 MÉTODO
(()=>{ const s=slide(); kicker(s,"Método · duas lentes para o padrão alimentar");
  title(s,"IRNI (a priori) + Cluster (a posteriori)");
  const pill=[
    ["IRNI — índice a priori","Proxy adaptado do Dietary Inflammatory Index (Shivappa, 2014). IRNI = Σ(peso × z-item) sobre 12 itens. + pró-inflamatório / − anti. Dois esquemas de peso (graded e direção) para robustez.",NAVY],
    ["CLUSTER — a posteriori","k-means nos 12 itens (z-score), k por silhueta, rótulo ordinal pelo escore pró do centróide. Captura padrões não-lineares que o IRNI (linear) não pega.",GOLD],
    ["QUADRANTE — aposentado","O antigo Padrao_Alimentar (mediana → 4 quadrantes) sai: redundante com IRNI+cluster e reintroduziria a diluição de importância.",ART],
  ];
  const x0=0.7,y0=2.0,cw=3.95,ch=2.7,gx=0.35;
  pill.forEach((c,i)=>{ const cx=x0+i*(cw+gx);
    s.addShape(p.shapes.RECTANGLE,{x:cx,y:y0,w:cw,h:ch,fill:{color:c[2]},shadow:sh()});
    s.addText(c[0],{x:cx+0.3,y:y0+0.28,w:cw-0.6,h:0.85,fontFace:HF,fontSize:16,bold:true,color:WHITE,margin:0,lineSpacingMultiple:0.97});
    s.addText(c[1],{x:cx+0.3,y:y0+1.15,w:cw-0.6,h:1.45,fontFace:BF,fontSize:12.5,color:"F0F2FA",margin:0,lineSpacingMultiple:1.08});
  });
  s.addText([{text:"Sem vazamento:  ",options:{bold:true,color:NAVY}},
    {text:"z-score do IRNI e ajuste do k-means são feitos in-fold (só no treino) no NB06; a versão da base é descritiva (alvo-cega).",options:{color:INK}}],
    {x:0.7,y:5.05,w:12,h:0.7,fontFace:BF,fontSize:13.5,italic:true,margin:0,lineSpacingMultiple:1.1});
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════ 6 A PERGUNTA
(()=>{ const s=slide(); s.background={color:LIGHT}; kicker(s,"A pergunta do Desenho 3");
  title(s,"Dose-resposta dentro da doença");
  s.addShape(p.shapes.RECTANGLE,{x:0.7,y:2.1,w:12.0,h:1.7,fill:{color:NAVY}});
  s.addText("“Entre idosos brasileiros com artrite, uma dieta mais pró-inflamatória acompanha maior carga de multimorbidade?”",
    {x:1.1,y:2.25,w:11.2,h:1.4,fontFace:HF,fontSize:19,italic:true,color:WHITE,valign:"middle",margin:0,lineSpacingMultiple:1.12});
  s.addText("É uma pergunta DIFERENTE de “dieta → artrite”: aqui todos já têm artrite. Mede-se a associação IRNI × n_comorbidades — total e, como controle, só as comorbidades NÃO-dietéticas (que não recebem orientação alimentar).",
    {x:0.7,y:4.1,w:12,h:1.0,fontFace:BF,fontSize:14.5,color:INK,margin:0,lineSpacingMultiple:1.15});
  takeaway(s,"a entrega central do D3 não é um classificador (494 é pouco e enviesado), e sim este gradiente associativo — coerente, citável e publicável por si só.",5.6,NAVY,"Escopo:  ");
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════ 7 RESULTADO 1 — GRADIENTE
(()=>{ const s=slide(); kicker(s,"Resultado 1 · entrega central",ART);
  title(s,"O gradiente IRNI × carga é nulo",ART,28);
  const [w,h]=figFit(11.8,3.4,2.908); const x=(W-w)/2;
  s.addImage({path:FIG+"etapa13_gradiente_irni_carga.png",x,y:1.8,w,h});
  s.addShape(p.shapes.RECTANGLE,{x:0.7,y:1.8+h+0.2,w:12.0,h:0.95,fill:{color:"FBEEEC"},line:{color:ART,width:1}});
  s.addText([
    {text:"Spearman IRNI × n_comorbidades:  ",options:{bold:true,color:ART}},
    {text:"rho ≈ −0,02 (graded e direção; total e não-dietética), todos com p > 0,10. ",options:{color:INK}},
    {text:"Nenhuma tendência dose-resposta.",options:{bold:true,color:INK}}],
    {x:0.95,y:1.8+h+0.33,w:11.5,h:0.7,fontFace:BF,fontSize:13.5,valign:"middle",margin:0,lineSpacingMultiple:1.1});
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════ 8 RESULTADO 2 — ROBUSTEZ
(()=>{ const s=slide(); kicker(s,"Resultado 2 · o nulo não está mascarado");
  title(s,"Robustez: três checagens, mesmo nulo");
  const cards=[
    ["(a) Contraste direto","Mann-Whitney do IRNI entre artrite pura e com comorbidade: p = 0,16 (graded) / 0,10 (direção) → ns.",NAVY],
    ["(b) Tendência por carga","IRNI médio ao longo dos níveis 0,1,2,3+ de comorbidade: sem monotonia (Spearman ns).",NAVY],
    ["(c) Por item alimentar","9/12 itens “significativos” pelo n gigante, mas |rho| < 0,07 (magnitude desprezível) e em direção REVERSA: menos doces/refri/carne com mais carga.",ART],
  ];
  const x0=0.7,y0=2.0,cw=3.95,ch=2.9,gx=0.35;
  cards.forEach((c,i)=>{ const cx=x0+i*(cw+gx);
    card(s,cx,cy(y0),cw,ch,c[2]);
    s.addText(c[0],{x:cx+0.3,y:y0+0.2,w:cw-0.55,h:0.7,fontFace:HF,fontSize:16,bold:true,color:c[2],margin:0,lineSpacingMultiple:0.97});
    s.addText(c[1],{x:cx+0.3,y:y0+0.95,w:cw-0.55,h:1.8,fontFace:BF,fontSize:12.8,color:INK,margin:0,lineSpacingMultiple:1.1});
  });
  function cy(v){return v;}
  takeaway(s,"o nulo é real, não artefato de baixa potência: nem o contraste direto, nem a tendência, nem os itens isolados mostram um gradiente pró-inflamatório → carga. O pouco que aparece é trivial e reverso.",5.45);
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════ 9 RESULTADO 3 — CONTROLE NEGATIVO
(()=>{ const s=slide(); kicker(s,"Resultado 3 · teste de falsificação");
  title(s,"Controle negativo: e se for manejo da comorbidade?");
  const [w,h]=figFit(7.4,3.5,2.512);
  s.addImage({path:FIG+"etapa13c_controle_negativo_irni.png",x:0.7,y:2.0,w,h});
  const lx=0.7+w+0.4, lw=W-lx-0.7;
  s.addText("A hipótese",{x:lx,y:2.0,w:lw,h:0.4,fontFace:HF,fontSize:16,bold:true,color:NAVY,margin:0});
  s.addText([
    {text:"Se a dieta “melhor” fosse manejo da comorbidade, o IRNI deveria cair só nos que têm comorbidade ",options:{breakLine:false,color:INK}},
    {text:"dietética",options:{italic:true,color:INK}},
    {text:" (HAS/DM/colesterol/cardíaca).",options:{breakLine:true,color:INK}},
    {text:"",options:{breakLine:true,fontSize:6}},
    {text:"A = pura (494) · B = só não-dietética (351) · C = ≥1 dietética (3.180)",options:{breakLine:true,bold:true,color:NAVY,fontSize:12}},
    {text:"",options:{breakLine:true,fontSize:6}},
    {text:"Kruskal-Wallis: p = 0,33. ",options:{bold:true,color:ART}},
    {text:"Nenhum par significativo (A vs C, o mais próximo, p = 0,15).",options:{color:INK}},
  ],{x:lx,y:2.5,w:lw,h:3.0,fontFace:BF,fontSize:13,margin:0,lineSpacingMultiple:1.12});
  takeaway(s,"a diferença alimentar do D2 NÃO é isolável como manejo dietético: dentro dos artríticos, o IRNI não muda com o tipo de comorbidade. A direção até sugere manejo (A>B>C), mas sem significância.",6.3);
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════ 10 RESULTADO 4 — CLUSTER
(()=>{ const s=slide(); kicker(s,"Resultado 4 · a segunda lente");
  title(s,"Cluster alimentar: padrões pouco nítidos");
  const [w,h]=figFit(6.6,4.0,1.697);
  s.addImage({path:FIG+"etapa13d_cluster_carga.png",x:0.7,y:2.0,w,h});
  const lx=0.7+w+0.5, lw=W-lx-0.7;
  s.addText("Leitura",{x:lx,y:2.05,w:lw,h:0.4,fontFace:HF,fontSize:16,bold:true,color:NAVY,margin:0});
  s.addText([
    {text:"k = 2 (por silhueta), mas silhueta = 0,12 — ",options:{color:INK}},
    {text:"a dieta não forma grupos nítidos",options:{bold:true,color:ART}},
    {text:" (achado em si).",options:{breakLine:true,color:INK}},
    {text:"",options:{breakLine:true,fontSize:6}},
    {text:"A carga média mal difere entre clusters (2,26 vs 2,13; p = 0,003 pelo n), e o cluster MAIS pró-inflamatório tem carga LIGEIRAMENTE menor — de novo, reverso.",options:{color:INK}},
  ],{x:lx,y:2.55,w:lw,h:2.8,fontFace:BF,fontSize:13.5,margin:0,lineSpacingMultiple:1.12});
  takeaway(s,"a lente a posteriori (cluster) concorda com a a priori (IRNI): não há padrão alimentar que concentre, de forma relevante, maior carga de comorbidade.",6.3);
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════ 11 TRIANGULAÇÃO
(()=>{ const s=slide(); kicker(s,"Síntese · triangulação dos três desenhos");
  title(s,"O sinal nutricional só aparece no D2");
  const hd=t=>({text:t,options:{fill:{color:NAVY},color:WHITE,bold:true,align:"center",valign:"middle",fontSize:12.5}});
  const data=[
    [hd("Item alimentar"),hd("D1 (puro × saud.)"),hd("D2 (comorb × saud.)"),hd("D3 (intra-artrite)")],
    ["Frutas","*** (medianas =)","***","—"],
    ["Verduras","ns","***","—"],
    ["Carne vermelha","ns","***","—"],
    ["Refrigerante","ns","***","—"],
    ["Feijão","**","***","—"],
    ["IRNI × carga / tipo / cluster","—","—","tudo ns (nulo)"],
  ];
  s.addTable(data,{x:0.7,y:1.95,w:12.0,colW:[3.6,2.8,2.8,2.8],
    rowH:[0.5,0.45,0.45,0.45,0.45,0.45,0.55],fontFace:BF,fontSize:12.5,valign:"middle",align:"center",
    border:{pt:0.5,color:"D9DEEA"},fill:{color:"FBFCFE"},color:INK});
  takeaway(s,"D1 quase sem dieta; D2 forte mas é contraste doente×saudável; D3 segura a artrite e o sinal some. Direção consistente entre os três: nada de dose-resposta intra-doença.",5.95);
  foot(s);
})();

// ════════════════════════════════════════════════════════════════════════ 12 CONCLUSÃO
(()=>{ const s=p.addSlide(); s.background={color:NAVY};
  s.addShape(p.shapes.RECTANGLE,{x:0,y:0,w:0.28,h:H,fill:{color:GOLD}});
  s.addText("SÍNTESE",{x:0.9,y:0.7,w:8,h:0.4,fontFace:BF,fontSize:13,bold:true,color:GOLD,charSpacing:3,margin:0});
  s.addText("O nulo honesto do Desenho 3",{x:0.9,y:1.1,w:11.4,h:0.8,fontFace:HF,fontSize:32,bold:true,color:WHITE,margin:0});
  const pts=[
    ["O eixo nutricional é fraco/nulo quando controlado","Gradiente IRNI×carga, contraste direto, controle negativo e cluster: todos ns no recorte intra-artrite."],
    ["O sinal do D2 é entre-grupos, não dose-resposta","A diferença alimentar do D2 vem de comparar doentes com saudáveis; some quando se segura a artrite (D3)."],
    ["Conclusão metodologicamente defensável","Mais difícil de um revisor derrubar do que afirmar “dieta causa artrite”: o trabalho mostra o limite honesto do dado transversal."],
    ["Coerente com toda a história do projeto","Causalidade reversa + alta imputação dos itens (57–74%) + corte transversal explicam o nulo."],
  ];
  let y=2.15;
  pts.forEach((t,i)=>{
    s.addShape(p.shapes.OVAL,{x:0.95,y:y+0.02,w:0.4,h:0.4,fill:{color:GOLD}});
    s.addText(String(i+1),{x:0.95,y:y+0.02,w:0.4,h:0.4,fontFace:HF,fontSize:17,bold:true,color:NAVY,align:"center",valign:"middle",margin:0});
    s.addText(t[0],{x:1.55,y:y-0.04,w:10.9,h:0.42,fontFace:HF,fontSize:16.5,bold:true,color:WHITE,margin:0});
    s.addText(t[1],{x:1.55,y:y+0.4,w:10.9,h:0.6,fontFace:BF,fontSize:12.5,color:ICE,margin:0,lineSpacingMultiple:1.06});
    y+=1.08;
  });
  s.addShape(p.shapes.RECTANGLE,{x:0.9,y:6.5,w:11.5,h:0.7,fill:{color:NAVY2}});
  s.addText([{text:"Próximo → NB06: ",options:{bold:true,color:WHITE}},
    {text:"IRNI e cluster in-fold na modelagem (D1/D2); o D3 entra como triangulação descritiva.",options:{color:ICE}}],
    {x:1.15,y:6.6,w:11,h:0.5,fontFace:BF,fontSize:13,valign:"middle",margin:0});
})();

p.writeFile({fileName:"Apresentacao_Desenho3_PNS2019.pptx"}).then(f=>{
  console.log("✅ DECK GERADO:",f);
});
