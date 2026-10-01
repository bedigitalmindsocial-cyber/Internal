// Build the Yerik proposal deck (.pptx) from work/deck-content.yaml.
//
//   npm run deck      (or: node scripts/build_pptx.js)
//
// While any [[PRICE]] or [[CONFIRM...]] remains, writes output/Yerik_Proposal_DRAFT.pptx
// with a DRAFT watermark on every slide. With none left, writes output/Yerik_Proposal_v1.pptx.
// Screenshots are picked up from work/screenshots/annotated/, work/screenshots/raw/ or
// inputs/manual-screenshots/ (name.jpg/.png/.webp). Missing ones become grey boxes.
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const pptxgen = require('pptxgenjs');

const ROOT = path.resolve(__dirname, '..');
const content = yaml.load(fs.readFileSync(path.join(ROOT, 'work/deck-content.yaml'), 'utf8'));

// ---------- theme (brief section 10) ----------
const C = {
  paper: 'FAF9FC', ink: '0F0A1A', primary: '4B2F79', deep: '2A1D4B', steel: '6B6478',
  rule: 'DDD8E8', p10: 'EDEAF1', p20: 'DBD5E4', white: 'FFFFFF', orange: 'E8772E',
};
// Fallbacks for Coolvetica / PP Editorial New / Neue Montreal (see TODO_before_sending.md)
const F = { display: 'Cambria', title: 'Cambria', body: 'Calibri' };
const W = 13.333, H = 7.5, MX = 0.6;

// ---------- template fill + placeholders ----------
const lookup = (ref) => ref.split('.').reduce((o, k) => (o == null ? o : o[k]), content);
const fill = (s) => String(s ?? '').replace(/\{([a-z_.0-9A-Z]+)\}/g, (m, ref) => (lookup(ref) ?? m));
const PH = /(\[\[[^\]]*\]\])/;
let placeholderCount = 0;
const scan = (n) => {
  if (typeof n === 'string') placeholderCount += (fill(n).match(/\[\[[^\]]*\]\]/g) || []).length;
  else if (Array.isArray(n)) n.forEach(scan);
  else if (n && typeof n === 'object') Object.entries(n).forEach(([k, v]) => k !== 'prices' && scan(v));
};
scan(content.slides);
scan(content.meta);
const DRAFT = placeholderCount > 0;
// NO_WATERMARK=1: clean editable copy (e.g. for Canva), placeholders stay highlighted
const NO_WATERMARK = process.env.NO_WATERMARK === '1';

// Split text into runs; placeholders get a lilac highlight so they are easy to spot.
function runs(text, opts = {}) {
  return fill(text).split(PH).filter(Boolean).map((t) => {
    const ph = PH.test(t);
    return { text: t, options: { ...opts, ...(ph ? { highlight: C.p20, color: C.primary, bold: true } : {}) } };
  });
}
function bulletLines(lines, opts = {}) {
  return lines.flatMap((l, li) => {
    // one run per bullet: split runs would start new, bullet-less paragraphs
    return [{ text: fill(l), options: { ...opts, bullet: { indent: 14 }, ...(li < lines.length - 1 ? { breakLine: true } : {}) } }];
  });
}
function para(lines, opts = {}, between = 6) {
  const out = [];
  lines.forEach((l, i) => {
    const r = runs(l, opts);
    if (i < lines.length - 1) r[r.length - 1].options = { ...r[r.length - 1].options, breakLine: true, paraSpaceAfter: between };
    out.push(...r);
  });
  return out;
}

// ---------- screenshots ----------
const SHOT_DIRS = ['work/screenshots/annotated', 'work/screenshots/raw', 'inputs/manual-screenshots'];
const SHOT_INFO = {
  '01_home_desktop': 'Homepage, first screen, 1440×900',
  '02_home_mobile': 'Homepage on a phone, 390×844, first 2 screens',
  '03_phone_number': 'Tight crop of the phone number',
  '04_product_page': 'Product page with the “tweet” label',
  '05_careers_form': 'Careers form filled (Test / abc / blank phone), not submitted',
  '06_competitor_jrs': 'JRS Farm Parts homepage, first screen',
  '07_competitor_machineparts': 'Machine Parts homepage, first screen',
  '08_google_profile': 'Google profile with unrelated photos (manual)',
  '09_linkedin_pages': 'Both LinkedIn pages named Yerik International (manual)',
  '10_hiring_post': 'One off-brand hiring post (manual, blur people)',
};
const missingShots = new Set();
function findShot(name) {
  for (const d of SHOT_DIRS) for (const ext of ['.jpg', '.jpeg', '.png', '.webp']) {
    const p = path.join(ROOT, d, name + ext);
    if (fs.existsSync(p)) return p;
  }
  return null;
}
function shot(slide, name, x, y, w, h) {
  const p = findShot(name);
  if (p) {
    slide.addShape('rect', { x, y, w, h, fill: { color: C.white }, line: { color: C.rule, width: 1 } });
    slide.addImage({ path: p, x: x + 0.05, y: y + 0.05, w: w - 0.1, h: h - 0.1, sizing: { type: 'contain', w: w - 0.1, h: h - 0.1 } });
    return;
  }
  missingShots.add(name);
  slide.addShape('rect', { x, y, w, h, fill: { color: C.p10 }, line: { color: C.p20, width: 1.25, dashType: 'dash' } });
  slide.addText([
    { text: 'Screenshot needed', options: { bold: true, color: C.steel, fontSize: 14, breakLine: true } },
    { text: `${name}: ${SHOT_INFO[name] || ''}`, options: { color: C.steel, fontSize: 12 } },
  ], { x: x + 0.2, y, w: w - 0.4, h, align: 'center', valign: 'middle', fontFace: F.body, isTextBox: true });
}

// ---------- shared furniture ----------
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.title = 'Yerik International: 30-day proposal';
pres.company = 'Giraffe Partners';

let pageNo = 0;
function base(dark = false) {
  pageNo += 1;
  const s = pres.addSlide();
  s.background = { color: dark ? C.deep : C.paper };
  return s;
}
function footer(s, dark = false) {
  s.addText(`${content.meta.footer} · ${pageNo}`, {
    x: MX, y: H - 0.5, w: W - 2 * MX, h: 0.3, fontFace: F.body, fontSize: 10,
    color: dark ? C.p20 : C.steel, margin: 0, isTextBox: true,
  });
}
function watermark(s) {
  if (!DRAFT || NO_WATERMARK) return;
  s.addText('DRAFT', {
    x: 2.2, y: 2.2, w: 9, h: 3, rotate: -28, align: 'center', valign: 'middle',
    fontFace: F.body, fontSize: 150, bold: true, color: C.primary, transparency: 90, isTextBox: true,
  });
}
function title(s, text, opts = {}) {
  s.addText(runs(text), {
    x: MX, y: opts.y ?? 0.45, w: opts.w ?? W - 2 * MX, h: opts.h ?? 1.0, fontFace: F.title, fontSize: opts.size ?? 32,
    bold: true, color: opts.color ?? C.primary, valign: 'top', margin: 0, isTextBox: true,
  });
}
function numCircle(s, n, x, y, d = 0.42, fillC = C.primary, txt = C.white, size = 14) {
  s.addShape('ellipse', { x, y, w: d, h: d, fill: { color: fillC }, line: { color: fillC } });
  s.addText(String(n), { x, y, w: d, h: d, align: 'center', valign: 'middle', fontFace: F.body, fontSize: size, bold: true, color: txt, margin: 0, isTextBox: true });
}
function callouts(s, items, x, y, w, size = 17, gap = 0.95) {
  items.forEach((c, i) => {
    numCircle(s, i + 1, x, y + i * gap);
    s.addText(runs(c), { x: x + 0.6, y: y + i * gap - 0.04, w: w - 0.6, h: gap - 0.1, fontFace: F.body, fontSize: size, color: C.ink, valign: 'top', margin: 0, isTextBox: true });
  });
}
function card(s, x, y, w, h, color = C.p10) {
  s.addShape('rect', { x, y, w, h, fill: { color }, line: { color } });
}

// ---------- slide renderers ----------
const R = {
  cover(d) {
    const s = base(true);
    s.addText('GIRAFFE PARTNERS', { x: MX, y: 0.6, w: 6, h: 0.4, fontFace: F.body, fontSize: 14, bold: true, charSpacing: 4, color: C.p20, margin: 0, isTextBox: true });
    s.addText('30', { x: 8.3, y: 0.9, w: 4.6, h: 3.6, fontFace: F.display, fontSize: 250, bold: true, color: C.primary, align: 'right', valign: 'middle', margin: 0, isTextBox: true });
    s.addText('days', { x: 8.3, y: 4.25, w: 4.45, h: 0.6, fontFace: F.title, fontSize: 28, italic: true, color: C.p20, align: 'right', margin: 0, isTextBox: true });
    s.addText(runs(d.title), { x: MX, y: 2.0, w: 7.8, h: 2.2, fontFace: F.title, fontSize: 46, bold: true, color: C.white, valign: 'bottom', margin: 0, isTextBox: true });
    s.addText(runs(d.subtitle), { x: MX, y: 4.35, w: 7.8, h: 0.9, fontFace: F.body, fontSize: 24, color: C.p20, valign: 'top', margin: 0, isTextBox: true });
    s.addText(runs(d.byline), { x: MX, y: 6.3, w: 12, h: 0.45, fontFace: F.body, fontSize: 15, color: C.p20, margin: 0, isTextBox: true });
    watermark(s);
  },

  points(d) {
    const s = base();
    s.addText(d.kicker.toUpperCase(), { x: MX, y: 0.45, w: 8, h: 0.3, fontFace: F.body, fontSize: 13, bold: true, charSpacing: 3, color: C.steel, margin: 0, isTextBox: true });
    title(s, d.title, { y: 0.8 });
    const cw = 5.9, ch = 1.55;
    d.points.forEach((p, i) => {
      const x = MX + (i % 2) * (cw + 0.33), y = 2.05 + Math.floor(i / 2) * (ch + 0.3);
      card(s, x, y, cw, ch);
      numCircle(s, i + 1, x + 0.3, y + 0.3, 0.5, C.primary, C.white, 16);
      s.addText(runs(p), { x: x + 1.05, y: y + 0.2, w: cw - 1.3, h: ch - 0.4, fontFace: F.body, fontSize: 22, color: C.ink, valign: 'middle', margin: 0, isTextBox: true });
    });
    card(s, MX, 5.75, W - 2 * MX, 0.95, C.deep);
    s.addText(runs(d.closing), { x: MX + 0.35, y: 5.75, w: W - 2 * MX - 0.7, h: 0.95, fontFace: F.title, fontSize: 24, bold: true, color: C.white, valign: 'middle', margin: 0, isTextBox: true });
    footer(s); watermark(s);
  },

  screenshot(d) {
    const s = base();
    title(s, d.title);
    if (d.image === '02_home_mobile') {
      shot(s, d.image, MX + 0.4, 1.55, 2.55, 5.25);
      let y = 1.7;
      if (d.body) {
        s.addText(runs(d.body), { x: 4.4, y, w: 8.3, h: 1.2, fontFace: F.body, fontSize: 20, color: C.ink, valign: 'top', margin: 0, isTextBox: true });
        y += 1.6;
      }
      callouts(s, d.callouts, 4.4, y, 8.3, 18);
    } else {
      shot(s, d.image, MX, 1.55, 8.4, 5.25);
      callouts(s, d.callouts, 9.4, 1.75, 3.35, 18, 1.1);
    }
    footer(s); watermark(s);
  },

  panels4(d) {
    const s = base();
    title(s, d.title);
    const pw = 5.9, ih = 1.85;
    d.panels.forEach((p, i) => {
      const x = MX + (i % 2) * (pw + 0.33), y = 1.5 + Math.floor(i / 2) * 2.7;
      numCircle(s, i + 1, x, y + 0.02, 0.36, C.primary, C.white, 12);
      if (p.text_card) {
        card(s, x + 0.5, y, pw - 0.5, ih, C.white);
        s.addShape('rect', { x: x + 0.5, y, w: pw - 0.5, h: ih, fill: { color: C.white }, line: { color: C.rule, width: 1 } });
        s.addText(runs(p.text_card), { x: x + 0.75, y, w: pw - 1.0, h: ih, fontFace: F.title, fontSize: 18, italic: true, color: C.ink, valign: 'middle', margin: 0, isTextBox: true });
      } else {
        shot(s, p.image, x + 0.5, y, pw - 0.5, ih);
      }
      if (p.caption) s.addText(runs(p.caption), { x: x + 0.5, y: y + ih + 0.1, w: pw - 0.5, h: 0.55, fontFace: F.body, fontSize: 16, color: C.ink, valign: 'top', margin: 0, isTextBox: true });
    });
    footer(s); watermark(s);
  },

  panels3(d, labelled = false) {
    const s = base();
    title(s, d.title);
    const pw = 3.85, gap = (W - 2 * MX - 3 * pw) / 2;
    d.panels.forEach((p, i) => {
      const x = MX + i * (pw + gap);
      let y = 1.55;
      if (labelled) {
        s.addText(p.label, { x, y, w: pw, h: 0.4, fontFace: F.body, fontSize: 16, bold: true, color: p.label === content.meta.client ? C.primary : C.steel, margin: 0, isTextBox: true });
        y += 0.5;
      } else {
        numCircle(s, i + 1, x, y, 0.36, C.primary, C.white, 12);
        y += 0.5;
      }
      shot(s, p.image, x, y, pw, labelled ? 3.5 : 3.3);
      s.addText(runs(p.caption), { x, y: y + (labelled ? 3.65 : 3.45), w: pw, h: 1.1, fontFace: F.body, fontSize: 16, color: C.ink, valign: 'top', margin: 0, isTextBox: true });
    });
    footer(s); watermark(s);
  },
  compare3(d) { R.panels3(d, true); },

  bignumber(d) {
    const s = base();
    title(s, d.title, { w: 11.5 });
    s.addText(d.number, { x: MX, y: 2.2, w: 6.6, h: 2.0, fontFace: F.display, fontSize: 100, bold: true, color: C.primary, valign: 'middle', margin: 0, isTextBox: true });
    s.addText(d.number_label, { x: MX, y: 4.25, w: 6.4, h: 0.5, fontFace: F.body, fontSize: 18, color: C.steel, margin: 0, isTextBox: true });
    s.addShape('line', { x: 7.5, y: 2.3, w: 0, h: 3.0, line: { color: C.rule, width: 1 } });
    s.addText(runs(d.body), { x: 7.9, y: 2.3, w: 4.8, h: 3.0, fontFace: F.body, fontSize: 24, color: C.ink, valign: 'middle', margin: 0, isTextBox: true });
    footer(s); watermark(s);
  },

  plan(d) {
    const s = base();
    title(s, d.title);
    const cw = 2.85, gap = (W - 2 * MX - 4 * cw) / 3;
    d.core.forEach((c, i) => {
      const x = MX + i * (cw + gap), y = 1.5;
      card(s, x, y, cw, 2.55);
      numCircle(s, c.code, x + 0.25, y + 0.25, 0.6, C.primary, C.white, 22);
      s.addText(c.name, { x: x + 0.25, y: y + 1.0, w: cw - 0.5, h: 0.5, fontFace: F.body, fontSize: 18, bold: true, color: C.ink, valign: 'top', margin: 0, isTextBox: true });
      s.addText(runs(c.line), { x: x + 0.25, y: y + 1.5, w: cw - 0.5, h: 0.95, fontFace: F.body, fontSize: 15, color: C.ink, valign: 'top', margin: 0, isTextBox: true });
    });
    s.addText('OPTIONAL', { x: MX, y: 4.3, w: 4, h: 0.3, fontFace: F.body, fontSize: 12, bold: true, charSpacing: 3, color: C.steel, margin: 0, isTextBox: true });
    const ow = (W - 2 * MX - 0.33) / 2;
    d.options.forEach((o, i) => {
      const x = MX + i * (ow + 0.33), y = 4.65;
      s.addShape('rect', { x, y, w: ow, h: 1.0, fill: { color: C.white }, line: { color: C.rule, width: 1 } });
      numCircle(s, o.code, x + 0.25, y + 0.25, 0.5, C.p20, C.primary, 18);
      s.addText([
        { text: o.name.replace(' (optional)', ''), options: { bold: true, breakLine: true } },
        ...runs(o.line),
      ], { x: x + 0.95, y, w: ow - 1.15, h: 1.0, fontFace: F.body, fontSize: 15, color: C.ink, valign: 'middle', margin: 0, isTextBox: true });
    });
    card(s, MX, 5.95, W - 2 * MX, 0.6, C.p10);
    s.addText(runs(d.not_included), { x: MX + 0.25, y: 5.95, w: W - 2 * MX - 0.5, h: 0.6, fontFace: F.body, fontSize: 15, color: C.steel, valign: 'middle', margin: 0, isTextBox: true });
    footer(s); watermark(s);
  },

  sitemaps(d) {
    const s = base();
    title(s, d.title);
    const pw = 5.9;
    [d.left, d.right].forEach((side, si) => {
      const x = MX + si * (pw + 0.33);
      s.addText(side.label.toUpperCase(), { x, y: 1.35, w: pw, h: 0.3, fontFace: F.body, fontSize: 12, bold: true, charSpacing: 3, color: si ? C.primary : C.steel, margin: 0, isTextBox: true });
      card(s, x, 1.75, pw, 0.5, si ? C.primary : C.steel);
      s.addText(runs(side.root), { x: x + 0.2, y: 1.75, w: pw - 0.4, h: 0.5, fontFace: F.body, fontSize: 14, bold: true, color: C.white, valign: 'middle', margin: 0, isTextBox: true });
      const rowH = 0.66, top = 2.45;
      s.addShape('line', { x: x + 0.25, y: 2.25, w: 0, h: top + (side.rows.length - 1) * rowH + rowH / 2 - 2.25, line: { color: C.rule, width: 1.25 } });
      side.rows.forEach((r, i) => {
        const y = top + i * rowH;
        s.addShape('line', { x: x + 0.25, y: y + rowH / 2, w: 0.25, h: 0, line: { color: C.rule, width: 1.25 } });
        s.addShape('rect', { x: x + 0.5, y: y + 0.04, w: pw - 0.5, h: rowH - 0.08, fill: { color: si ? C.p10 : C.white }, line: { color: C.rule, width: 0.75 } });
        const marks = r.marks || [];
        const textW = pw - 0.75 - marks.length * 0.32;
        s.addText([
          { text: r.page, options: { bold: true, fontSize: 14, breakLine: true } },
          ...runs(r.sub, { fontSize: 12, color: C.steel }),
        ], { x: x + 0.65, y: y + 0.04, w: textW, h: rowH - 0.08, fontFace: F.body, color: C.ink, valign: 'middle', margin: 0, isTextBox: true });
        marks.forEach((m, mi) => numCircle(s, m, x + pw - 0.15 - (marks.length - mi) * 0.32, y + rowH / 2 - 0.14, 0.28, C.primary, C.white, 10));
      });
      const below = top + side.rows.length * rowH + 0.15;
      if (side.legend) {
        side.legend.forEach((l, i) => {
          const lx = x + (i % 2) * (pw / 2), ly = below + Math.floor(i / 2) * 0.33;
          numCircle(s, i + 1, lx, ly + 0.02, 0.24, C.primary, C.white, 9);
          s.addText(runs(l), { x: lx + 0.32, y: ly, w: pw / 2 - 0.4, h: 0.3, fontFace: F.body, fontSize: 12, color: C.steel, valign: 'middle', margin: 0, isTextBox: true });
        });
      }
      if (side.footnote) s.addText(runs(side.footnote), { x, y: below, w: pw, h: 0.6, fontFace: F.body, fontSize: 13, italic: true, color: C.primary, valign: 'top', margin: 0, isTextBox: true });
    });
    footer(s); watermark(s);
  },

  columns5(d) {
    const s = base();
    title(s, d.title);
    const cw = 2.25, gap = (W - 2 * MX - 5 * cw) / 4;
    d.columns.forEach((c, i) => {
      const x = MX + i * (cw + gap);
      card(s, x, 1.55, cw, 0.65, C.deep);
      s.addText(c.head, { x: x + 0.2, y: 1.55, w: cw - 0.4, h: 0.65, fontFace: F.title, fontSize: 19, bold: true, color: C.white, valign: 'middle', margin: 0, isTextBox: true });
      card(s, x, 2.2, cw, 4.35, C.p10);
      s.addText(bulletLines(c.lines), { x: x + 0.12, y: 2.4, w: cw - 0.3, h: 4.0, fontFace: F.body, fontSize: 15, color: C.ink, valign: 'top', paraSpaceAfter: 10, margin: 0, isTextBox: true });
    });
    footer(s); watermark(s);
  },

  wireframe(d) {
    const s = base();
    title(s, d.title);
    const wf = d.wireframe, x = MX, y = 1.5, w = 8.6, h = 5.3, G = 'C9C6CF', LG = 'E6E4EA';
    s.addShape('rect', { x, y, w, h, fill: { color: C.white }, line: { color: G, width: 1.25 } });
    s.addShape('rect', { x, y, w, h: 0.55, fill: { color: LG }, line: { color: G, width: 0.75 } });
    s.addShape('rect', { x: x + 0.2, y: y + 0.13, w: 1.2, h: 0.3, fill: { color: G }, line: { color: G } });
    s.addText('LOGO', { x: x + 0.2, y: y + 0.13, w: 1.2, h: 0.3, fontFace: F.body, fontSize: 9, color: C.white, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
    s.addText(wf.nav, { x: x + 3.2, y, w: 5.2, h: 0.55, fontFace: F.body, fontSize: 11, color: C.steel, align: 'right', valign: 'middle', margin: 0, isTextBox: true });
    s.addText(runs(wf.headline), { x: x + 0.35, y: y + 0.75, w: 5.6, h: 1.05, fontFace: F.body, fontSize: 22, bold: true, color: C.ink, valign: 'top', margin: 0, isTextBox: true });
    s.addText(runs(wf.subline), { x: x + 0.35, y: y + 1.8, w: 5.6, h: 0.75, fontFace: F.body, fontSize: 12, color: C.steel, valign: 'top', margin: 0, isTextBox: true });
    s.addShape('rect', { x: x + 6.2, y: y + 0.75, w: 2.1, h: 1.8, fill: { color: LG }, line: { color: G, width: 0.75 } });
    s.addText('Plant photo', { x: x + 6.2, y: y + 0.75, w: 2.1, h: 1.8, fontFace: F.body, fontSize: 11, color: C.steel, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
    // November show banner, orange only as a small dot accent
    s.addShape('rect', { x: x + 0.35, y: y + 2.7, w: w - 0.7, h: 0.55, fill: { color: LG }, line: { color: G, width: 0.75 } });
    s.addShape('ellipse', { x: x + 0.55, y: y + 2.89, w: 0.17, h: 0.17, fill: { color: C.orange }, line: { color: C.orange } });
    s.addText(runs(wf.show_banner), { x: x + 0.85, y: y + 2.7, w: w - 1.4, h: 0.55, fontFace: F.body, fontSize: 12, bold: true, color: C.ink, valign: 'middle', margin: 0, isTextBox: true });
    const cw = (w - 0.7 - 3 * 0.2) / 4;
    wf.cards.forEach((c, i) => {
      const cx = x + 0.35 + i * (cw + 0.2);
      s.addShape('rect', { x: cx, y: y + 3.45, w: cw, h: 1.05, fill: { color: C.white }, line: { color: G, width: 0.75 } });
      s.addShape('rect', { x: cx + 0.12, y: y + 3.57, w: cw - 0.24, h: 0.45, fill: { color: LG }, line: { color: LG } });
      s.addText(c, { x: cx + 0.12, y: y + 4.05, w: cw - 0.24, h: 0.4, fontFace: F.body, fontSize: 11, bold: true, color: C.ink, valign: 'middle', margin: 0, isTextBox: true });
    });
    s.addShape('roundRect', { x: x + w - 2.35, y: y + 4.68, w: 2.0, h: 0.42, rectRadius: 0.2, fill: { color: G }, line: { color: G } });
    s.addText(wf.whatsapp, { x: x + w - 2.35, y: y + 4.68, w: 2.0, h: 0.42, fontFace: F.body, fontSize: 11, bold: true, color: C.white, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
    s.addText('Contact strip: phone · email · address', { x: x + 0.35, y: y + 4.68, w: 5, h: 0.42, fontFace: F.body, fontSize: 11, color: C.steel, valign: 'middle', margin: 0, isTextBox: true });
    // right-hand notes
    const notes = ['Headline says what Yerik makes, from where, since when.', 'The November show sits on the first screen.', 'Product ranges are one tap away.', 'A WhatsApp button that works.'];
    callouts(s, notes, 9.6, 1.65, 3.15, 15, 0.95);
    s.addText(d.label, { x: 9.6, y: 5.6, w: 3.15, h: 1.0, fontFace: F.body, fontSize: 13, italic: true, color: C.steel, valign: 'top', margin: 0, isTextBox: true });
    footer(s); watermark(s);
  },

  twocol(d) {
    const s = base();
    title(s, d.title);
    const cw = 5.9;
    [d.left, d.right].forEach((col, i) => {
      const x = MX + i * (cw + 0.33);
      card(s, x, 1.5, cw, 4.0 + (col.note ? 0 : 1.0));
      s.addText(col.head, { x: x + 0.3, y: 1.7, w: cw - 0.6, h: 0.5, fontFace: F.title, fontSize: 22, bold: true, color: C.primary, margin: 0, isTextBox: true });
      s.addText(bulletLines(col.lines), { x: x + 0.3, y: 2.35, w: cw - 0.6, h: 3.0, fontFace: F.body, fontSize: 17, color: C.ink, valign: 'top', paraSpaceAfter: 8, margin: 0, isTextBox: true });
      if (col.note) {
        card(s, x, 5.6, cw, 1.0, C.deep);
        s.addText(runs(col.note), { x: x + 0.3, y: 5.6, w: cw - 0.6, h: 1.0, fontFace: F.body, fontSize: 15, bold: true, color: C.white, valign: 'middle', margin: 0, isTextBox: true });
      }
    });
    footer(s); watermark(s);
  },

  table(d) {
    const s = base();
    title(s, d.title);
    const big = d.rows.length > 6;
    const fs_ = big ? 13 : 14;
    const colW = d.columns[1] === 'Giraffe does' ? [2.1, 6.4, 3.63] : [3.2, 3.7, 5.23];
    const head = d.columns.map((c) => ({ text: c, options: { bold: true, color: C.white, fill: { color: C.primary } } }));
    const body = d.rows.map((r, ri) => r.map((cell, ci) => ({
      text: runs(cell),
      options: { fill: { color: ri % 2 ? C.white : C.p10 }, bold: ci === 0, color: ci === 2 && !big ? C.ink : (ci === 2 ? C.primary : C.ink) },
    })));
    s.addTable([head, ...body], {
      x: MX, y: 1.4, w: W - 2 * MX, colW, fontFace: F.body, fontSize: fs_, color: C.ink,
      border: { type: 'solid', pt: 0.75, color: C.rule }, valign: 'middle', margin: [3, 6, 3, 6],
      rowH: big ? 0.4 : [0.5, ...d.rows.map(() => 0.8)],
    });
    if (d.note || d.deadline) {
      s.addText(runs(d.note || ''), { x: MX, y: 5.3, w: 12.1, h: 0.35, fontFace: F.body, fontSize: 14, italic: true, color: C.steel, margin: 0, isTextBox: true });
      card(s, MX, 5.8, W - 2 * MX, 0.7, C.deep);
      s.addText(runs(d.deadline), { x: MX + 0.3, y: 5.8, w: W - 2 * MX - 0.6, h: 0.7, fontFace: F.body, fontSize: 18, bold: true, color: C.white, valign: 'middle', margin: 0, isTextBox: true });
    }
    footer(s); watermark(s);
  },

  checklist(d) {
    const s = base();
    title(s, d.title);
    const cw = 5.9, rowH = 0.98;
    d.items.forEach(([text, due], i) => {
      const x = MX + Math.floor(i / 5) * (cw + 0.33), y = 1.5 + (i % 5) * rowH;
      s.addShape('rect', { x, y, w: cw, h: rowH - 0.14, fill: { color: C.white }, line: { color: C.rule, width: 0.75 } });
      numCircle(s, i + 1, x + 0.18, y + (rowH - 0.14) / 2 - 0.19, 0.38, C.primary, C.white, 12);
      s.addText(runs(text), { x: x + 0.72, y, w: cw - 2.0, h: rowH - 0.14, fontFace: F.body, fontSize: 14, color: C.ink, valign: 'middle', margin: 0, isTextBox: true });
      s.addShape('roundRect', { x: x + cw - 1.18, y: y + (rowH - 0.14) / 2 - 0.17, w: 1.0, h: 0.34, rectRadius: 0.15, fill: { color: C.p20 }, line: { color: C.p20 } });
      s.addText(due, { x: x + cw - 1.18, y: y + (rowH - 0.14) / 2 - 0.17, w: 1.0, h: 0.34, fontFace: F.body, fontSize: 11, bold: true, color: C.primary, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
    });
    footer(s); watermark(s);
  },

  pricing(d) {
    const s = base();
    title(s, d.title);
    s.addText(runs(d.lead), { x: MX, y: 1.3, w: 12, h: 0.4, fontFace: F.body, fontSize: 17, color: C.steel, margin: 0, isTextBox: true });
    const head = d.columns.map((c) => ({ text: c, options: { bold: true, color: C.white, fill: { color: C.primary } } }));
    const body = d.rows.map((r) => {
      const total = /total/i.test(r[0]);
      const opt = /^Optional/.test(r[0]);
      return r.map((cell, ci) => ({
        text: runs(cell),
        options: { bold: total || ci === 0, fill: { color: total ? C.p20 : C.white }, color: opt && ci === 0 ? C.steel : C.ink, align: ci === 2 ? 'right' : 'left' },
      }));
    });
    s.addTable([head, ...body], {
      x: MX, y: 1.85, w: W - 2 * MX, colW: [4.3, 5.9, 1.93], fontFace: F.body, fontSize: 14,
      border: { type: 'solid', pt: 0.75, color: C.rule }, valign: 'middle', margin: [3, 8, 3, 8], rowH: 0.42,
    });
    s.addText(para(d.notes.map((n) => '· ' + n), { fontSize: 12, color: C.steel }, 2), { x: MX, y: 5.65, w: 7.6, h: 1.2, fontFace: F.body, valign: 'top', margin: 0, isTextBox: true });
    s.addText(runs(d.later), { x: 8.6, y: 5.65, w: 4.13, h: 0.9, fontFace: F.body, fontSize: 13, italic: true, color: C.primary, valign: 'top', margin: 0, isTextBox: true });
    footer(s); watermark(s);
  },

  closing(d) {
    const s = base(true);
    title(s, d.title, { color: C.white });
    const L = d.left;
    s.addText(para(L.lines, { fontSize: 17, color: C.p20 }, 6), { x: MX, y: 1.5, w: 6.0, h: 1.4, fontFace: F.body, valign: 'top', margin: 0, isTextBox: true });
    s.addText(runs(`“${L.quote}”`), { x: MX, y: 3.0, w: 6.0, h: 0.9, fontFace: F.title, fontSize: 24, italic: true, color: C.white, valign: 'top', margin: 0, isTextBox: true });
    s.addShape('rect', { x: MX, y: 4.1, w: 6.0, h: 2.35, fill: { color: C.primary }, line: { color: C.primary } });
    s.addText([
      { text: L.example_head, options: { bold: true, fontSize: 17, color: C.white, breakLine: true, paraSpaceAfter: 6 } },
      ...runs(L.example, { fontSize: 15, color: C.p20 }),
    ], { x: MX + 0.3, y: 4.1, w: 3.2, h: 2.35, fontFace: F.body, valign: 'middle', margin: 0, isTextBox: true });
    // Neev images if present, else one placeholder tile
    const neevDir = path.join(ROOT, 'inputs/neev');
    const neev = fs.existsSync(neevDir) ? fs.readdirSync(neevDir).filter((f) => /\.(jpe?g|png|webp)$/i.test(f)).slice(0, 2) : [];
    if (neev.length) neev.forEach((f, i) => s.addImage({ path: path.join(neevDir, f), x: MX + 3.65 + i * 1.2, y: 4.3, w: 1.1, h: 1.95, sizing: { type: 'cover', w: 1.1, h: 1.95 } }));
    else {
      s.addShape('rect', { x: MX + 3.65, y: 4.3, w: 2.15, h: 1.95, fill: { color: C.deep }, line: { color: C.p20, width: 1, dashType: 'dash' } });
      s.addText('Neev Seeds before / after images (optional)', { x: MX + 3.75, y: 4.3, w: 1.95, h: 1.95, fontFace: F.body, fontSize: 10, color: C.p20, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
    }
    const Rt = d.right, rx = 7.3, rw = W - MX - rx;
    s.addText(Rt.head.toUpperCase(), { x: rx, y: 1.5, w: rw, h: 0.35, fontFace: F.body, fontSize: 13, bold: true, charSpacing: 3, color: C.p20, margin: 0, isTextBox: true });
    Rt.steps.forEach((st, i) => {
      const y = 2.0 + i * 0.85;
      numCircle(s, i + 1, rx, y, 0.5, C.white, C.deep, 16);
      s.addText(runs(st), { x: rx + 0.7, y, w: rw - 0.7, h: 0.5, fontFace: F.body, fontSize: 19, color: C.white, valign: 'middle', margin: 0, isTextBox: true });
    });
    s.addShape('line', { x: rx, y: 5.6, w: rw, h: 0, line: { color: C.steel, width: 0.75 } });
    const [cName, ...cRest] = fill(Rt.contact).split(' · ');
    s.addText([
      { text: cName, options: { bold: true, fontSize: 17, breakLine: true } },
      ...runs(cRest.join(' · '), { fontSize: 14 }),
    ], { x: rx, y: 5.75, w: rw, h: 0.8, fontFace: F.body, color: C.white, valign: 'top', margin: 0, isTextBox: true });
    footer(s, true); watermark(s);
  },
};

for (const sl of content.slides) {
  const fn = R[sl.type];
  if (!fn) throw new Error(`No renderer for slide type ${sl.type}`);
  fn(sl);
}

const outName = NO_WATERMARK ? 'Yerik_Proposal_Editable.pptx' : (DRAFT ? 'Yerik_Proposal_DRAFT.pptx' : 'Yerik_Proposal_v1.pptx');
const out = path.join(ROOT, 'output', outName);
for (const f of NO_WATERMARK ? [outName] : ['Yerik_Proposal_DRAFT.pptx', 'Yerik_Proposal_v1.pptx']) { const p = path.join(ROOT, 'output', f); if (fs.existsSync(p)) fs.unlinkSync(p); }
pres.writeFile({ fileName: out }).then(() => {
  fs.writeFileSync(path.join(ROOT, 'output/.build.json'), JSON.stringify({ file: outName, draft: DRAFT, placeholders: placeholderCount, missingShots: [...missingShots] }, null, 2));
  console.log(`Wrote output/${outName} (${pageNo} slides, ${placeholderCount} placeholders, ${missingShots.size} screenshots missing)`);
});
