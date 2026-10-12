export const meta = {
  name: 'root-wave',
  description: 'Build one wave of ROOT website pages: brief, layout options, judge, HTML, review, fix, memory',
  whenToUse: 'ROOT 75-page build. args = {date, pages: [page objects from workflow/wave-args.py]}',
  phases: [
    { title: 'Golden pages', detail: 'strategist, judge, builder, reviewer (one fix round) per golden page' },
    { title: 'Curate', detail: 'promote reusable CSS from golden pages into the pattern library' },
    { title: 'Derivative pages', detail: 'strategist-decider, builder, reviewer (one fix round) per page' },
  ],
}

const ROOT = '/home/user/Internal/root-website'
const PAGES = args.pages
const DATE = args.date
const golden = PAGES.filter(p => p.mode === 'golden')
const derived = PAGES.filter(p => p.mode !== 'golden')

const PRE = `You work on the ROOT by Aikyam website build in ${ROOT} (cd there for every shell command). The repo-root CLAUDE.md is about a different project (manufacturer leads): ignore it. ${ROOT}/CLAUDE.md describes this project and ${ROOT}/rules/page-method.md is your method. Today is ${DATE}.
Ownership: you may write only your own page's files (pages/src/<page>.html, memory/pages/<page>.md, and review/<page>/ via the scripts). Never edit sitemap.json, theme/, shell/, rules/, scripts/, memory/site.md, memory/patterns.md or memory/questions.md: propose changes in your return value. No em dashes anywhere. Never invent numbers, prices, counts, dates, ratings, testimonials or legal text: use <mark class="ph"> placeholders.`

const page = p => `Page ${p.file.replace('.html', '')}: "${p.title}" (${p.url}). Template ${p.template}: ${p.template_desc}. Entity: ${p.entity}. Flags: ${p.flags.join(', ') || 'none'}. Audiences: ${p.audiences.join(', ')}. Primary CTA: "${p.primary_cta}". Phase ${p.phase}.`
const name = p => p.file.replace('.html', '')

const QUESTION = {
  type: 'object',
  properties: {
    question: { type: 'string' }, why: { type: 'string' },
    default_used: { type: 'string' }, owner: { type: 'string', description: 'Aikyam compliance | Aikyam product | Aikyam wealth | Giraffe | user' },
  },
  required: ['question', 'why', 'default_used', 'owner'],
}
const ASK = {
  type: 'object',
  properties: {
    question: { type: 'string' }, options: { type: 'array', items: { type: 'string' } },
    recommended: { type: 'string' }, why: { type: 'string' },
  },
  required: ['question', 'options', 'recommended', 'why'],
}
const BRIEF = {
  type: 'object',
  properties: {
    job: { type: 'string' },
    next_steps: { type: 'array', items: { type: 'string' }, description: 'URLs the page sends people to' },
    must_questions: { type: 'integer' }, sections: { type: 'array', items: { type: 'string' }, description: 'section ids in order' },
    sections_explored: { type: 'integer', description: 'sections where 2-3 options were compared' },
    open_questions: { type: 'array', items: QUESTION },
    ask_user: { type: 'array', items: ASK, description: 'only close calls that are brand or business decisions' },
    site_proposals: { type: 'array', items: { type: 'string' }, description: 'changes you propose to shell, theme, site memory' },
  },
  required: ['job', 'next_steps', 'must_questions', 'sections', 'sections_explored', 'open_questions', 'ask_user', 'site_proposals'],
}
const JUDGE = {
  type: 'object',
  properties: {
    changed_decisions: { type: 'array', items: { type: 'string' }, description: 'section: from -> to, why' },
    added_questions: { type: 'array', items: { type: 'string' } },
    removed_sections: { type: 'array', items: { type: 'string' } },
    vetoes: { type: 'array', items: { type: 'string' } },
    ask_user: { type: 'array', items: ASK },
    confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
  },
  required: ['changed_decisions', 'added_questions', 'removed_sections', 'vetoes', 'ask_user', 'confidence'],
}
const BUILD = {
  type: 'object',
  properties: {
    built: { type: 'boolean' }, lint_errors: { type: 'integer' }, overflow: { type: 'boolean' },
    sections: { type: 'integer' }, placeholders: { type: 'integer' },
    slices_viewed: { type: 'integer' },
    new_patterns: { type: 'array', items: { type: 'string' }, description: 'name: what, where in page CSS, why reusable' },
    open_questions: { type: 'array', items: QUESTION },
    notes: { type: 'string' },
  },
  required: ['built', 'lint_errors', 'overflow', 'sections', 'placeholders', 'slices_viewed', 'new_patterns', 'open_questions', 'notes'],
}
const REVIEW = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['pass', 'fix'] },
    score: { type: 'integer', description: '0-100 overall quality' },
    must_fix: { type: 'array', items: { type: 'string' }, description: 'section id: exact change. Blocking.' },
    should_fix: { type: 'array', items: { type: 'string' } },
    unanswered_questions: { type: 'array', items: { type: 'string' } },
    compliance_issues: { type: 'array', items: { type: 'string' } },
    slices_viewed: { type: 'integer' },
  },
  required: ['verdict', 'score', 'must_fix', 'should_fix', 'unanswered_questions', 'compliance_issues', 'slices_viewed'],
}

// one retry on a dead agent; the page is marked needs-human if it still fails
async function run(prompt, opts) {
  const r = await agent(prompt, opts)
  if (r) return r
  log(`retrying ${opts.label}`)
  return agent(prompt, { ...opts, label: opts.label + ' (retry)' })
}

const CHECK = p => `cd ${ROOT} && python3 scripts/build.py ${String(p.n).padStart(2, '0')} && python3 scripts/lint.py ${String(p.n).padStart(2, '0')}; python3 scripts/shoot.py ${String(p.n).padStart(2, '0')}`

function strategistPrompt(p) {
  const isGolden = p.mode === 'golden'
  return `${PRE}

${page(p)}

ROLE: product strategist and UX lead. Do Steps 0 to 4 of rules/page-method.md for this page and write memory/pages/${name(p)}.md from memory/pages/_TEMPLATE.md (sections 1 to 6 and 10; status: briefed).
${isGolden
  ? `This is the GOLDEN page for template ${p.template}: the other template-${p.template} pages will inherit its section layouts, so explore properly. For EVERY section give options A (baseline from memory/patterns.md / theme/sections-reference.html), B and C (structurally different), each as a 3-line wireframe spec with weighted rubric scores, and mark your provisional pick. An independent judge will challenge you next.`
  : `This is a DERIVATIVE of golden page ${p.golden_file}: read memory/pages/${p.golden_file.replace('.html', '.md')} and pages/src/${p.golden_file} first. Inherit its section layouts by default (write "inherit ${p.golden_file.slice(0, 2)} s-<id>"). Compare 2 to 3 options only for sections new to this page or where the inherited layout fails this page's questions, and say why. There is no separate judge for derivative pages: for every decision write the strongest argument against it before you keep it, then record the FINAL choice in section 6.`}
The PM question list must be specific to this page's visitors and moment in the journey; a question that would be identical on every page is not allowed unless it is one of the always-asked ones in Step 2. Include the "who am I dealing with" (entity) question on every page with a form or CTA to open an account, invest, apply or enquire.
Put every question for Aikyam or Giraffe in memory section 10 and in open_questions, with the default you used. Use ask_user only for genuine close calls that are brand or business decisions.`
}

function judgePrompt(p) {
  return `${PRE}

${page(p)}

ROLE: independent judge (senior product designer). You did not write memory/pages/${name(p)}.md: challenge it.
1. Questions: are these the ones a real visitor asks here, in that order? Add missing MUST questions, cut generic ones.
2. Traceability: every MUST question maps to a section; every section earns its place. Cut or merge the rest.
3. Layouts: re-score every section's options yourself on the rubric (rules/page-method.md) before looking at the strategist's scores, then choose. You may merge options or propose a better one. Apply the vetoes.
4. Journey: the next step is obvious; CTA labels and targets match memory/site.md and sitemap URLs; the page does not dead-end.
5. Conversion over decoration: when a prettier option and a clearer option tie, the clearer one wins.
Rewrite section 6 so it holds the FINAL decision per section (chosen option, one-line why, rejected options and why). Add "Judge ${DATE}: <summary of changes>" to the change log. If two options are within 2 weighted points and it is a brand or business call, add it to ask_user (still pick a default).`
}

function builderPrompt(p) {
  return `${PRE}

${page(p)}

ROLE: front-end builder. Build pages/src/${p.file} from memory/pages/${name(p)}.md (section 6 holds the final layout decisions) following rules/figma-html.md exactly. Reuse markup and class names from theme/sections-reference.html and memory/patterns.md${p.mode !== 'golden' ? ` and from the golden page pages/src/${p.golden_file} for inherited sections` : ''}. Mandatory blocks from rules/compliance-blocks.md by flag.
Then run: ${CHECK(p)}
Repeat until lint shows no errors and shoot shows no OVERFLOW. Then LOOK at the screenshots: review/${name(p)}/desktop-01.png and every following desktop slice, and mobile-01.png plus at least two more mobile slices. Fix anything broken, cramped, misaligned, off-theme or unreadable, and re-run the checks.
Finally fill memory sections 7 to 11 (components, new patterns, actions, compliance, open questions, designer notes), add "Built ${DATE}" to the change log, set status: built.`
}

function reviewerPrompt(p, round) {
  return `${PRE}

${page(p)}

ROLE: reviewer${round > 1 ? ' (second round: check the previous must-fixes were done and nothing regressed)' : ''}. You did not build this page. Read memory/pages/${name(p)}.md, figma/${p.file}, review/${name(p)}/lint.json and shots.json, and LOOK at every screenshot slice in review/${name(p)}/ (desktop-NN.png and mobile-NN.png).
Check in order:
1. Every MUST question in memory section 4 is visibly answered, in the order asked.
2. The primary action is clear on the first screen at 1440 and at 390, and repeated where the visitor is ready.
3. Compliance: claims rule (rules/voice-and-claims.md), the Aikyam company named at every conversion, mandatory disclosures by flag (rules/compliance-blocks.md), placeholders instead of invented values, nothing that reads as advice or a recommendation.
4. Visual quality: theme fidelity (aubergine ink, one gold spark, serif display over Mukta, Mist bands, at most one dark band), alignment, spacing rhythm, density, hierarchy, mobile stacking.
5. Figma-readiness: static, semantic section ids, no inline styles beyond custom properties, no images.
verdict "pass" only when must_fix is empty. Each must_fix names the section id and the exact change. Do not edit any file.`
}

function fixPrompt(p, rev) {
  return `${PRE}

${page(p)}

ROLE: builder, fix round. The reviewer returned these blocking fixes for pages/src/${p.file}:
${rev.must_fix.map(f => '- ' + f).join('\n')}
${rev.compliance_issues.length ? 'Compliance issues:\n' + rev.compliance_issues.map(f => '- ' + f).join('\n') : ''}
${rev.unanswered_questions.length ? 'Questions not visibly answered:\n' + rev.unanswered_questions.map(f => '- ' + f).join('\n') : ''}
Also apply these if cheap: ${rev.should_fix.join(' | ') || 'none'}.
Apply them, run: ${CHECK(p)}, look at the affected screenshot slices, and update memory (change log "Fix ${DATE}: ..."; status: built).`
}

async function finish(p, phaseName, built) {
  const lbl = name(p)
  let rev = await run(reviewerPrompt(p, 1), { label: `review ${lbl}`, phase: phaseName, schema: REVIEW })
  let fixes = null, rev2 = null
  if (rev && rev.verdict === 'fix') {
    fixes = await run(fixPrompt(p, rev), { label: `fix ${lbl}`, phase: phaseName, schema: BUILD })
    rev2 = await run(reviewerPrompt(p, 2), { label: `re-review ${lbl}`, phase: phaseName, schema: REVIEW })
  }
  const last = rev2 || rev
  return {
    page: p.file, built: !!(built && built.built), first_review: rev, final_review: last,
    status: !last ? 'needs-human' : (last.verdict === 'pass' ? 'reviewed' : 'needs-human'),
    open_questions: [...((built && built.open_questions) || []), ...((fixes && fixes.open_questions) || [])],
    new_patterns: [...((built && built.new_patterns) || []), ...((fixes && fixes.new_patterns) || [])],
  }
}

phase('Golden pages')
const goldenResults = await pipeline(
  golden,
  p => run(strategistPrompt(p), { label: `brief ${name(p)}`, phase: 'Golden pages', schema: BRIEF }),
  (brief, p) => run(judgePrompt(p), { label: `judge ${name(p)}`, phase: 'Golden pages', schema: JUDGE }).then(j => ({ brief, judge: j })),
  (bj, p) => run(builderPrompt(p), { label: `build ${name(p)}`, phase: 'Golden pages', schema: BUILD }).then(b => ({ ...bj, build: b })),
  (bjb, p) => finish(p, 'Golden pages', bjb.build).then(f => ({ ...f, brief: bjb.brief, judge: bjb.judge })),
)

let curated = null
const goldenWithPatterns = goldenResults.filter(Boolean).filter(r => r.new_patterns.length)
if (goldenWithPatterns.length) {
  phase('Curate')
  curated = await run(`${PRE}

ROLE: pattern curator (you act for the orchestrator, so for this task you MAY edit theme/patterns.css and memory/patterns.md).
Golden pages just built and their proposed new patterns:
${goldenWithPatterns.map(r => `- ${r.page}: ${r.new_patterns.join(' | ')}`).join('\n')}
For each proposal that is genuinely reusable on other pages: move its CSS from the page's <style data-page> block into theme/patterns.css (tokens only, a comment naming the source page), remove it from the page source, add a row to memory/patterns.md (pattern, root class, specs, reuse on, source). Leave one-off CSS in the page.
Then rebuild and re-check each touched page (python3 scripts/build.py NN && python3 scripts/lint.py NN; python3 scripts/shoot.py NN) and confirm lint errors and overflow are still zero and the slice count did not change. Return a short list of promoted patterns and anything you declined.`, { label: 'curate patterns', phase: 'Curate' })
}

phase('Derivative pages')
const derivedResults = await pipeline(
  derived,
  p => run(strategistPrompt(p), { label: `brief ${name(p)}`, phase: 'Derivative pages', schema: BRIEF }),
  (brief, p) => run(builderPrompt(p), { label: `build ${name(p)}`, phase: 'Derivative pages', schema: BUILD }).then(b => ({ brief, build: b })),
  (bb, p) => finish(p, 'Derivative pages', bb.build).then(f => ({ ...f, brief: bb.brief })),
)

const all = [...goldenResults, ...derivedResults]
const dropped = PAGES.filter((p, i) => !all[i]).map(p => p.file)
if (dropped.length) log(`pages that failed outright: ${dropped.join(', ')}`)
return {
  pages: all.filter(Boolean).map(r => ({
    page: r.page, status: r.status,
    score_first: r.first_review && r.first_review.score, score_final: r.final_review && r.final_review.score,
    remaining_must_fix: r.final_review ? r.final_review.must_fix : ['no review'],
    open_questions: [...((r.brief && r.brief.open_questions) || []), ...r.open_questions],
    ask_user: [...((r.brief && r.brief.ask_user) || []), ...((r.judge && r.judge.ask_user) || [])],
    site_proposals: (r.brief && r.brief.site_proposals) || [],
    judge: r.judge ? { changed: r.judge.changed_decisions, confidence: r.judge.confidence } : null,
  })),
  failed: dropped,
  curated,
}
