# HANDOVER.md

Överlämning mellan agenter och sessioner. Läs innan du börjar, uppdatera innan du slutar.

## Aktuellt läge

*Senast inventerat 2026-11-04 av Claude (Cowork).*

Projekt: Build infrastructure dependency graphs, calculate failure blast radius, and find single points of failure before an outage does.

- Huvudbranch: `main`
- Senaste commit på `main`: 2026-11-01 `98c9cc8` Add privacy guard for local hooks and CI (#2)
- Öppna PR:er: 0
- Andra brancher på remote: 2

## Pågående arbete

| Agent/vem | Branch | Status | Beskrivning |
|-----------|--------|--------|-------------|
| Cursor | `cursor/privacy-guard-e2fd` | branch utan PR, senaste commit 2026-11-01 | Add privacy guard for local hooks and CI |
| okänd (människa/agent) | `agent/dependency-impact-engine` | branch utan PR, senaste commit 2026-07-18 | Document InfraGraph impact analysis |

## Nästa steg

- Gå igenom brancher utan PR: öppna PR, merga eller radera (fråga användaren innan radering).
- Fyll på "Bygga och testa" i AGENTS.md om något saknas eller är fel.

## Kända problem

- Inga dokumenterade ännu.

## Senaste commits

- 2026-11-01 `98c9cc8` Add privacy guard for local hooks and CI (#2)
- 2026-10-26 `0f09b2e` docs: add contributor guide for layout, conventions and edge direction
- 2026-10-26 `90483a6` test: fail when the README impact example drifts from real output
- 2026-10-26 `0c5ddc0` docs: correct README example and document exit codes, fields and topology
- 2026-10-26 `0ec0ea1` test: cover CLI exit codes, error output and mermaid export
- 2026-10-26 `0ac6716` fix: report unknown nodes and invalid inventory fields cleanly in the CLI
- 2026-10-26 `edef25b` feat: ignore optional dependencies when computing blast radius
- 2026-10-26 `4c8d1fc` ci: test on Python 3.13
- 2026-10-26 `7623440` build: pin ruff lint rule set and wrap long lines
- 2026-10-26 `85d8112` style: apply ruff fixes for UP035, UP037 and I001

## Logg

| Datum | Agent | Vad som gjordes |
|-------|-------|-----------------|
| 2026-11-04 | Claude (Cowork) | Lade till AGENTS.md, HANDOVER.md och CLAUDE.md; inventerade PR:er, brancher och commits. |
