// Gentle crawl + raw screenshots for the Yerik proposal (brief section 6).
//
//   node scripts/capture.mjs [siteUrl]          default: http://www.yerikindia.com/
//
// Rules built in:
//   - real Chromium, 2-3 s wait between pages, max 60 pages, same domain only
//   - NEVER submits a form: the careers form is filled, screenshotted, then the page is closed
//   - no logins; Google / LinkedIn shots come from inputs/manual-screenshots/
// Writes work/screenshots/raw/*.jpg and work/crawl.json (page list, categories, load time).
import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const RAW = path.join(ROOT, 'work/screenshots/raw');
const START = process.argv[2] || 'http://www.yerikindia.com/';
const COMPETITORS = {
  '06_competitor_jrs': process.env.JRS_URL || 'https://www.jrsparts.com/',
  '07_competitor_machineparts': process.env.MP_URL || 'https://machineparts.co.in/',
};
const MAX_PAGES = 60;
const host = new URL(START).hostname.replace(/^www\./, '');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const pause = () => sleep(2000 + Math.random() * 1000);
const sameSite = (u) => { try { return new URL(u).hostname.replace(/^www\./, '') === host; } catch { return false; } };
const clean = (u) => { const x = new URL(u); x.hash = ''; return x.toString(); };

fs.mkdirSync(RAW, { recursive: true });
const shot = (page, name, opts = {}) => page.screenshot({ path: path.join(RAW, `${name}.jpg`), type: 'jpeg', quality: 80, ...opts });

// Block any form submission at the browser level, whatever the page script does.
const NO_SUBMIT = () => {
  HTMLFormElement.prototype.submit = function () { console.warn('submit blocked'); };
  HTMLFormElement.prototype.requestSubmit = function () { console.warn('submit blocked'); };
  document.addEventListener('submit', (e) => { e.preventDefault(); e.stopImmediatePropagation(); }, true);
};

const browser = await chromium.launch();
const report = { start: START, date: new Date().toISOString(), pages: [], categories: {}, productPages: [], pdfs: [], tweetLabelPages: [], errors: [] };

try {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  await ctx.addInitScript(NO_SUBMIT);
  // Refuse non-GET requests to the client's site: nothing can be posted.
  await ctx.route('**/*', (route) => {
    const r = route.request();
    if (r.method() !== 'GET' && sameSite(r.url())) return route.abort();
    return route.continue();
  });
  const page = await ctx.newPage();

  // Homepage + load time
  const t0 = Date.now();
  await page.goto(START, { waitUntil: 'load', timeout: 60000 });
  report.homeLoadSeconds = +((Date.now() - t0) / 1000).toFixed(1);
  report.https = page.url().startsWith('https://');
  await shot(page, '01_home_desktop');

  // Crawl (BFS)
  const queue = [clean(page.url())];
  const seen = new Set(queue);
  while (queue.length && report.pages.length < MAX_PAGES) {
    const url = queue.shift();
    if (report.pages.length) { await pause(); await page.goto(url, { waitUntil: 'load', timeout: 60000 }).catch((e) => report.errors.push(`${url}: ${e.message}`)); }
    const info = await page.evaluate(() => ({
      title: document.title,
      links: [...document.querySelectorAll('a[href]')].map((a) => a.href),
      hasTweet: /\btweet\b/i.test(document.body?.innerText || ''),
      hasViewport: !!document.querySelector('meta[name=viewport]'),
      year: (document.body?.innerText.match(/(?:©|copyright)\s*(?:\d{4}\s*[-–]\s*)?(\d{4})/i) || [])[1] || null,
      form: !!document.querySelector('form'),
    })).catch(() => ({ links: [] }));
    report.pages.push({ url, title: info.title, hasViewport: info.hasViewport, year: info.year, form: info.form });
    const m = new URL(url).pathname.match(/^\/(\d+)-([A-Z0-9_&]+)-(\d+)-([A-Z0-9_&]+)-/);
    if (m) {
      (report.categories[m[2]] ||= new Set()).add(m[4]);
      report.productPages.push(url);
    }
    if (info.hasTweet) report.tweetLabelPages.push(url);
    for (const l of info.links) {
      if (!sameSite(l)) continue;
      const c = clean(l);
      if (/\.pdf($|\?)/i.test(c)) { if (!report.pdfs.includes(c)) report.pdfs.push(c); continue; }
      if (/^(mailto|tel|javascript):/.test(c) || seen.has(c)) continue;
      seen.add(c); queue.push(c);
    }
  }
  report.unvisited = queue.length;

  // 04 product page with the "tweet" label
  const tweetPage = report.tweetLabelPages.find((u) => report.productPages.includes(u)) || report.productPages[0];
  if (tweetPage) {
    await pause(); await page.goto(tweetPage, { waitUntil: 'load' });
    const box = await page.getByText(/tweet/i).first().boundingBox().catch(() => null);
    await shot(page, '04_product_page', box ? { clip: { x: 0, y: Math.max(0, box.y - 300), width: 1440, height: 700 } } : {});
  }

  // 03 phone number (tight crop)
  await pause(); await page.goto(START, { waitUntil: 'load' });
  const phone = page.getByText(/77173\s*04013|7717304013/).first();
  const pbox = await phone.boundingBox().catch(() => null);
  if (pbox) await shot(page, '03_phone_number', { clip: { x: Math.max(0, pbox.x - 120), y: Math.max(0, pbox.y - 60), width: Math.min(700, 1440 - Math.max(0, pbox.x - 120)), height: 180 }, fullPage: true });
  else report.errors.push('phone number not found on homepage');

  // 05 careers form: fill, screenshot, close. NEVER submit.
  const careers = report.pages.find((p) => /career/i.test(p.url));
  if (careers) {
    await pause();
    const cp = await ctx.newPage();
    await cp.goto(careers.url, { waitUntil: 'load' });
    const fill = async (key, v) => {
      const el = cp.locator(`input[name*="${key}" i], input[id*="${key}" i], input[placeholder*="${key}" i]`).first();
      if (await el.count()) await el.fill(v);
    };
    await fill('name', 'Test');
    await fill('mail', 'abc');
    const form = cp.locator('form').first();
    const fbox = await form.boundingBox().catch(() => null);
    await shot(cp, '05_careers_form', fbox ? { clip: fbox, fullPage: true } : {});
    await cp.close(); // closed without submitting
  } else report.errors.push('careers page not found');

  // 02 mobile, first 2 screens
  const mctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  await mctx.addInitScript(NO_SUBMIT);
  const mp = await mctx.newPage();
  await pause(); await mp.goto(START, { waitUntil: 'load' });
  await shot(mp, '02_home_mobile', { clip: { x: 0, y: 0, width: 390, height: 1688 }, fullPage: true });
  await mctx.close();

  // Competitors, first screen
  for (const [name, url] of Object.entries(COMPETITORS)) {
    await pause();
    await page.goto(url, { waitUntil: 'load', timeout: 60000 }).then(() => shot(page, name)).catch((e) => report.errors.push(`${name}: ${e.message}`));
  }
} catch (e) {
  report.errors.push(String(e));
} finally {
  await browser.close();
  for (const k of Object.keys(report.categories)) report.categories[k] = [...report.categories[k]];
  report.counts = { pagesVisited: report.pages.length, categories: Object.keys(report.categories).length, productPages: report.productPages.length, pdfs: report.pdfs.length };
  fs.writeFileSync(path.join(ROOT, 'work/crawl.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify({ homeLoadSeconds: report.homeLoadSeconds, https: report.https, ...report.counts, errors: report.errors }, null, 2));
}
