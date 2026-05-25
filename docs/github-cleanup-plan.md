# GitHub Repository Cleanup Plan

Generated: 2026-05-25

This is a safe plan only. Do not rename, archive, or delete repos until Corbyn approves the exact map.

Corbyn noted that many repositories will likely be archived or deleted, not just renamed. Treat cleanup as a triage process with three possible actions:

- **Keep/rename:** active or valuable repos that should remain visible and well named.
- **Archive:** historical repos that may still contain useful reference material, but should be read-only/out of the way.
- **Delete candidate:** disposable experiments, duplicates, generated scaffolds, or repos with no future value. Deletion is irreversible enough that these require a separate explicit approval pass.

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

## Triage actions by repo

### Keep/rename first

- `Falkurne/Motofi` → `client-motofi-marketplace`
  - Action: keep/rename
  - Reason: active paid MVP planning/build.
  - Current language: Python
  - Risk: update local remote at `/home/falkae/Projects/Motofi` and reporting source map.
- `Falkurne/eastpoint-finance-landing` → `client-eloanz-landing`
  - Action: keep/rename
  - Reason: active client website.
  - Current language: HTML
  - Risk: update Linear/GitHub references, reporting source map, and local clone if present.
- `Falkurne/project-update-reports` → keep as `project-update-reports` for now
  - Action: keep
  - Reason: active reporting automation/hub.
  - Revisit later: possibly rename to `client-project-update-reports` after automation is stable.

### Keep/rename or archive after quick inspection

- `gw2-legendary-tracker` → `product-first-legendary` or `product-gw2-legendary-tracker`
  - Likely action: keep/rename
- `Corbyn.net-Website` → `personal-corbyn-net`
  - Likely action: keep/rename
- `command-center` → `personal-command-center`
  - Likely action: keep/rename
- `knowledge` → `personal-knowledge`
  - Likely action: keep/rename or archive depending on contents
- `Gaming` → `personal-gaming`
  - Likely action: archive unless actively used
- `Fal-Default` → `personal-fal-default`
  - Likely action: inspect; probably archive/delete candidate if it is generated/default scaffolding

### Archive candidates

Corbyn no longer works with TGS and does not want Hermes connected to or relying on TGS infrastructure. These should be archived unless Corbyn explicitly chooses deletion:

- `TGS-Website` → `archive-tgs-website`
- `openclaw-tgs` → `archive-openclaw-tgs`
- `openclaw-personal` → `archive-openclaw-personal`
- `TGS_Brandy-in-Marketing` → `archive-tgs-brandy-marketing`
- `TGS` → `archive-tgs`

### Learning archive or delete candidates

- `5055482-Corbyn-Ridler-BIT706-Assignment1` → `learning-bit706-assignment-1`
  - Likely action: archive after rename, or delete if no sentimental/reference value.
- `5055482-Corbyn-Ridler-BIT706-Assignment2` → `learning-bit706-assignment-2`
  - Likely action: archive after rename, or delete if no sentimental/reference value.
- `BIT504_AT2_TaskB` → `learning-bit504-task-b`
  - Likely action: archive after rename, or delete if no sentimental/reference value.
- `vol` → `archive-vol`
  - Likely action: delete candidate unless contents are useful.

### Needs inspection before deciding keep/archive/delete

- `O2D-Chat` / `O2D-Chat-mvp`
  - If alive: `product-o2d-chat` / `product-o2d-chat-mvp`
  - If stale: archive or delete duplicate/empty repo.
- `Warp-Oz-Cloud-Agent`
  - likely `infra-warp-oz-cloud-agent`, archive, or delete candidate.
- `antigravity-trigger-dev-main`
  - likely archive/delete candidate.
- `eff-mobile-app`
  - likely `client-eff-mobile-app` if still client-relevant; otherwise archive.
- `Shopify-OnfarmHarvest`
- `Shopify-OnFarmHarvest---Dawn-Theme`
- `OFH-CONVEX`
- `OFH-ST`
  - likely OnFarm Harvest client/archive family; inspect before deciding.

## Execution steps after approval

1. Do an inspection pass for all uncertain repos and mark each as `keep`, `archive`, or `delete candidate`.
2. Rename lowest-risk keep/archive repos first using `gh repo rename`.
3. For any local clones under `~/Projects`, update remotes:

```bash
git remote set-url origin git@github.com:Falkurne/<new-name>.git
```

4. Add topics to active repos:

- `client-work`
- `motofi` / `eloanz`
- `linear-managed`
- `hermes-managed`

5. Archive repos that are confirmed historical but still worth retaining.
6. Produce a separate delete-candidate checklist for Corbyn to approve one-by-one.
7. Only after explicit approval, delete selected repos using `gh repo delete OWNER/REPO --yes`.
8. Re-run this report and update the map with final names/statuses.
