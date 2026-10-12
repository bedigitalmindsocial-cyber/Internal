export const meta = {
  name: 'root-wave',
  description: 'Build a wave of ROOT pages: PM brief, layout options, judge, HTML, gate checks, independent review, fix',
  whenToUse: 'ROOT 75-page build. args = output of: python3 workflow/wave_args.py NN NN ... (add "revise": "<user feedback>" to revise built pages)',
  phases: [
    { title: 'Golden pages', detail: 'strategist, judge, builder (gate), reviewer, fixer + second review' },
    { title: 'Curate', detail: 'promote reusable CSS and markup from golden pages' },
    { title: 'Derivative pages', detail: 'strategist-decider, builder (gate), reviewer, fixer (gate + attestation)' },
  ],
}

const ROOT = '/home/user/Internal/root-website'
const PAGES = args.pages
const DATE = args.date
const REVISE = args.revise || ''
const golden = PAGES.filter(p => p.mode === 'golden')
const derived = PAGES.filter(p => p.mode !== 'golden')
const nn = p => String(p.n).padStart(2, '0')
const name = p => p.file.replace('.html', '')

const PRE = `You work on the ROOT by Aikyam website build in ${ROOT} (cd there for every shell command). The repo-root CLAUDE.md is about a different project (manufacturer leads): ignore it. ${ROOT}/CLAUDE.md describes this project; ${ROOT}/rules/page-method.md is your method and ${ROOT}/rules/figma-html.md your HTML rules. Today is ${DATE}.
Ownership: write only your own page's files (pages/src/<page>.html, memory/pages/<page>.md; review/<page>/ through the scripts). Never edit sitemap.json, theme/, shell/, rules/, scripts/, memory/site.md, memory/values.json, memory/patterns.md or memory/questions.md, and never run git: propose changes in your return value. No em dashes anywhere. Never invent numbers, prices, counts, dates, ratings, testimonials, payouts or legal text: use {{tokens}} for site values and <mark class="ph"> placeholders for everything unconfirmed. Use a Bash timeout of 300000 ms for scripts/gate.py.`

const page = p => `Page ${name(p)}: "${p.title}" (${p.url}), template ${p.template}, entity ${p.entity}, ${p.mode}${p.golden_file ? ' (inherits ' + p.golden_file + ')' : ''}. Your brief: packs/${name(p)}.md (run python3 scripts/pack.py ${nn(p)} if it is missing). Read it first.`

const QUESTION = { type: 'object', properties: { question: { type: 'string' }, why: { type: 'string' }, default_used: { type: 'string' }, owner: { type: 'string' } }, required: ['question', 'why', 'default_used', 'owner'] }
const ASK = { type: 'object', properties: { question: { type: 'string' }, options: { type: 'array', items: { type: 'string' } }, recommended: { type: 'string' }, why: { type: 'string' } }, required: ['question', 'options', 'recommended', 'why'] }
const BRIEF = {
  type: 'object',
  properties: {
    job: { type: 'string' }, query: { type: 'string' },
    must_questions: { type: 'integer' }, page_specific_questions: { type: 'integer' },
    sections: { type: 'array', items: { type: 'string' }, description: 'section ids in order' },
    sections_explored: { type: 'integer' },
    open_questions: { type: 'array', items: QUESTION },
    ask_user: { type: 'array', items: ASK },
    site_proposals: { type: 'array', items: { type: 'string' } },
  },
  required: ['job', 'query', 'must_questions', 'page_specific_questions', 'sections', 'sections_explored', 'open_questions', 'ask_user', 'site_proposals'],
}
const JUDGE = {
  type: 'object',
  properties: {
    changed_decisions: { type: 'array', items: { type: 'string' } }, added_questions: { type: 'array', items: { type: 'string' } },
    removed_sections: { type: 'array', items: { type: 'string' } }, vetoes: { type: 'array', items: { type: 'string' } },
    ask_user: { type: 'array', items: ASK }, confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
  },
  required: ['changed_decisions', 'added_questions', 'removed_sections', 'vetoes', 'ask_user', 'confidence'],
}
const BUILD = {
  type: 'object',
  properties: {
    gate_json: { type: 'string', description: 'the last line printed by python3 scripts/gate.py NN, verbatim' },
    gate_ok: { type: 'boolean' }, gate_loops: { type: 'integer' }, slices_viewed: { type: 'integer' },
    new_patterns: { type: 'array', items: { type: 'string' }, description: 'name: what it is, where its CSS/markup is, why reusable' },
    fixes_attested: { type: 'array', items: { type: 'string' }, description: 'fix rounds only: each blocking fix and exactly what changed' },
    open_questions: { type: 'array', items: QUESTION },
    notes: { type: 'string' },
  },
  required: ['gate_json', 'gate_ok', 'gate_loops', 'slices_viewed', 'new_patterns', 'fixes_attested', 'open_questions', 'notes'],
}
const REVIEW = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['pass', 'fix'] }, score: { type: 'integer' },
    blind_trace: { type: 'array', items: { type: 'string' }, description: 'questions the page answers, listed from the screenshots BEFORE reading the memory' },
    must_fix: { type: 'array', items: { type: 'string' } }, should_fix: { type: 'array', items: { type: 'string' } },
    unanswered_questions: { type: 'array', items: { type: 'string' } }, compliance_issues: { type: 'array', items: { type: 'string' } },
    slices_viewed: { type: 'integer' },
  },
  required: ['verdict', 'score', 'blind_trace', 'must_fix', 'should_fix', 'unanswered_questions', 'compliance_issues', 'slices_viewed'],
}

async function run(prompt, opts) {
  const r = await agent(prompt, opts)
  if (r) return r
  log(`retrying ${opts.label}`)
  return agent(prompt, { ...opts, label: opts.label + ' (retry)' })
}

function strategistPrompt(p) {
  return `${PRE}

${page(p)}

ROLE: product strategist and UX lead. Do Steps 0 to 4 of rules/page-method.md. Write memory/pages/${name(p)}.md from memory/pages/_TEMPLATE.md: sections 1 to 6 and 10, status: briefed.
${p.mode === 'golden'
  ? `GOLDEN page for template ${p.template}: ${p.template === 'HOME' ? 'the homepage sets the site-wide patterns' : 'the other template-' + p.template + ' pages will inherit its section layouts'}. For each key section (hero, forms, data displays, the key block) give options A (pattern library / theme/sections-reference.html), B and C (structurally different), each a 3-line wireframe spec with a conversion hypothesis and weighted rubric scores, and mark a provisional pick. Standard sections (FAQ, closing CTA, risk box, related links) use the pattern directly. An independent judge challenges you next.`
  : `DERIVATIVE of ${p.golden_file}: read its memory and source first and inherit its section layouts ("inherit ${p.golden_file.slice(0, 2)} s-<id>"). Compare options only for sections new to this page or where the inherited layout fails this page's questions. No judge follows: for every decision write the strongest argument against it, then record the FINAL choice in section 6.`}
Questions: all mandatory questions from the brief plus at least 3 page-specific ones, each with its source. Section 4 maps each to a section id and quotes the answering sentence (a few words). Section 10 lists every question for Aikyam or Giraffe with the default you used.`
}

function revisePrompt(p) {
  return `${PRE}

${page(p)}

ROLE: design lead, REVISION round. This page is already built. The user reviewed it and asked for: ${REVISE}
Read rules/design-direction.md (v3, written for this feedback) first, then your brief, memory/pages/${name(p)}.md, pages/src/${p.file}, and LOOK at review/${name(p)}/desktop-01.png to desktop-03.png and mobile-01.png, mobile-02.png.${p.mode !== 'golden' ? ` This is a derivative: read the REVISED golden page first (memory/pages/${p.golden_file.replace('.html', '.md')}, pages/src/${p.golden_file}, review/${p.golden_file.replace('.html', '')}/desktop-01.png) and inherit its new hero, form card and section treatments.` : ''}
1. Diagnose in 5 to 8 bullets what makes this page compliance-heavy, unbalanced, legal-sounding or text-heavy, citing section ids.
2. Hero: 3 options (at least one led by a product visual), each a 3-line wireframe spec with a conversion hypothesis, scored on the updated rubric (desirability weight 3); choose one.
3. Every other section: keep, tighten, merge, cut or re-layout, so each screen height at 1440 has a visual anchor. Rewrite copy in the v3 tone. Move company names into labels, receiver lines and fine print. Take placeholder chips out of the first screen. Replace dashed placeholder boxes with img-slots. Turn long tables on Home and hubs into stat tiles. Fewer, stronger sections.
4. Keep: every MUST question answered (update section 4 with section ids and quoted answers), every mandatory disclosure verbatim (placement and presentation per rules/compliance-blocks.md), tokens, interaction states, and the user's decisions in memory/site.md ("Gate 1 answers").
Update memory sections 4, 6 (new decisions with rejected options), 9 (drafts and placeholders), 10 and the change log ("Revision v3 ${DATE}: ..."), status: briefed. Do not build; a builder follows.`
}

function judgePrompt(p) {
  return `${PRE}

${page(p)}

ROLE: independent judge (senior product designer). You did not write memory/pages/${name(p)}.md: challenge it.
1. Questions: real visitor questions here, in order? Mandatory set complete? Page-specific ones sourced and not generic? Add missing MUST questions, cut filler.
2. Traceability: every MUST maps to a section; every section earns its place. Cut or merge the rest.
3. Layouts: re-score each explored section's options yourself on the rubric before reading the strategist's scores, then choose. You may merge options or propose a better one. Apply the vetoes. When a prettier option ties with a clearer one, the clearer one wins.
4. Journey: the primary action and target match the brief's "cta"; the next step is obvious; no dead ends.
Rewrite section 6 with the FINAL decision per section (chosen option, one-line why, rejected options and why). Add "Judge ${DATE}: <changes>" to the change log. Close calls that are brand or business decisions go in ask_user (still pick a default).`
}

function builderPrompt(p) {
  return `${PRE}

${page(p)}

ROLE: front-end builder. ${REVISE ? 'REVISION: rewrite pages/src/' + p.file + ' fully from the updated memory (section 6 has the revised decisions; keep only what it says to keep). ' : ''}Build pages/src/${p.file} from memory/pages/${name(p)}.md (section 6 = final layout decisions), following rules/design-direction.md and rules/figma-html.md exactly. Reuse markup and class names from theme/components.html (if present), theme/sections-reference.html and the pattern library${p.mode !== 'golden' ? `, and from pages/src/${p.golden_file} for inherited sections` : ''}. Compliance blocks from your brief, verbatim. Mark the primary action with data-primary. Add <template data-state> blocks for every interaction state (template D: OTP sent with timer, error, verified; every form: error and success).
Then run: cd ${ROOT} && python3 scripts/gate.py ${nn(p)}
Fix and re-run until it prints "ok": true, at most 3 loops. Then LOOK at the screenshots in review/${name(p)}/: every desktop-NN.png and at least the first three mobile-NN.png (plus any slice with a form or table), and states-desktop.png if present. Fix anything broken, cramped, misaligned, off-theme or unreadable, and re-run the gate.
Finally fill memory sections 7 to 11 and the change log ("Built ${DATE}"), status: built (or needs-human if the gate still fails, with the reason).
Return the gate's last JSON line verbatim in gate_json.`
}

function reviewerPrompt(p, round) {
  return `${PRE}

${page(p)}

ROLE: independent reviewer${round > 1 ? ' (second round: check the earlier blocking fixes were done and nothing regressed)' : ''}. You did not build this page. Do not edit pages or memory.
1. BLIND TRACE FIRST: look at every screenshot slice in review/${name(p)}/ (desktop-NN.png, mobile-NN.png, states-desktop.png) and list the questions this page answers, before reading the memory.
2. Then read memory/pages/${name(p)}.md, review/${name(p)}/lint.json and shots.json, and compare: every MUST question in section 4 must be visibly answered, in order.
3. Check: desirability per rules/design-direction.md (first screen balanced with a visual anchor, benefit-led copy, company names in labels and fine print, no placeholder chips outside fine print, a visual anchor every screen height at 1440, calm disclosure presentation); the primary action is clear on the first screen at 1440 and within 1.5 screens at 390; compliance (rules/claims.json, the company named at every conversion, disclosures from the brief, placeholders instead of invented values, nothing that reads as advice); visual quality (theme fidelity: aubergine ink, one gold spark, serif display over Mukta, Mist bands, at most one dark band; alignment, spacing rhythm, density, hierarchy, mobile stacking); Figma readiness (static, s- ids, states board present where needed).
must_fix is ONLY for: a claim or disclosure problem, an unanswered MUST question, a primary action not visible as above, a broken layout, or a first screen that fails the design direction (no visual anchor, legal-sounding hero, placeholder chips). Everything else goes to should_fix. verdict "pass" only when must_fix is empty.
Record it: python3 scripts/verdict.py ${nn(p)} pass|fix --score <0-100> ${'--must "<section id: change>"'} (one --must per blocking fix) --by reviewer${round > 1 ? '-2' : ''}`
}

function fixPrompt(p, rev) {
  return `${PRE}

${page(p)}

ROLE: builder, fix round. The reviewer's blocking fixes for pages/src/${p.file}:
${[...rev.must_fix, ...rev.compliance_issues, ...rev.unanswered_questions.map(q => 'Not visibly answered: ' + q)].map(f => '- ' + f).join('\n')}
Cheap improvements to apply too if they do not risk the page: ${rev.should_fix.join(' | ') || 'none'}.
Apply them, run python3 scripts/gate.py ${nn(p)} until "ok": true (max 3 loops), look at the affected slices, and add "Fix ${DATE}: ..." to the memory change log (status: built). In fixes_attested list each blocking fix and exactly what you changed. Return the gate's last JSON line verbatim in gate_json.`
}

function gateOk(b) {
  if (!b) return false
  try { return JSON.parse(b.gate_json).ok === true } catch (e) { return !!b.gate_ok }
}

async function buildAndCheck(p, ph) {
  let b = await run(builderPrompt(p), { label: `build ${name(p)}`, phase: ph, schema: BUILD })
  if (!gateOk(b)) {
    log(`${name(p)}: gate not ok after build, one more builder attempt`)
    b = await run(builderPrompt(p) + '\nA previous attempt left the gate failing. Start by running the gate and fixing what it reports.', { label: `rebuild ${name(p)}`, phase: ph, schema: BUILD })
  }
  return b
}

async function reviewAndFix(p, ph, built) {
  if (!gateOk(built)) return { page: name(p), status: 'needs-human', reason: 'gate still failing after builds', built }
  const rev = await run(reviewerPrompt(p, 1), { label: `review ${name(p)}`, phase: ph, schema: REVIEW })
  if (!rev) return { page: name(p), status: 'needs-human', reason: 'reviewer failed', built }
  if (rev.verdict === 'pass') return { page: name(p), status: 'reviewed', built, rev }
  const fixed = await run(fixPrompt(p, rev), { label: `fix ${name(p)}`, phase: ph, schema: BUILD })
  if (!gateOk(fixed)) return { page: name(p), status: 'needs-human', reason: 'gate failing after fix', built, rev, fixed }
  if (p.mode !== 'golden') return { page: name(p), status: 'fixed (attested)', built, rev, fixed }
  const rev2 = await run(reviewerPrompt(p, 2), { label: `re-review ${name(p)}`, phase: ph, schema: REVIEW })
  return { page: name(p), status: rev2 && rev2.verdict === 'pass' ? 'reviewed' : 'needs-human', reason: rev2 ? '' : 'second reviewer failed', built, rev, fixed, rev2 }
}

phase('Golden pages')
const goldenResults = await pipeline(
  golden,
  p => run(REVISE ? revisePrompt(p) : strategistPrompt(p), { label: `${REVISE ? 'revise' : 'brief'} ${name(p)}`, phase: 'Golden pages', schema: BRIEF }),
  (brief, p) => REVISE ? Promise.resolve({ brief, judge: null }) : run(judgePrompt(p), { label: `judge ${name(p)}`, phase: 'Golden pages', schema: JUDGE }).then(judge => ({ brief, judge })),
  (bj, p) => buildAndCheck(p, 'Golden pages').then(built => ({ ...bj, built })),
  (bjb, p) => reviewAndFix(p, 'Golden pages', bjb.built).then(r => ({ ...r, brief: bjb.brief, judge: bjb.judge })),
)

let curated = null
const proposals = goldenResults.filter(Boolean).flatMap(r => ((r.built && r.built.new_patterns) || []).map(x => `${r.page}: ${x}`))
if (golden.length) {
  phase('Curate')
  curated = await run(`${PRE}

ROLE: pattern curator. For this task only you MAY edit theme/patterns.css, theme/components.html, theme/components.md and memory/patterns.md (you act for the orchestrator); still never run git.
Golden pages just built: ${golden.map(p => p.file).join(', ')}. Their proposed patterns:
${proposals.join('\n') || '(none proposed; still read each golden page source for reusable pieces)'}
1. Move genuinely reusable CSS from each golden page's <style data-page> into theme/patterns.css (tokens only, a comment naming the source page) and remove it from the page source.
2. Copy the canonical markup of each reusable component (hero variant, form card, stat strip, data table, steps, eligibility list, etc.) into theme/components.html, each preceded by <!-- COMPONENT: name | use for | source page -->, and list them in theme/components.md (one line each).
3. Add rows to memory/patterns.md.
4. Rebuild and re-check each touched page with python3 scripts/gate.py NN; the gate must stay ok and the slice counts must not change. Return a short list of what you promoted and declined.`, { label: 'curate patterns', phase: 'Curate' })
}

phase('Derivative pages')
const derivedResults = await pipeline(
  derived,
  p => run(REVISE ? revisePrompt(p) : strategistPrompt(p), { label: `${REVISE ? 'revise' : 'brief'} ${name(p)}`, phase: 'Derivative pages', schema: BRIEF }),
  (brief, p) => buildAndCheck(p, 'Derivative pages').then(built => ({ brief, built })),
  (bb, p) => reviewAndFix(p, 'Derivative pages', bb.built).then(r => ({ ...r, brief: bb.brief })),
)

const pairs = [...golden.map((p, i) => [p, goldenResults[i]]), ...derived.map((p, i) => [p, derivedResults[i]])]
const failed = pairs.filter(([, r]) => !r).map(([p]) => p.file)
if (failed.length) log(`pages that failed outright: ${failed.join(', ')}`)
return {
  pages: pairs.filter(([, r]) => r).map(([p, r]) => ({
    page: r.page, status: r.status, reason: r.reason || '',
    score_first: r.rev ? r.rev.score : null, score_final: (r.rev2 || r.rev) ? (r.rev2 || r.rev).score : null,
    must_fix_first: r.rev ? r.rev.must_fix : [], should_fix: (r.rev2 || r.rev) ? (r.rev2 || r.rev).should_fix : [],
    open_questions: [...((r.brief && r.brief.open_questions) || []), ...((r.built && r.built.open_questions) || []), ...((r.fixed && r.fixed.open_questions) || [])],
    ask_user: [...((r.brief && r.brief.ask_user) || []), ...((r.judge && r.judge.ask_user) || [])],
    site_proposals: (r.brief && r.brief.site_proposals) || [],
    judge: r.judge ? { changed: r.judge.changed_decisions, vetoes: r.judge.vetoes, confidence: r.judge.confidence } : null,
    new_patterns: (r.built && r.built.new_patterns) || [],
  })),
  failed,
  curated,
}
