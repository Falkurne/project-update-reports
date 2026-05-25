# GitHub Repository Cleanup Plan

Generated: 2026-05-25

This is a safe plan only. Do not rename/archive repos until Corbyn approves the exact map.

## Naming convention

`<area>-<client-or-project>-<purpose>`

Areas:

- `client-` — paid client work
- `product-` — products/SaaS/passion products
- `personal-` — portfolio, personal systems, life admin
- `archive-` — historical/stale work retained for reference
- `learning-` — assignments/courses/experiments
- `infra-` — reusable infrastructure or tooling
- `internal-` — Corbyn business/admin/workflow systems

## Approved-to-propose rename map

### Active paid/client work

- `Falkurne/Motofi` → `client-motofi-marketplace`
  - Current language: Python
  - Status: active paid MVP planning/build
  - Risk: update local remote at `/home/falkae/Projects/Motofi`
- `Falkurne/eastpoint-finance-landing` → `client-eloanz-landing`
  - Current language: HTML
  - Status: active client website
  - Risk: update Linear/GitHub references and local clone if present
- `Falkurne/project-update-reports` → keep as `project-update-reports` for now, or later `client-project-update-reports`
  - Public static hub
  - Keep current name until the automation is stable and deployed

### Personal/product work

- `gw2-legendary-tracker` → `product-first-legendary` or `product-gw2-legendary-tracker`
- `Corbyn.net-Website` → `personal-corbyn-net`
- `command-center` → `personal-command-center`
- `knowledge` → `personal-knowledge`
- `Gaming` → `personal-gaming`
- `Fal-Default` → `personal-fal-default` or archive after inspection

### Archive/TGS cleanup

Corbyn no longer works with TGS and does not want Hermes connected to or relying on TGS infrastructure. These should be archived/renamed for historical reference only:

- `TGS-Website` → `archive-tgs-website`
- `openclaw-tgs` → `archive-openclaw-tgs`
- `openclaw-personal` → `archive-openclaw-personal`
- `TGS_Brandy-in-Marketing` → `archive-tgs-brandy-marketing`
- `TGS` → `archive-tgs`

### Learning/archive

- `5055482-Corbyn-Ridler-BIT706-Assignment1` → `learning-bit706-assignment-1`
- `5055482-Corbyn-Ridler-BIT706-Assignment2` → `learning-bit706-assignment-2`
- `BIT504_AT2_TaskB` → `learning-bit504-task-b`
- `vol` → `archive-vol` unless still needed

### Needs inspection before naming

- `O2D-Chat` / `O2D-Chat-mvp`
  - If alive: `product-o2d-chat` / `product-o2d-chat-mvp`
  - If stale: `archive-o2d-chat` / `archive-o2d-chat-mvp`
- `Warp-Oz-Cloud-Agent`
  - likely `infra-warp-oz-cloud-agent` or archive
- `antigravity-trigger-dev-main`
  - likely archive/experiment
- `eff-mobile-app`
  - likely `client-eff-mobile-app` if still client-relevant; otherwise archive
- `Shopify-OnfarmHarvest`
- `Shopify-OnFarmHarvest---Dawn-Theme`
- `OFH-CONVEX`
- `OFH-ST`
  - likely OnFarm Harvest client/archive family; inspect before rename

## Execution steps after approval

1. Rename lowest-risk archive repos first using `gh repo rename`.
2. For any local clones under `~/Projects`, update remotes:

```bash
git remote set-url origin git@github.com:Falkurne/<new-name>.git
```

3. Add topics to active repos:

- `client-work`
- `motofi` / `eloanz`
- `linear-managed`
- `hermes-managed`

4. Archive repos that are truly historical after confirming no active dependencies.
5. Re-run this report and update the map with final names.
