# Project update reports

Static hub for HTML progress updates across client projects. Built for Vercel hosting with no build step.

## Location

```
c:\Users\Corbyn\A_Repo\client_All_Project-Reports
```

This folder sits outside the ELoanz workspace so update reports can live in their own repo.

## Structure

```
client_All_Project-Reports/
  index.html              Homepage with search, filters, and sorting
  data/
    projects.json         Project categories and report types
    updates.json          Catalog of all HTML reports
  updates/
    eloanz/               Reports for the ELoanz website project
      2026-05-20-stakeholder-update.html
  vercel.json
```

## Add a new report manually

1. Save the HTML file under `updates/<project-id>/`, using a date prefix in the filename.
2. Add an entry to `data/updates.json`.
3. If this is a new project, add it to `data/projects.json`.

## Generate a draft report from Linear + GitHub

```bash
cd /home/falkae/Projects/client_All_Project-Reports
python3 scripts/generate_update.py --write
```

Options:

```bash
python3 scripts/generate_update.py --project eloanz --lookback-days 2 --write
python3 scripts/generate_update.py --project motofi --lookback-days 7 --write
```

The generator is draft-only by convention: it writes HTML and updates the catalog, but it does not commit, push, deploy, or send anything to clients.

Source mapping lives in `data/reporting-sources.json`.


Example `updates.json` entry:

```json
{
  "id": "eloanz-2026-05-20-stakeholder",
  "projectId": "eloanz",
  "title": "ELoanz website progress update",
  "date": "2026-05-20",
  "category": "stakeholder-update",
  "summary": "Short one-line summary for the homepage card.",
  "path": "/updates/eloanz/2026-05-20-stakeholder-update.html",
  "audience": "Freddie and stakeholders",
  "tags": ["launch", "lead-capture"]
}
```

## Categories

Defined in `data/projects.json`:

| ID | Label |
|----|-------|
| `stakeholder-update` | Stakeholder update |
| `progress-report` | Progress report |
| `meeting-prep` | Meeting prep |
| `technical-note` | Technical note |
| `ui-mockup` | UI mockup |

## Projects in catalog

| ID | Project |
|----|---------|
| `eloanz` | ELoanz Website |
| `motofi` | Motofi Marketplace |

## Local preview

```bash
cd "c:\Users\Corbyn\A_Repo\client_All_Project-Reports"
npx --yes serve .
```

Open `http://localhost:3000`.

## Deploy to Vercel

1. Create a new GitHub repo (for example `client_All_Project-Reports`).
2. Push this folder:

```bash
cd "c:\Users\Corbyn\A_Repo\client_All_Project-Reports"
git add .
git commit -m "Initial project update reports hub"
git remote add origin https://github.com/YOUR_USER/client_All_Project-Reports.git
git push -u origin main
```

3. In Vercel: **Add New Project** → import the repo.
4. Framework preset: **Other** (static HTML, no build command).
5. Output directory: `.` (root).
6. Deploy.

Or use the Vercel CLI:

```bash
npm i -g vercel
cd "c:\Users\Corbyn\A_Repo\client_All_Project-Reports"
vercel
```

## Move files from the ELoanz repo

The first report was copied from:

`docs/stakeholder-update.html` in the ELoanz landing page repo.

You can remove that file from the ELoanz repo once this hub is live, or keep it as a local working copy.
