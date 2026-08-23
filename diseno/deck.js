const pptxgen = require("pptxgenjs");

// Paleta verificada por contraste WCAG. Cada par de texto supera 5:1.
const INK    = "141414",   // titulos y texto principal      18.4:1 sobre blanco
      BODY   = "3F4A46",   // texto corrido                   9.2:1 sobre blanco
      SOFT   = "646E6A",   // pies y subtitulos               5.3:1 sobre blanco
      SOFT_D = "A9B5B0",   // los mismos, sobre fondo oscuro  8.1:1
      GREEN  = "05614A",   // acento principal                7.5:1 sobre blanco
      GREEN_L= "4FC49A",   // acento sobre fondo oscuro       7.9:1
      AMBER  = "8A4A08",   // alerta                          6.9:1 sobre blanco
      DARK   = "0B1F1A",   // fondo de portada y cierre      17.1:1 con blanco
      PALE   = "E6F0EC",   // cajas con tinte
      BASE   = "5A625E",   // gris de texto recesivo          5.5:1 sobre blanco
      MARK   = "8A9490",   // serie de contexto en graficos   marca, no texto
      OFFW   = "F5F7F6",   // tarjeta recesiva
      WHITE  = "FFFFFF", LINE = "D3DAD7";
const H = "Cambria", B = "Calibri";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";                 // 13.3 x 7.5
pres.author = "Jerarquizador APP";
pres.title = "Priorización de proyectos APP del Gobierno Nacional";

const W = 13.3, HT = 7.5, M = 0.75;

function eyebrow(s, t, color) {
  s.addText(t, { x: M, y: 0.42, w: 10, h: 0.26, fontFace: B, fontSize: 11, bold: true,
                 color: color || GREEN, charSpacing: 2, margin: 0 });
}
function titulo(s, t, color) {
  s.addText(t, { x: M, y: 0.72, w: W - 2 * M, h: 0.8, fontFace: H, fontSize: 34, bold: true,
                 color: color || INK, margin: 0 });
}
function bajada(s, t, y) {
  s.addText(t, { x: M, y: y || 1.55, w: 11.2, h: 0.65, fontFace: B, fontSize: 15, color: BODY,
                 lineSpacing: 21, margin: 0 });
}
function badge(s, n, x, y, d, bg, fg) {
  s.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: bg || GREEN } });
  s.addText(String(n), { x, y, w: d, h: d, align: "center", valign: "middle",
                         fontFace: H, fontSize: d > 0.5 ? 18 : 13, bold: true, color: fg || WHITE, margin: 0 });
}
function tarjeta(s, x, y, w, h, fill) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.09,
    fill: { color: fill || WHITE }, line: { color: LINE, width: 0.75 } });
}
function pie(s, t) {
  s.addText(t, { x: M, y: HT - 0.62, w: W - 2 * M, h: 0.3, fontFace: B, fontSize: 10,
                 color: SOFT, margin: 0 });
}

/* ───────────────────────── 1. portada ───────────────────────── */
{
  const s = pres.addSlide();
  s.background = { color: DARK };
  s.addText("RESUMEN EJECUTIVO · AGOSTO 2026", { x: M, y: 1.15, w: 10, h: 0.3, fontFace: B,
    fontSize: 12, bold: true, color: GREEN_L, charSpacing: 3, margin: 0 });
  s.addText("Priorización de proyectos\nAsociación Público Privada", { x: M, y: 1.6, w: 9.4, h: 1.9,
    fontFace: H, fontSize: 44, bold: true, color: WHITE, lineSpacing: 50, margin: 0 });
  s.addText("La metodología multicriterio de la RD 002-2026-EF/68.01, aplicada al portafolio de ProInversión",
    { x: M, y: 3.55, w: 9.6, h: 0.6, fontFace: B, fontSize: 16, color: PALE, lineSpacing: 24, margin: 0 });

  const stats = [
    ["73", "proyectos evaluados", "Formulación y Estructuración"],
    ["US$ 29 057", "millones en cartera", "8 sectores"],
    ["27", "sobre la línea de corte", "US$ 8 632 MM · 30 %"],
  ];
  stats.forEach(([n, l, sub], i) => {
    const x = M + i * 3.95;
    s.addText(n, { x, y: 4.85, w: 3.6, h: 0.72, fontFace: H, fontSize: 40, bold: true,
                   color: GREEN_L, margin: 0 });
    s.addText(l, { x, y: 5.58, w: 3.6, h: 0.28, fontFace: B, fontSize: 13, bold: true,
                   color: WHITE, margin: 0 });
    s.addText(sub, { x, y: 5.86, w: 3.6, h: 0.28, fontFace: B, fontSize: 11, color: SOFT_D, margin: 0 });
  });
  s.addNotes("Resumen ejecutivo de la metodología de priorización de APP del Gobierno Nacional aprobada por el MEF en julio de 2026, aplicada a los 73 proyectos que hoy están en Formulación y Estructuración.");
}

/* ───────────────────────── 2. qué cambia ───────────────────────── */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  eyebrow(s, "EL CAMBIO");
  titulo(s, "De criterios propios a un puntaje común");
  bajada(s, "El MEF centralizó lo que antes fijaba cada entidad por separado. La priorización deja de ser una decisión discrecional y pasa a ser un cálculo reproducible.");

  const cols = [
    ["Antes", BASE, [
      "Cada entidad fijaba sus propios criterios",
      "Sin ponderaciones comparables entre proyectos",
      "Sin línea de corte explícita",
      "Sustento narrativo, difícil de auditar",
    ]],
    ["Con la RD 002-2026", GREEN, [
      "Diez indicadores con pesos fijados por norma",
      "Escala común de 0 a 1 para todo proyecto",
      "Corte en el percentil 70 de cada sector",
      "Ficha por indicador y trazabilidad de la fuente",
    ]],
  ];
  cols.forEach(([tit, color, items], i) => {
    const x = M + i * 6.15, w = 5.6;
    tarjeta(s, x, 2.35, w, 3.75, i === 1 ? WHITE : OFFW);
    s.addText(tit, { x: x + 0.4, y: 2.65, w: w - 0.8, h: 0.4, fontFace: H, fontSize: 21, bold: true,
                     color: color, margin: 0 });
    items.forEach((it, k) => {
      badge(s, "", x + 0.42, 3.32 + k * 0.66, 0.16, i === 1 ? GREEN : BASE);
      s.addText(it, { x: x + 0.75, y: 3.22 + k * 0.66, w: w - 1.2, h: 0.5, fontFace: B,
                      fontSize: 13.5, color: i === 1 ? INK : BODY, lineSpacing: 18, margin: 0 });
    });
  });
  pie(s, "Resolución Directoral N.° 002-2026-EF/68.01 · MEF, Dirección General de Política de Promoción de la Inversión Privada");
}

/* ───────────────────────── 3. dos etapas ───────────────────────── */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  eyebrow(s, "CÓMO FUNCIONA");
  titulo(s, "Dos etapas, en este orden");

  const et = [
    ["1", "Criterios de elegibilidad", "Filtro de entrada: ¿puede este proyecto desarrollarse como APP? No otorga puntaje. Se aplica según la RD 004-2016-EF/68.01.", "Los 73 proyectos del portafolio ya lo superaron."],
    ["2", "Evaluación multicriterio", "Diez indicadores con escalas propias se normalizan a 0–1 y se ponderan. El puntaje ordena los proyectos dentro de su sector.", "Es la etapa que produce la jerarquía."],
  ];
  et.forEach(([n, tit, txt, nota], i) => {
    const x = M + i * 6.15, w = 5.6;
    tarjeta(s, x, 2.05, w, 3.5, WHITE);
    badge(s, n, x + 0.4, 2.4, 0.62);
    s.addText(tit, { x: x + 1.15, y: 2.45, w: w - 1.55, h: 0.5, fontFace: H, fontSize: 20, bold: true,
                     color: INK, margin: 0 });
    s.addText(txt, { x: x + 0.4, y: 3.25, w: w - 0.8, h: 1.15, fontFace: B, fontSize: 13.5,
                     color: BODY, lineSpacing: 19, margin: 0 });
    s.addShape(pres.ShapeType.roundRect, { x: x + 0.4, y: 4.5, w: w - 0.8, h: 0.62, rectRadius: 0.06,
      fill: { color: PALE } });
    s.addText(nota, { x: x + 0.62, y: 4.5, w: w - 1.24, h: 0.62, valign: "middle", fontFace: B,
                      fontSize: 12.5, bold: true, color: GREEN, margin: 0 });
  });

  s.addShape(pres.ShapeType.rightArrow, { x: 6.42, y: 3.55, w: 0.5, h: 0.42, fill: { color: GREEN } });

  s.addText("Después del corte, y ya fuera del puntaje, operan dos restricciones: el límite de capacidad de financiamiento aprobado por el MEF y la capacidad operativa de PROINVERSIÓN.",
    { x: M, y: 5.85, w: W - 2 * M, h: 0.5, fontFace: B, fontSize: 13, italic: true, color: BODY,
      lineSpacing: 19, margin: 0 });
}

/* ───────────────────────── 4. los indicadores ───────────────────────── */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  eyebrow(s, "LOS DIEZ INDICADORES");
  titulo(s, "Ocho obligatorios pesan 85 %");
  bajada(s, "Los pesos los fijó el MEF a partir de la valoración de un grupo de expertos. Los dos indicadores opcionales se reparten el 15 % restante según la evidencia disponible.");

  const labels = ["2 · Capacidad de generar ingresos", "5 · Monto de inversión",
    "7 · Transferencia de riesgos", "4 · Población beneficiada",
    "8 · Avance de los estudios", "3 · Nivel de pobreza",
    "6 · Impulso territorial", "1 · Inclusión en el PNI"];
  const vals = [16, 12, 12, 10, 10, 9, 9, 7];

  s.addChart(pres.ChartType.bar, [{ name: "Peso", labels, values: vals }], {
    x: 0.6, y: 2.4, w: 7.9, h: 4.0,
    barDir: "bar", barGapWidthPct: 45,
    chartColors: [GREEN], showLegend: false,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0"%"',
    dataLabelFontFace: B, dataLabelFontSize: 12, dataLabelColor: INK,
    catAxisLabelFontFace: B, catAxisLabelFontSize: 12, catAxisLabelColor: BODY,
    valAxisHidden: true, valAxisMaxVal: 19,
    catGridLine: { style: "none" }, valGridLine: { style: "none" },
    catAxisLineShow: false, valAxisLineShow: false,
  });

  tarjeta(s, 8.85, 2.4, 3.7, 4.0, WHITE);
  s.addText("Bloque fijo", { x: 9.2, y: 2.7, w: 3, h: 0.3, fontFace: B, fontSize: 12, bold: true,
                             color: BODY, charSpacing: 1, margin: 0 });
  s.addText("85 %", { x: 9.2, y: 2.98, w: 3, h: 0.88, fontFace: H, fontSize: 44, bold: true,
                      color: GREEN, margin: 0 });
  s.addText("Indicadores 1 a 8. Se aplican siempre, en todo proceso de priorización sectorial.",
    { x: 9.2, y: 3.8, w: 3, h: 0.75, fontFace: B, fontSize: 12.5, color: BODY, lineSpacing: 17, margin: 0 });

  s.addText("Bloque opcional", { x: 9.2, y: 4.7, w: 3, h: 0.3, fontFace: B, fontSize: 12, bold: true,
                                 color: BODY, charSpacing: 1, margin: 0 });
  s.addText("15 %", { x: 9.2, y: 5.0, w: 3, h: 0.6, fontFace: H, fontSize: 34, bold: true,
                      color: AMBER, margin: 0 });
  s.addText("9 · Brecha de infraestructura\n10 · Declaración de viabilidad",
    { x: 9.2, y: 5.65, w: 3, h: 0.6, fontFace: B, fontSize: 12.5, color: BODY, lineSpacing: 17, margin: 0 });
  s.addNotes("El indicador 2 concentra el mayor peso individual: 16 %. Junto con el 5 y el 7, tres indicadores económico-financieros suman 40 % del puntaje.");
}

/* ───────────────────────── 5. el cálculo ───────────────────────── */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  eyebrow(s, "EL CÁLCULO");
  titulo(s, "Tres pasos por indicador");

  const pasos = [
    ["1", "Calificar", "Cada indicador tiene su escala propia según su ficha del Anexo 2: binaria para la inclusión en el PNI, 1 a 3 para la capacidad de generar ingresos, 1 a 10 para los beneficiarios."],
    ["2", "Normalizar", "El puntaje se lleva a una escala común de 0 a 1 por rango fijo. Se usa el rango teórico de la escala, no el observado, así que sumar proyectos no altera a los demás."],
    ["3", "Ponderar", "Se multiplica por el peso del indicador. El puntaje total del proyecto es la suma de todos los puntajes ponderados, entre 0 y 1."],
  ];
  pasos.forEach(([n, tit, txt], i) => {
    const x = M + i * 4.03, w = 3.65;
    tarjeta(s, x, 2.2, w, 2.85, WHITE);
    badge(s, n, x + 0.35, 2.5, 0.56);
    s.addText(tit, { x: x + 1.05, y: 2.56, w: w - 1.4, h: 0.45, fontFace: H, fontSize: 19, bold: true,
                     color: INK, margin: 0 });
    s.addText(txt, { x: x + 0.35, y: 3.28, w: w - 0.7, h: 1.5, fontFace: B, fontSize: 12.5,
                     color: BODY, lineSpacing: 18, margin: 0 });
  });

  s.addShape(pres.ShapeType.roundRect, { x: M, y: 5.4, w: W - 2 * M, h: 1.0, rectRadius: 0.09,
    fill: { color: DARK } });
  s.addText("v = (P − P mín) ÷ (P máx − P mín)", { x: M + 0.5, y: 5.4, w: 5.2, h: 1.0, valign: "middle",
    fontFace: "Courier New", fontSize: 19, bold: true, color: WHITE, margin: 0 });
  s.addText("Normalización de rango fijo: evita que un indicador medido de 1 a 10 pese más que uno medido de 1 a 3 solo por su escala.",
    { x: 6.3, y: 5.4, w: 6.2, h: 1.0, valign: "middle", fontFace: B, fontSize: 13, color: PALE,
      lineSpacing: 19, margin: 0 });
}

/* ───────────────────────── 6. dos reglas ───────────────────────── */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  eyebrow(s, "LETRA CHICA CON CONSECUENCIAS");
  titulo(s, "Dos reglas que mueven el resultado");

  const reglas = [
    ["Reponderación", "Si dentro de un sector todos los proyectos sacan el mismo valor en un indicador obligatorio, ese indicador no discrimina: se retira del cálculo y su peso se reparte entre los demás, manteniendo el bloque en 85 %.",
     "Un mismo indicador puede pesar distinto en Salud y en Transporte. En sectores con pocos proyectos llega a retirar la mitad de los indicadores."],
    ["Línea de corte P70", "Los proyectos se ordenan de mayor a menor y solo avanza el tercio superior: el percentil 70 de cada sector, calculado únicamente con los proyectos de ese sector.",
     "La norma ordena y corta por sector, no en una lista única. Con empates exactos en el valor de corte pasan todos los empatados."],
  ];
  reglas.forEach(([tit, txt, nota], i) => {
    const x = M + i * 6.15, w = 5.6;
    tarjeta(s, x, 2.1, w, 4.0, WHITE);
    s.addText(tit, { x: x + 0.4, y: 2.4, w: w - 0.8, h: 0.45, fontFace: H, fontSize: 21, bold: true,
                     color: INK, margin: 0 });
    s.addText(txt, { x: x + 0.4, y: 3.0, w: w - 0.8, h: 1.55, fontFace: B, fontSize: 13.5,
                     color: BODY, lineSpacing: 19, margin: 0 });
    s.addShape(pres.ShapeType.roundRect, { x: x + 0.4, y: 4.72, w: w - 0.8, h: 1.05, rectRadius: 0.06,
      fill: { color: PALE } });
    s.addText(nota, { x: x + 0.62, y: 4.72, w: w - 1.24, h: 1.05, valign: "middle", fontFace: B,
                      fontSize: 12.5, color: GREEN, lineSpacing: 17, margin: 0 });
  });
}

/* ───────────────────────── 7. resultado ───────────────────────── */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  eyebrow(s, "RESULTADO SOBRE EL PORTAFOLIO");
  titulo(s, "27 de 73 proyectos pasan el corte");
  bajada(s, "Aplicando la metodología a los 73 proyectos APP hoy en Formulación y Estructuración, por US$ 29 057 millones.");

  const sectores = ["Transporte", "Agua y saneam.", "Salud", "Agric. e irrig.", "Turismo",
                    "Hidrocarburos", "Educación", "Tecnología"];
  s.addChart(pres.ChartType.bar, [
    { name: "Cartera", labels: sectores, values: [27, 17, 10, 6, 5, 3, 3, 2] },
    { name: "Seleccionados", labels: sectores, values: [8, 5, 4, 2, 5, 1, 1, 1] },
  ], {
    x: 0.55, y: 2.35, w: 7.6, h: 4.05,
    barDir: "bar", barGrouping: "clustered", barGapWidthPct: 40,
    chartColors: [MARK, GREEN],
    showLegend: true, legendPos: "t", legendFontFace: B, legendFontSize: 12, legendColor: BODY,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFontFace: B, dataLabelFontSize: 10,
    dataLabelColor: BODY,
    catAxisLabelFontFace: B, catAxisLabelFontSize: 11.5, catAxisLabelColor: BODY,
    valAxisHidden: true, valAxisMaxVal: 31,
    catGridLine: { style: "none" }, valGridLine: { style: "none" },
    catAxisLineShow: false, valAxisLineShow: false,
  });

  const cifras = [
    ["US$ 8 632 MM", "inversión comprometida", "30 % del portafolio"],
    ["9", "en el PNI 2026-2031", "portafolio priorizado del DS 039-2026-EF"],
    ["8", "rankings sectoriales", "un corte P70 independiente por sector"],
  ];
  cifras.forEach(([n, l, sub], i) => {
    const y = 2.5 + i * 1.35;
    tarjeta(s, 8.5, y, 4.05, 1.15, WHITE);
    s.addText(n, { x: 8.8, y: y + 0.13, w: 3.5, h: 0.45, fontFace: H, fontSize: 24, bold: true,
                   color: GREEN, margin: 0 });
    s.addText(l, { x: 8.8, y: y + 0.6, w: 3.5, h: 0.24, fontFace: B, fontSize: 12.5, bold: true,
                   color: INK, margin: 0 });
    s.addText(sub, { x: 8.8, y: y + 0.83, w: 3.5, h: 0.24, fontFace: B, fontSize: 11, color: SOFT, margin: 0 });
  });
  s.addNotes("Turismo selecciona 5 de 5 porque cuatro teleféricos empatan exactamente en el valor de corte y la regla admite a todos los empatados.");
}

/* ───────────────────────── 8. qué decide la cartera ───────────────────────── */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  eyebrow(s, "HALLAZGO 1");
  titulo(s, "El indicador 2 decide la cartera");
  bajada(s, "Diferencia entre el valor normalizado promedio de los proyectos seleccionados y el del resto. Cuanto mayor la diferencia, más está decidiendo ese indicador.");

  const labels = ["2 · Generar ingresos", "1 · Inclusión en el PNI", "3 · Nivel de pobreza",
                  "7 · Transferencia de riesgos", "8 · Avance de estudios", "5 · Monto de inversión",
                  "4 · Población beneficiada", "6 · Impulso territorial"];
  s.addChart(pres.ChartType.bar, [{ name: "Diferencia", labels,
    values: [0.259, 0.216, 0.163, 0.130, 0.075, 0.024, 0.015, -0.140] }], {
    x: 0.6, y: 2.75, w: 7.7, h: 3.5,
    barDir: "bar", barGapWidthPct: 45,
    chartColors: [GREEN], invertedColors: [AMBER], showLegend: false,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.00",
    dataLabelFontFace: B, dataLabelFontSize: 11, dataLabelColor: INK,
    catAxisLabelFontFace: B, catAxisLabelFontSize: 11.5, catAxisLabelColor: BODY,
    valAxisHidden: true,
    catGridLine: { style: "none" }, valGridLine: { style: "none" },
    catAxisLineShow: false, valAxisLineShow: false,
  });

  tarjeta(s, 8.6, 2.75, 3.95, 3.5, WHITE);
  s.addText("Es también el dato más barato de precisar", { x: 8.95, y: 3.05, w: 3.3, h: 0.75,
    fontFace: H, fontSize: 17, bold: true, color: INK, lineSpacing: 22, margin: 0 });
  s.addText("Con 16 % de peso, la clasificación autofinanciada frente a cofinanciada es lo que más mueve el ranking.\n\n42 proyectos requieren solo revisar si el contrato prevé tarifa o peaje al usuario.\n\nEl indicador 6 sale invertido: los proyectos bajo el corte puntúan mejor en impulso territorial.",
    { x: 8.95, y: 3.9, w: 3.3, h: 2.1, fontFace: B, fontSize: 12.5, color: BODY, lineSpacing: 17, margin: 0 });
}

/* ───────────────────────── 9. concentración ───────────────────────── */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  eyebrow(s, "HALLAZGO 2");
  titulo(s, "Cortar en una sola lista concentra la cartera");
  bajada(s, "Si el presupuesto se asigna a nivel general en vez de por sector, el equilibrio intersectorial deja de estar garantizado por el método.");

  const sectores = ["Transporte", "Agua y saneam.", "Salud", "Agric. e irrig.", "Turismo",
                    "Hidrocarburos", "Educación", "Tecnología"];
  s.addChart(pres.ChartType.bar, [
    { name: "% del portafolio", labels: sectores, values: [37.0, 23.3, 13.7, 8.2, 6.8, 4.1, 4.1, 2.7] },
    { name: "% de la selección general", labels: sectores, values: [68.2, 13.6, 0, 9.1, 0, 4.5, 0, 4.5] },
  ], {
    x: 0.55, y: 2.75, w: 7.9, h: 3.5,
    barDir: "bar", barGrouping: "clustered", barGapWidthPct: 40,
    chartColors: [MARK, GREEN],
    showLegend: true, legendPos: "t", legendFontFace: B, legendFontSize: 12, legendColor: BODY,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0"%"',
    dataLabelFontFace: B, dataLabelFontSize: 10, dataLabelColor: BODY,
    catAxisLabelFontFace: B, catAxisLabelFontSize: 11.5, catAxisLabelColor: BODY,
    valAxisHidden: true, valAxisMaxVal: 82,
    catGridLine: { style: "none" }, valGridLine: { style: "none" },
    catAxisLineShow: false, valAxisLineShow: false,
  });

  s.addShape(pres.ShapeType.roundRect, { x: 8.75, y: 2.75, w: 3.8, h: 1.65, rectRadius: 0.09,
    fill: { color: DARK } });
  s.addText("18", { x: 9.1, y: 2.88, w: 3.1, h: 0.72, fontFace: H, fontSize: 38, bold: true,
                    color: AMBER, margin: 0 });
  s.addText("proyectos de Salud, Turismo y Educación: ninguno pasa el corte general",
    { x: 9.1, y: 3.55, w: 3.1, h: 0.72, fontFace: B, fontSize: 12.5, color: WHITE, lineSpacing: 17, margin: 0 });

  tarjeta(s, 8.75, 4.6, 3.8, 1.65, WHITE);
  s.addText("Es una decisión de política, no un resultado técnico. El corte sectorial de la norma existe precisamente para evitarlo.",
    { x: 9.1, y: 4.6, w: 3.1, h: 1.65, valign: "middle", fontFace: B, fontSize: 13, italic: true,
      color: BODY, lineSpacing: 18, margin: 0 });
}

/* ───────────────────────── 10. qué falta ───────────────────────── */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  eyebrow(s, "HALLAZGO 3");
  titulo(s, "La jerarquía es preliminar, y se sabe por qué");
  bajada(s, "De las 489 calificaciones aplicadas, 187 (38 %) salen de fuente oficial sin supuestos. El resto descansa en aproximaciones documentadas.");

  const grupos = [
    ["78", "Se cierran en la aplicación", "Marcar las provincias reales del proyecto (ind. 3) y la macrozona que manda cuando el ámbito abarca varias (ind. 6).", GREEN],
    ["44", "Necesitan el contrato o la ficha", "Cofinanciada total frente a parcial (ind. 2) y el monto de inversión que ProInversión no publica (ind. 5).", INK],
    ["180", "Requieren el estudio técnico", "Beneficiarios directos (ind. 4), matriz de riesgos preliminar (ind. 7) y nivel de ingeniería (ind. 8).", AMBER],
  ];
  grupos.forEach(([n, tit, txt, color], i) => {
    const x = M + i * 4.03, w = 3.65;
    tarjeta(s, x, 2.5, w, 2.85, WHITE);
    s.addText(n, { x: x + 0.35, y: 2.72, w: w - 0.7, h: 0.72, fontFace: H, fontSize: 40, bold: true,
                   color: color, margin: 0 });
    s.addText(tit, { x: x + 0.35, y: 3.48, w: w - 0.7, h: 0.5, fontFace: B, fontSize: 14, bold: true,
                     color: INK, lineSpacing: 18, margin: 0 });
    s.addText(txt, { x: x + 0.35, y: 4.02, w: w - 0.7, h: 1.1, fontFace: B, fontSize: 12.5,
                     color: BODY, lineSpacing: 17, margin: 0 });
  });

  s.addText("En los indicadores 3 y 4 falta resolución geográfica: ProInversión publica el ámbito solo a nivel departamento. En el 7 y el 8, el dato que pide la norma solo existe dentro del estudio técnico, que no es público.",
    { x: M, y: 5.65, w: W - 2 * M, h: 0.7, fontFace: B, fontSize: 13, italic: true, color: BODY,
      lineSpacing: 19, margin: 0 });
}

/* ───────────────────────── 11. cierre ───────────────────────── */
{
  const s = pres.addSlide();
  s.background = { color: DARK };
  s.addText("RECOMENDACIÓN", { x: M, y: 0.95, w: 10, h: 0.3, fontFace: B, fontSize: 12, bold: true,
    color: GREEN_L, charSpacing: 3, margin: 0 });
  s.addText("Cerrar primero lo que no depende de terceros", { x: M, y: 1.4, w: 11.8, h: 1.2,
    fontFace: H, fontSize: 36, bold: true, color: WHITE, lineSpacing: 42, margin: 0 });

  const acc = [
    ["78", "supuestos que se cierran dentro de la propia aplicación, sin pedirle nada a nadie"],
    ["42", "fichas de contrato para resolver el indicador 2, el de mayor peso y mayor poder de decisión"],
    ["6", "proyectos seleccionados sin capacidad presupuestal resuelta, que hoy no son proponibles"],
  ];
  acc.forEach(([n, txt], i) => {
    const y = 2.9 + i * 1.12;
    s.addText(n, { x: M, y, w: 1.3, h: 0.75, fontFace: H, fontSize: 34, bold: true, color: GREEN_L,
                   align: "right", margin: 0 });
    s.addText(txt, { x: M + 1.55, y: y + 0.06, w: 9.3, h: 0.7, fontFace: B, fontSize: 15, color: PALE,
                     lineSpacing: 21, margin: 0 });
  });

  s.addText("Es el 25 % de los supuestos, concentra el indicador de mayor peso y no depende de terceros. Con eso la jerarquía pasa de preliminar a defendible ante el MEF.",
    { x: M, y: 6.25, w: 11.2, h: 0.6, fontFace: B, fontSize: 14, italic: true, color: WHITE,
      lineSpacing: 20, margin: 0 });
  s.addNotes("El cierre propone una secuencia de trabajo: primero lo interno (78), luego lo contractual (42), y en paralelo resolver la capacidad presupuestal de los 6 seleccionados que no la tienen.");
}

pres.writeFile({ fileName: "Resumen_Ejecutivo_Priorizacion_APP.pptx" })
  .then(f => console.log("escrito:", f));
