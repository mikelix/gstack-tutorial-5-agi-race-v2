// build_deck.js — node _build/build_deck.js  →  dist/gstack-tutorial-5_{EN,ZH}.pptx
const path = require("path");
const pptxgen = require("pptxgenjs");
const C = require("./content");

const ROOT = path.resolve(__dirname, "..");
const A = (f) => path.join(ROOT, "assets", f);
const INK = "1B1F2A", AMBER = "E8872B", TEAL = "1F8A8A", GREY = "6B7079", LIGHT = "EEF0F3", WHITE = "FFFFFF", RED = "C0392B";
const W = 10, M = 0.5;

function build(lang) {
  const c = C[lang], d = c.deck, F = c.font;
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.title = `${d.kicker} — ${d.title}`;
  let page = 0;

  const T = (s, text, o) => s.addText(text, Object.assign({ isTextBox: true, fontFace: F.body, color: INK, margin: 0, valign: "top" }, o));

  function content(sectionTag, title) {
    const s = pres.addSlide();
    page += 1;
    s.background = { color: WHITE };
    T(s, sectionTag, { x: M, y: 0.28, w: 6, h: 0.25, fontSize: 10, bold: true, color: AMBER, charSpacing: 1 });
    T(s, title, { x: M, y: 0.52, w: W - 2 * M, h: 0.85, fontSize: 21, bold: true, fontFace: F.head, color: INK, valign: "top" });
    T(s, d.sources, { x: M, y: 5.28, w: 6, h: 0.2, fontSize: 8, color: GREY });
    T(s, String(page), { x: W - M - 0.5, y: 5.28, w: 0.5, h: 0.2, fontSize: 8, color: GREY, align: "right" });
    return s;
  }
  const circle = (s, x, y, n, col) => {
    s.addShape(pres.shapes.OVAL, { x, y, w: 0.36, h: 0.36, fill: { color: col || AMBER }, line: { color: col || AMBER } });
    T(s, String(n), { x, y, w: 0.36, h: 0.36, fontSize: 12, bold: true, color: WHITE, align: "center", valign: "middle" });
  };
  const card = (s, x, y, w, h, fill) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: fill || LIGHT }, line: { color: fill || LIGHT } });
  const img = (s, file, x, y, maxW, maxH, px) => {
    const r = px[0] / px[1];
    let w = maxW, h = maxW / r;
    if (h > maxH) { h = maxH; w = maxH * r; }
    s.addImage({ path: A(file), x: x + (maxW - w) / 2, y, w, h });
    return h;
  };
  const tableOpts = (colW, fs) => ({ x: M, colW, fontFace: F.body, fontSize: fs || 11, color: INK, border: { type: "solid", pt: 0.5, color: "D5D8DE" }, margin: [3, 6, 3, 6], valign: "middle" });
  const head = (arr) => arr.map((t) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: INK } } }));

  // 1 — title
  {
    const s = pres.addSlide(); page += 1;
    s.background = { color: INK };
    T(s, d.kicker, { x: M, y: 0.7, w: 9, h: 0.4, fontSize: 14, bold: true, color: AMBER, charSpacing: 2 });
    T(s, d.title, { x: M, y: 1.2, w: 8.6, h: 1.5, fontSize: 34, bold: true, fontFace: F.head, color: WHITE });
    T(s, d.subtitle, { x: M, y: 2.85, w: 8.4, h: 0.8, fontSize: 15, color: "C9CDD6" });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 3.95, w: 8.6, h: 0.62, rectRadius: 0.06, fill: { color: "2A3040" }, line: { color: "2A3040" } });
    T(s, d.scope, { x: M + 0.18, y: 3.95, w: 8.3, h: 0.62, fontSize: 11, color: "E6E8EC", valign: "middle" });
    T(s, d.date, { x: M, y: 4.95, w: 4, h: 0.3, fontSize: 11, color: "9AA0AB" });
  }
  // 2 — exec summary
  {
    const s = content(lang === "en" ? "EXECUTIVE SUMMARY" : "执行摘要", d.exec.title);
    const w = (W - 2 * M - 0.6) / 3;
    d.exec.cards.forEach((k, i) => {
      const x = M + i * (w + 0.3);
      card(s, x, 1.55, w, 3.4, i === 2 ? "FDF1E6" : LIGHT);
      T(s, k.big, { x: x + 0.25, y: 1.8, w: w - 0.5, h: 0.75, fontSize: lang === "zh" ? 21 : 26, bold: true, fontFace: F.body, fit: "shrink", color: i === 2 ? AMBER : TEAL });
      T(s, k.label, { x: x + 0.25, y: 2.6, w: w - 0.5, h: 0.4, fontSize: 12, bold: true });
      T(s, k.text, { x: x + 0.25, y: 3.1, w: w - 0.5, h: 1.6, fontSize: 12.5, color: "3A3F4B" });
    });
  }
  // 3 — system
  {
    const s = content(lang === "en" ? "THE SYSTEM" : "系统", d.system.title);
    img(s, `fig_pipeline_${lang}.png`, M, 1.45, W - 2 * M, 3.3, [1768, 672]);
    T(s, d.system.takeaway, { x: M, y: 4.8, w: W - 2 * M, h: 0.35, fontSize: 12, italic: true, color: GREY });
  }
  // 4 — mental model
  {
    const s = content(lang === "en" ? "PART 0 · MENTAL MODEL" : "第 0 部分 · 心智模型", d.model.title);
    const cw = (W - 2 * M - 0.3) / 2;
    [[d.model.left, d.model.leftItems, TEAL], [d.model.right, d.model.rightItems, GREY]].forEach(([h, items, col], i) => {
      const x = M + i * (cw + 0.3);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.5, w: cw, h: 0.45, rectRadius: 0.06, fill: { color: col }, line: { color: col } });
      T(s, h, { x: x + 0.15, y: 1.5, w: cw - 0.3, h: 0.45, fontSize: 13, bold: true, color: WHITE, valign: "middle" });
      T(s, items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < items.length - 1 } })),
        { x: x + 0.1, y: 2.1, w: cw - 0.2, h: 1.9, fontSize: 13, paraSpaceAfter: 5 });
    });
    card(s, M, 4.05, W - 2 * M, 0.55, "FDF1E6");
    T(s, d.model.test, { x: M + 0.2, y: 4.05, w: W - 2 * M - 0.4, h: 0.55, fontSize: 13, bold: true, color: INK, valign: "middle" });
    T(s, d.model.note, { x: M, y: 4.75, w: W - 2 * M, h: 0.35, fontSize: 11.5, italic: true, color: GREY });
  }
  // 5 — setup
  {
    const s = content(lang === "en" ? "PART 1 · SETUP" : "第 1 部分 · 环境搭建", d.setup.title);
    const w = (W - 2 * M - 0.45) / 4;
    d.setup.steps.forEach((k, i) => {
      const x = M + i * (w + 0.15);
      card(s, x, 1.5, w, 2.85);
      circle(s, x + 0.15, 1.65, k.n, i === 1 ? AMBER : TEAL);
      T(s, k.h, { x: x + 0.6, y: 1.67, w: w - 0.7, h: 0.35, fontSize: 13, bold: true, valign: "middle" });
      T(s, k.t, { x: x + 0.15, y: 2.2, w: w - 0.3, h: 1.1, fontSize: 11.5, color: "3A3F4B" });
      s.addShape(pres.shapes.RECTANGLE, { x: x + 0.12, y: 3.4, w: w - 0.24, h: 0.8, fill: { color: "0C0C0C" }, line: { color: "0C0C0C" } });
      T(s, k.code, { x: x + 0.2, y: 3.42, w: w - 0.4, h: 0.76, fontSize: 8.5, fontFace: "Courier New", color: "61D6D6", valign: "middle" });
    });
    T(s, d.setup.pitfall, { x: M, y: 4.55, w: W - 2 * M, h: 0.55, fontSize: 11, color: RED });
  }
  // 6 — mock screenshot
  {
    const s = content(lang === "en" ? "PART 1 · SETUP" : "第 1 部分 · 环境搭建", d.shot.title);
    img(s, `mock_03_hyperframes_${lang}.png`, M, 1.4, W - 2 * M, 3.55, [1600, 636]);
    T(s, d.shot.caption, { x: M, y: 5.02, w: W - 2 * M, h: 0.25, fontSize: 9.5, italic: true, color: RED });
  }
  // 7 — diagnosis
  {
    const s = content(lang === "en" ? "PART 2 · CSR-RAP DIAGNOSIS" : "第 2 部分 · CSR-RAP 诊断", d.diag.title);
    d.diag.stats.forEach((k, i) => {
      const y = 1.5 + i * 1.12;
      T(s, k.big, { x: M, y, w: 2.6, h: 0.6, fontSize: 32, bold: true, fontFace: F.head, color: i === 2 ? AMBER : INK });
      T(s, k.label, { x: M, y: y + 0.6, w: 2.6, h: 0.4, fontSize: 11, color: GREY });
    });
    const rows = [head(d.diag.head)].concat(d.diag.rows.map((r, i) => r.map((t, j) => ({ text: t, options: { bold: i === 3 || j === 1, fill: { color: i === 3 ? "FDF1E6" : WHITE }, align: j === 1 ? "center" : "left" } }))));
    s.addTable(rows, Object.assign(tableOpts([2.1, 0.8, 3.1], 12), { x: 3.4, y: 1.55, w: 6.0, rowH: 0.62 }));
  }
  // 8 — Visual DNA
  {
    const s = content(lang === "en" ? "PART 3 · VISUAL DNA" : "第 3 部分 · 视觉 DNA", d.dna.title);
    const w = (W - 2 * M - 0.4) / 3;
    d.dna.stats.forEach((k, i) => {
      const x = M + (i % 3) * (w + 0.2), y = 1.5 + Math.floor(i / 3) * 1.65;
      card(s, x, y, w, 1.5, i === 5 ? "FDF1E6" : LIGHT);
      T(s, k.big, { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: 0.55, fontSize: lang === "zh" ? 19 : 24, bold: true, fontFace: F.body, color: i === 5 ? AMBER : TEAL });
      T(s, k.label, { x: x + 0.2, y: y + 0.75, w: w - 0.4, h: 0.7, fontSize: 11.5, color: "3A3F4B" });
    });
    T(s, d.dna.note, { x: M, y: 4.85, w: W - 2 * M, h: 0.3, fontSize: 10, italic: true, color: GREY });
  }
  // 9 — detour
  {
    const s = content(lang === "en" ? "PART 4 · THE DETOUR" : "第 4 部分 · 弯路", d.detour.title);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 1.5, w: 3.6, h: 3.5, rectRadius: 0.08, fill: { color: INK }, line: { color: INK } });
    T(s, d.detour.quote, { x: M + 0.25, y: 1.75, w: 3.1, h: 2.4, fontSize: 15, italic: true, color: WHITE, fontFace: "Cambria" });
    T(s, "— " + d.detour.quoteBy, { x: M + 0.25, y: 4.35, w: 3.1, h: 0.5, fontSize: 10.5, color: AMBER });
    d.detour.lessons.forEach((k, i) => {
      const y = 1.5 + i * 0.9;
      circle(s, 4.4, y + 0.05, i + 1, i === 3 ? RED : TEAL);
      T(s, k.h, { x: 4.9, y, w: 4.6, h: 0.3, fontSize: 13, bold: true });
      T(s, k.t, { x: 4.9, y: y + 0.32, w: 4.6, h: 0.52, fontSize: 11.5, color: "3A3F4B" });
    });
  }
  // 10 — playbook
  {
    const s = content(lang === "en" ? "PART 5 · SHOT PLAYBOOK" : "第 5 部分 · SHOT PLAYBOOK", d.playbook.title);
    const cw = (W - 2 * M - 0.4) / 2;
    d.playbook.rules.forEach((r, i) => {
      const col = i < 4 ? 0 : 1, row = i < 4 ? i : i - 4;
      const x = M + col * (cw + 0.4), y = 1.5 + row * 0.78;
      circle(s, x, y + 0.04, i + 1, i === 3 || i === 6 ? AMBER : TEAL);
      T(s, r, { x: x + 0.5, y, w: cw - 0.55, h: 0.66, fontSize: 12.5, valign: "middle" });
    });
    card(s, M + cw + 0.4, 3.9, cw, 0.95, "FDF1E6");
    T(s, d.playbook.note, { x: M + cw + 0.55, y: 3.9, w: cw - 0.3, h: 0.95, fontSize: 11, color: INK, valign: "middle" });
  }
  // 11 — brief
  {
    const s = content(lang === "en" ? "PART 6 · THE V2 BRIEF" : "第 6 部分 · V2 简报", d.brief.title);
    const cw = (W - 2 * M - 0.3) / 2;
    [[d.brief.left, d.brief.leftItems, AMBER], [d.brief.right, d.brief.rightItems, TEAL]].forEach(([h, items, col], i) => {
      const x = M + i * (cw + 0.3);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.5, w: cw, h: 0.45, rectRadius: 0.06, fill: { color: col }, line: { color: col } });
      T(s, h, { x: x + 0.15, y: 1.5, w: cw - 0.3, h: 0.45, fontSize: 13, bold: true, color: WHITE, valign: "middle" });
      card(s, x, 2.0, cw, 2.35);
      T(s, items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < items.length - 1 } })),
        { x: x + 0.15, y: 2.12, w: cw - 0.3, h: 2.15, fontSize: 12.5, paraSpaceAfter: 4 });
    });
    T(s, d.brief.foot, { x: M, y: 4.5, w: W - 2 * M, h: 0.6, fontSize: 11, color: GREY });
  }
  // 12 — timeline
  {
    const s = content(lang === "en" ? "PART 7 · V2 ANATOMY" : "第 7 部分 · V2 解剖", d.timeline.title);
    img(s, `fig_timeline_${lang}.png`, M, 1.35, W - 2 * M, 3.85, [2168, 1016]);
  }
  // 13 — improvement map
  {
    const s = content(lang === "en" ? "PART 7 · V2 ANATOMY" : "第 7 部分 · V2 解剖", d.map.title);
    const rows = [head(d.map.head)].concat(d.map.rows.map((r, i) => r.map((t, j) => ({ text: t, options: { fill: { color: i % 2 ? WHITE : "F7F8FA" }, bold: j === 3, color: j === 3 ? TEAL : INK } }))));
    s.addTable(rows, Object.assign(tableOpts([2.0, 2.0, 3.0, 2.0], 10.5), { y: 1.45, w: 9.0, rowH: 0.36 }));
  }
  // 14 — RAP
  {
    const s = content(lang === "en" ? "PART 8 · RE-SCORE" : "第 8 部分 · 重新打分", d.rap.title);
    s.addChart(pres.charts.BAR, [
      { name: "V1", labels: d.rap.cats, values: d.rap.v1 },
      { name: "V2", labels: d.rap.cats, values: d.rap.v2 },
    ], {
      x: M, y: 1.45, w: 5.4, h: 3.65, barDir: "col", barGrouping: "clustered",
      chartColors: ["9AA0AB", TEAL], showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 10, dataLabelColor: INK,
      showLegend: true, legendPos: "t", legendFontSize: 10, showTitle: true, title: d.rap.chartTitle, titleFontSize: 11, titleColor: GREY,
      valAxisHidden: true, valAxisMinVal: 0, valAxisMaxVal: 110, valGridLine: { style: "none" }, catGridLine: { style: "none" },
      catAxisLabelColor: INK, catAxisLabelFontSize: 12,
    });
    d.rap.callouts.forEach((k, i) => {
      const y = 1.5 + i * 1.2;
      card(s, 6.2, y, 3.3, 1.05, i === 2 ? "FDF1E6" : LIGHT);
      T(s, k.big, { x: 6.35, y: y + 0.1, w: 3.0, h: 0.42, fontSize: 20, bold: true, fontFace: F.head, color: i === 2 ? AMBER : TEAL });
      T(s, k.t, { x: 6.35, y: y + 0.52, w: 3.0, h: 0.5, fontSize: 10.5, color: "3A3F4B" });
    });
  }
  // 15 — measure
  {
    const s = content(lang === "en" ? "PART 9 · CLOSE THE LOOP" : "第 9 部分 · 闭环", d.measure.title);
    card(s, M, 1.45, W - 2 * M, 0.5, "FDF1E6");
    T(s, d.measure.q, { x: M + 0.2, y: 1.45, w: W - 2 * M - 0.4, h: 0.5, fontSize: 12.5, bold: true, valign: "middle" });
    const rows = [head(d.measure.head)].concat(d.measure.rows.map((r) => r.map((t, j) => ({ text: t, options: { bold: j === 0 } }))));
    s.addTable(rows, Object.assign(tableOpts([1.4, 3.8, 3.8], 11), { y: 2.1, w: 9.0, rowH: 0.48 }));
    T(s, d.measure.obs, { x: M, y: 4.35, w: W - 2 * M, h: 0.75, fontSize: 10.5, color: GREY });
  }
  // 16 — limits
  {
    const s = content(lang === "en" ? "PART 10 · LIMITS" : "第 10 部分 · 局限", d.limits.title);
    const cw = (W - 2 * M - 0.3) / 2;
    d.limits.items.forEach((k, i) => {
      const x = M + (i % 2) * (cw + 0.3), y = 1.5 + Math.floor(i / 2) * 1.75;
      card(s, x, y, cw, 1.55, i === 0 ? "FDF1E6" : LIGHT);
      circle(s, x + 0.2, y + 0.2, i + 1, i === 0 ? AMBER : GREY);
      T(s, k.h, { x: x + 0.7, y: y + 0.2, w: cw - 0.9, h: 0.36, fontSize: 14, bold: true, valign: "middle" });
      T(s, k.t, { x: x + 0.7, y: y + 0.65, w: cw - 0.9, h: 0.8, fontSize: 12, color: "3A3F4B" });
    });
  }
  // 17 — operating system
  {
    const s = content(lang === "en" ? "PART 11 · OPERATING SYSTEM" : "第 11 部分 · 操作系统", d.os.title);
    const w = (W - 2 * M - 0.4 * 2) / 3;
    d.os.steps.forEach((t, i) => {
      const x = M + (i % 3) * (w + 0.4), y = 1.5 + Math.floor(i / 3) * 1.15;
      card(s, x, y, w, 0.95, i === 7 ? "FDF1E6" : LIGHT);
      circle(s, x + 0.15, y + 0.3, i + 1, [AMBER, AMBER, TEAL, INK, INK, TEAL, AMBER, AMBER, GREY][i]);
      T(s, t, { x: x + 0.62, y, w: w - 0.72, h: 0.95, fontSize: 12.5, bold: true, valign: "middle" });
    });
  }
  // 18 — close
  {
    const s = pres.addSlide(); page += 1;
    s.background = { color: INK };
    T(s, d.close.title, { x: M, y: 1.2, w: 9, h: 0.9, fontSize: 36, bold: true, fontFace: F.head, color: WHITE });
    T(s, d.close.text, { x: M, y: 2.15, w: 8.5, h: 0.6, fontSize: 16, color: AMBER });
    T(s, d.close.links.map((t, j) => ({ text: t, options: { breakLine: j < d.close.links.length - 1 } })),
      { x: M, y: 3.3, w: 9, h: 1.3, fontSize: 12, color: "C9CDD6", paraSpaceAfter: 6 });
  }

  return pres.writeFile({ fileName: path.join(ROOT, "dist", `${c.file}_${lang.toUpperCase()}.pptx`) });
}

Promise.all(["en", "zh"].map(build)).then((f) => console.log(f.join("\n")));
