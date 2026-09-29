// build_doc.js — node _build/build_doc.js  →  dist/gstack-tutorial-5_{EN,ZH}.docx (executive memo)
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, ImageRun, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, Footer, PageNumber, LevelFormat, TableLayoutType,
} = require("docx");
const C = require("./content");

const ROOT = path.resolve(__dirname, "..");
const INK = "1B1F2A", AMBER = "E8872B", TEAL = "1F8A8A", GREY = "6B7079";
const CONTENT_W = 9638; // A4 width 11906 − 2 × 1134 margins (twips)
const PX_W = 640;

function build(lang) {
  const c = C[lang], m = c.memo, d = c.deck;
  const bodyFont = lang === "zh" ? { ascii: "Calibri", hAnsi: "Calibri", eastAsia: "Microsoft YaHei" } : "Calibri";
  const headFont = lang === "zh" ? { ascii: "Cambria", hAnsi: "Cambria", eastAsia: "Microsoft YaHei" } : "Cambria";

  const P = (text, o = {}) => new Paragraph({ spacing: { after: 120, line: 300 }, ...o.p, children: [new TextRun({ text, ...o.r })] });
  const H = (text, brk) => new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: !!brk, keepNext: true, spacing: { before: 280, after: 120 }, children: [new TextRun(text)] });
  const bullet = (text) => new Paragraph({ numbering: { reference: "bul", level: 0 }, spacing: { after: 80, line: 290 }, children: [new TextRun(text)] });
  const num = (text) => new Paragraph({ numbering: { reference: "num", level: 0 }, spacing: { after: 80, line: 290 }, children: [new TextRun(text)] });
  const image = (file, px, caption, pw) => {
    const w = pw || PX_W, h = Math.round(w * px[1] / px[0]);
    return [
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60 }, children: [new ImageRun({ type: "png", data: fs.readFileSync(path.join(ROOT, "assets", file)), transformation: { width: w, height: h }, altText: { title: caption, description: caption, name: file } })] }),
      P(caption, { p: { alignment: AlignmentType.CENTER, spacing: { after: 200 } }, r: { italics: true, size: 18, color: GREY } }),
    ];
  };
  const border = { style: BorderStyle.SINGLE, size: 4, color: "D5D8DE" };
  const borders = { top: border, bottom: border, left: border, right: border };
  const table = (headRow, rows, widths) => new Table({
    width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: widths, layout: TableLayoutType.FIXED,
    rows: [headRow].concat(rows).map((r, i) => new TableRow({
      tableHeader: i === 0,
      children: r.map((t, j) => new TableCell({
        width: { size: widths[j], type: WidthType.DXA }, borders,
        shading: { type: ShadingType.CLEAR, color: "auto", fill: i === 0 ? INK : (i % 2 ? "FFFFFF" : "F7F8FA") },
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        children: [new Paragraph({ children: [new TextRun({ text: t, bold: i === 0 || j === 0, color: i === 0 ? "FFFFFF" : INK, size: 19 })] })],
      })),
    })),
  });

  const children = [
    P(d.kicker, { r: { bold: true, color: AMBER, size: 22 }, p: { spacing: { after: 60 } } }),
    new Paragraph({ heading: HeadingLevel.TITLE, spacing: { after: 120 }, children: [new TextRun(m.title)] }),
    P(m.subtitle, { r: { size: 24, color: GREY }, p: { spacing: { after: 200 } } }),
    table([m.meta[0][0], m.meta[0][1]], m.meta.slice(1), [2200, CONTENT_W - 2200]),
    H(m.h_bottom), ...m.bottom.map(num),
    H(m.h_scope), P(m.scope),
    H(m.h_system), P(m.system), ...image(`fig_pipeline_${lang}.png`, [1768, 672], m.figPipe),
    H(m.h_setup), table(m.stepHead, m.setupSteps, [2200, CONTENT_W - 2200]),
    P(m.setupNote, { p: { spacing: { before: 120, after: 120 } }, r: { color: "C0392B", size: 20 } }),
    H(m.h_diag), P(m.diag),
    H(m.h_detour), P(m.detour),
    H(m.h_changed, true), ...image(`fig_timeline_${lang}.png`, [2168, 1016], m.figTime),
    table(m.tableHead, d.map.rows, [2200, 2100, 3238, 2100]),
    H(m.h_score), ...image(`fig_rap_${lang}.png`, [1456, 874], m.figRap, 470), P(m.score),
    H(m.h_next), ...m.next.map(bullet),
    H(m.h_risks), table(m.riskHead, m.risks, [2400, CONTENT_W - 2400]),
    H(m.h_appendix),
    ...image(`mock_03_hyperframes_${lang}.png`, [1600, 636], m.figMock),
    ...image(`mock_04_gates_${lang}.png`, [1600, 696], m.figMock2),
  ];

  const doc = new Document({
    creator: "gstack tutorial #5", title: m.title,
    styles: {
      default: { document: { run: { font: bodyFont, size: 21, color: INK } } },
      paragraphStyles: [
        { id: "Title", name: "Title", basedOn: "Normal", next: "Normal", run: { font: headFont, size: 40, bold: true, color: INK } },
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: headFont, size: 28, bold: true, color: TEAL }, paragraph: { outlineLevel: 0 } },
      ],
    },
    numbering: { config: [
      { reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
      { reference: "num", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] },
    ] },
    sections: [{
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
        new TextRun({ text: m.footer + "   ·   ", size: 16, color: GREY }),
        new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GREY }),
      ] })] }) },
      children,
    }],
  });
  const out = path.join(ROOT, "dist", `${c.file}_${lang.toUpperCase()}.docx`);
  return Packer.toBuffer(doc).then((b) => { fs.writeFileSync(out, b); return out; });
}

Promise.all(["en", "zh"].map(build)).then((f) => console.log(f.join("\n")));
