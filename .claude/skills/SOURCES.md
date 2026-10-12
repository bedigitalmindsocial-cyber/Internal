# Project skills: sources

Design skills copied from public GitHub repos so every cloud session on this repo can use them. Each folder keeps its upstream LICENSE.

| Skill | Upstream | Commit | License |
|---|---|---|---|
| impeccable (plus 4 subagents in `.claude/agents/impeccable-*.md`) | github.com/pbakaus/impeccable, path `.claude/skills/impeccable` | c63b8dd (skill v4.5.2) | Apache 2.0 |
| better-ui | github.com/jakubkrehel/skills, path `skills/better-ui` | c0588bb | MIT |
| better-colors | github.com/jakubkrehel/skills, path `skills/better-colors` | c0588bb | MIT |
| better-layout | github.com/jakubkrehel/skills, path `skills/better-layout` | c0588bb | MIT |
| design-motion-principles | github.com/kylezantos/design-motion-principles, path `skills/design-motion-principles` | 4a9ca87 | MIT |

Notes:

- Impeccable's upstream `.claude/settings.json` hooks (SessionStart, PostToolUse on every Edit/Write, Stop) are NOT installed. They run the Impeccable engine binary on every edit, which this Python repo does not need. The skill works without them.
- The Impeccable launcher (`scripts/impeccable`) downloads its engine from GitHub Releases on first run and verifies a SHA-256 checksum. If the cloud network policy blocks the download, the skill falls back to reading PRODUCT.md and DESIGN.md directly.
- To update: re-copy the same paths from the upstream repo and bump the commit column.
