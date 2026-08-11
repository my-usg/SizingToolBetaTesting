// Keeps the USG regulator sizing tools from hibernating.
//
// Streamlit Community Cloud sleeps any app after 12 hours without traffic. These
// apps are embedded on hollandsupplycompany.com and my-usg.com, so a sleeping app
// shows customers a "this app has gone to sleep" screen instead of the tool.
//
// A plain HTTP request may not be enough: Streamlit runs its session over a
// websocket, so we drive a real browser to establish a genuine session. If an app
// is already asleep, we click the wake button.

import { chromium } from 'playwright';

const APPS = [
  { name: 'General (all models)', url: 'https://allmodels-usg.streamlit.app/' },
  { name: 'Model 441/461',        url: 'https://model461-usg.streamlit.app/' },
  { name: 'Model 243',            url: 'https://model243-usg.streamlit.app/' },
  { name: 'Model 046',            url: 'https://model046-usg.streamlit.app/' },
  { name: 'Model 143',            url: 'https://model143-usg.streamlit.app/' },
  { name: 'Model 496',            url: 'https://model496-usg.streamlit.app/' },
  { name: 'Model 121/122',        url: 'https://model121-usg.streamlit.app/' },
  { name: 'Model 243-RPC',        url: 'https://modelrpc-usg.streamlit.app/' },
  { name: 'Homepage',             url: 'https://sizingtool-usg.streamlit.app/'},
];

const WAKE_TEXT  = /get this app back up/i;
const SLEEP_TEXT = /gone to sleep/i;
const LIMIT_TEXT = /(over its resource limits|Oh no)/i;

const results = [];

const browser = await chromium.launch();

for (const app of APPS) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await context.newPage();
  const started = Date.now();
  let status = 'awake';
  let detail = '';

  try {
    const resp = await page.goto(app.url, { waitUntil: 'domcontentloaded', timeout: 60_000 });
    const httpStatus = resp ? resp.status() : 0;

    if (!resp || httpStatus >= 400) {
      status = 'error';
      detail = `HTTP ${httpStatus} — app may have been renamed, redeployed or deleted`;
    } else {
      // Give the Streamlit frontend a moment to open its websocket and render.
      await page.waitForTimeout(6_000);
      let body = await page.locator('body').innerText().catch(() => '');

      if (SLEEP_TEXT.test(body) || WAKE_TEXT.test(body)) {
        status = 'was-asleep';
        const wake = page.getByRole('button', { name: WAKE_TEXT });
        const fallback = page.locator('button', { hasText: WAKE_TEXT });
        const target = (await wake.count()) ? wake.first() : fallback.first();

        if (await target.count()) {
          await target.click({ timeout: 15_000 });
          // Cold start: the container has to be rebuilt and the script re-run.
          await page.waitForTimeout(45_000);
          body = await page.locator('body').innerText().catch(() => '');
          detail = SLEEP_TEXT.test(body)
            ? 'clicked wake button but app still reports sleeping'
            : 'woken successfully';
        } else {
          detail = 'sleep screen detected but no wake button found';
        }
      }

      if (LIMIT_TEXT.test(body)) {
        status = 'error';
        detail = 'app is over its resource limits';
      }
    }
  } catch (err) {
    status = 'error';
    detail = err.message.split('\n')[0].slice(0, 160);
  }

  const secs = ((Date.now() - started) / 1000).toFixed(1);
  results.push({ ...app, status, detail, secs });
  await context.close();
}

await browser.close();

// ── report ──────────────────────────────────────────────────────────────────
const pad = (s, n) => String(s).padEnd(n);
console.log('\n' + pad('App', 24) + pad('Status', 13) + 'Detail');
console.log('-'.repeat(78));
for (const r of results) {
  console.log(pad(r.name, 24) + pad(r.status, 13) + (r.detail || `${r.secs}s`));
}

const errors = results.filter(r => r.status === 'error');
const slept  = results.filter(r => r.status === 'was-asleep');

console.log('\n' + `${results.length - errors.length}/${results.length} apps reachable.`);
if (slept.length) {
  console.log(`${slept.length} app(s) had gone to sleep and were woken — consider running this more often.`);
}

// Surface a summary on the workflow run page.
if (process.env.GITHUB_STEP_SUMMARY) {
  const { appendFileSync } = await import('node:fs');
  const icon = s => (s === 'awake' ? '✅' : s === 'was-asleep' ? '💤' : '❌');
  let md = '## Sizing tool app status\n\n| App | Status | Detail |\n|---|---|---|\n';
  for (const r of results) {
    md += `| ${r.name} | ${icon(r.status)} ${r.status} | ${r.detail || r.secs + 's'} |\n`;
  }
  appendFileSync(process.env.GITHUB_STEP_SUMMARY, md);
}

if (errors.length) {
  console.error(`\nFAIL: ${errors.length} app(s) unreachable.`);
  process.exit(1);
}
