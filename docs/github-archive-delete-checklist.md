# GitHub Archive/Delete Review Checklist

Generated: 2026-05-25

This checklist is intentionally conservative. No repos should be deleted without Corbyn approving them one-by-one.

## Recommended active/keep

- [ ] `Falkurne/project-update-reports`
  - Action: keep
  - Reason: active reporting hub and automation.
- [ ] `Falkurne/Motofi`
  - Action: keep/rename to `client-motofi-marketplace`
  - Reason: active paid marketplace MVP.
- [ ] `Falkurne/eastpoint-finance-landing`
  - Action: keep/rename to `client-eloanz-landing`
  - Reason: active paid ELoanz website work.
- [ ] `Falkurne/gw2-legendary-tracker`
  - Action: keep/rename if First Legendary remains active.
- [ ] `Falkurne/Corbyn.net-Website`
  - Action: keep/rename to `personal-corbyn-net`.
- [ ] `Falkurne/command-center`
  - Action: keep/rename to `personal-command-center` if still useful.

## Recommended archive first

Archive means retained but read-only/out of the way.

- [ ] `Falkurne/TGS-Website`
  - Size: ~50 MB
  - Reason: historical TGS site; keep only as reference unless Corbyn wants deletion.
- [ ] `Falkurne/openclaw-tgs`
  - Size: ~99 MB
  - Reason: TGS-related agent setup; archive preferred before deletion because it is large and likely contains environment/context history.
- [ ] `Falkurne/openclaw-personal`
  - Size: tiny
  - Reason: old agent setup; archive unless superseded and no longer useful.
- [ ] `Falkurne/eff-mobile-app`
  - Reason: old EFF app/client project; archive unless client relationship/work is still active.
- [ ] `Falkurne/Shopify-OnfarmHarvest`
  - Reason: old OnFarm Harvest/Shopify family; archive unless definitely disposable.
- [ ] `Falkurne/Shopify-OnFarmHarvest---Dawn-Theme`
  - Reason: theme repo; archive unless definitely disposable.
- [ ] `Falkurne/OFH-CONVEX`
  - Reason: OnFarm Harvest backend/app family; archive unless definitely disposable.
- [ ] `Falkurne/OFH-ST`
  - Reason: OnFarm Harvest app/theme family; archive unless definitely disposable.
- [ ] `Falkurne/5055482-Corbyn-Ridler-BIT706-Assignment1`
  - Reason: assignment archive/sentimental/reference value only.
- [ ] `Falkurne/5055482-Corbyn-Ridler-BIT706-Assignment2`
  - Reason: assignment archive/sentimental/reference value only.
- [ ] `Falkurne/BIT504_AT2_TaskB`
  - Reason: assignment archive/sentimental/reference value only.

## Strong delete candidates after confirmation

These look empty, duplicate, tiny, or generated. Confirm before deleting.

- [ ] `Falkurne/O2D-Chat`
  - Size: 0 KB
  - Reason: likely empty shell or duplicate of `O2D-Chat-mvp`.
- [ ] `Falkurne/TGS_Brandy-in-Marketing`
  - Size: 0 KB
  - Reason: likely empty/historical TGS repo.
- [ ] `Falkurne/TGS`
  - Size: 0 KB
  - Reason: likely empty/historical TGS repo.
- [ ] `Falkurne/Fal-Default`
  - Size: 0 KB
  - Reason: likely generated/default placeholder.
- [ ] `Falkurne/knowledge`
  - Size: 0 KB
  - Reason: likely empty; keep only if it has non-GitHub-linked value elsewhere.
- [ ] `Falkurne/Warp-Oz-Cloud-Agent`
  - Size: ~1 KB
  - Reason: tiny infrastructure experiment; inspect before deleting.
- [ ] `Falkurne/antigravity-trigger-dev-main`
  - Size: ~137 KB
  - Reason: likely generated experiment/scaffold; inspect before deleting.
- [ ] `Falkurne/vol`
  - Size: ~107 KB
  - Reason: old C++ repo; likely delete unless personally meaningful.

## Needs Corbyn decision

- [ ] `Falkurne/O2D-Chat-mvp`
  - Size: ~5.3 MB
  - Action: keep/rename to `product-o2d-chat-mvp`, archive, or delete depending whether the idea is still alive.
- [ ] `Falkurne/Gaming`
  - Size: ~19 KB
  - Action: keep if useful for gaming/server notes; otherwise archive/delete.

## Safe execution order

1. Archive confirmed historical repos first.
2. Rename active keepers after reporting source maps are ready to update.
3. Re-check local clones under `~/Projects` and update remotes.
4. Delete only repos Corbyn explicitly marks from the strong delete candidates list.

## Commands after approval

Archive:

```bash
gh repo archive Falkurne/<repo> --yes
```

Delete:

```bash
gh repo delete Falkurne/<repo> --yes
```

Rename:

```bash
gh repo rename <new-name> --repo Falkurne/<old-name>
```
