#!/usr/bin/env python3
"""Generate draft stakeholder update reports from Linear + GitHub activity.

Default behaviour is safe/draft-only:
- writes an HTML report under updates/<project>/
- prepends an entry to data/updates.json
- does not commit, push, or send to clients

The report intentionally has two layers:
1. a client-readable summary with cleaned wording;
2. a technical source appendix for Corbyn's review.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import pathlib
import re
import subprocess
from collections import Counter
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES_PATH = ROOT / "data" / "reporting-sources.json"
UPDATES_PATH = ROOT / "data" / "updates.json"

NOISY_COMMIT_PREFIXES = (
    "merge pull request",
    "merge branch",
    "wip",
)

TYPO_FIXES = {
    "gradiant": "gradient",
    "imrpove": "improve",
    "shouldnt": "shouldn't",
    "doesnt": "doesn't",
    "isnt": "isn't",
    "whats": "what's",
    "exmaple": "example",
    "monochome": "monochrome",
    "questionaire": "questionnaire",
    "chnage": "change",
    "alot": "a lot",
    "brokeridge": "brokerage",
    "fianance": "finance",
}

THEME_KEYWORDS = {
    "Lead capture and enquiry flow": ["form", "input", "email", "phone", "date of birth", "number plate", "tickbox", "validation", "enquiry"],
    "Design polish and page layout": ["hero", "gradient", "padding", "photo", "cards", "slider", "navbar", "section", "background", "monochrome", "white box", "orange", "footer", "logo"],
    "Trust, content, and compliance": ["compliance", "faq", "testimonials", "pros and cons", "banks", "lenders", "eastpoint", "mike", "trading name", "knowledge"],
    "Marketplace planning and build setup": ["mvp", "brief", "planning", "marketplace", "broker", "dealer", "dashboard", "infrastructure", "convex", "clerk", "vercel"],
}


def run(cmd: list[str], *, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(cmd, cwd=str(cwd) if cwd else None, text=True).strip()


def iso_z(d: dt.datetime) -> str:
    return d.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: pathlib.Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: pathlib.Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def linear_graphql(query: str, variables: dict | None = None) -> dict:
    key = os.environ.get("LINEAR_API_KEY")
    if not key:
        raise RuntimeError("LINEAR_API_KEY is not set")
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = Request(
        "https://api.linear.app/graphql",
        data=payload,
        headers={"Authorization": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=30) as res:
            data = json.loads(res.read().decode())
    except HTTPError as exc:
        body = exc.read().decode(errors="replace")
        raise RuntimeError(f"Linear API HTTP {exc.code}: {body}") from exc
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], indent=2))
    return data["data"]


def fetch_linear_issues(project_name: str, since: str) -> list[dict]:
    query = """
    query($project: String!, $since: DateTimeOrDuration!) {
      issues(
        first: 100,
        filter: {
          project: { name: { eq: $project } },
          updatedAt: { gte: $since }
        }
      ) {
        nodes {
          identifier title updatedAt priority url
          state { name type }
          labels { nodes { name } }
          assignee { name }
        }
      }
    }
    """
    return linear_graphql(query, {"project": project_name, "since": since})["issues"]["nodes"]


def fetch_commits(repo: str, since: str) -> list[dict]:
    try:
        raw = run([
            "gh", "api", "--method", "GET", f"repos/{repo}/commits",
            "-f", f"since={since}",
            "--jq", ".[] | {sha: .sha, url: .html_url, message: .commit.message, date: .commit.author.date, author: .commit.author.name}"
        ])
    except subprocess.CalledProcessError:
        return []
    commits = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        commit = json.loads(line)
        first = commit["message"].splitlines()[0].strip()
        if first.lower().startswith(NOISY_COMMIT_PREFIXES):
            continue
        commits.append(commit)
    return commits


def clean_text(value: str) -> str:
    text = value.strip()
    text = re.sub(r"\s+", " ", text)
    for wrong, right in TYPO_FIXES.items():
        text = re.sub(rf"\b{re.escape(wrong)}\b", right, text, flags=re.IGNORECASE)
    text = text.strip(" .")
    if text:
        text = text[0].upper() + text[1:]
    return text


def phrase_from_issue(issue: dict) -> str:
    title = clean_text(issue["title"])
    lower = title.lower()

    patterns = [
        (r"we will be in touch|center and change to be more friendly", "Improved the confirmation message so it feels more friendly and reassuring"),
        (r"delete this step", "Removed an unnecessary step from the enquiry flow"),
        (r"^can you add an option.*number plate input", "Added a conditional number plate field for vehicle enquiry paths that need it"),
        (r"^enable the style preview modal", "Made the style preview available across the site instead of hiding it behind a special URL"),
        (r"phone number validation", "Fixed phone number validation in the enquiry flow"),
        (r"slider", "Improved the repayment/term slider so the range and selection feel clearer"),
        (r"date of birth", "Changed the relevant form step to collect date of birth details"),
        (r"promotional communications", "Updated the promotional communications checkbox behaviour"),
        (r"email to send a summary", "Clarified the email collection step for enquiry summaries"),
        (r"logo.*navbar|navbar.*logo", "Cleaned up the form navigation and centred the ELoanz logo"),
        (r"remove this subheader", "Removed an unnecessary subheader from the form experience"),
        (r"eastpoint|mike", "Removed internal/Eastpoint/Mike references from client-facing copy"),
        (r"faq", "Reworked the FAQ area into a clean placeholder structure for later content"),
        (r"testimonials", "Started the testimonials/social proof section"),
        (r"compliance|knowledge", "Progressed the compliance wording review and site-change checklist"),
        (r"hero.*gradient|gradient", "Polished the hero background and transition into the page"),
        (r"collaboration", "Started the collaboration/partner-style content section below the hero"),
        (r"html brief|brief", "Updated the HTML project brief for stakeholder review"),
    ]
    for pattern, replacement in patterns:
        if re.search(pattern, lower):
            return replacement

    # Remove request-style phrasing that should not go to clients.
    title = re.sub(r"^(can you|please|i want to|change|add|remove|delete|fix|move)\s+", "", title, flags=re.IGNORECASE)
    title = title.strip(" .")
    if title:
        return title[0].upper() + title[1:]
    return "Tracked project update"


def phrase_from_commit(commit: dict) -> str:
    first = clean_text(commit["message"].splitlines()[0])
    first = re.sub(r"^docs\([^)]*\):\s*", "Documented ", first, flags=re.IGNORECASE)
    first = re.sub(r"^docs:\s*", "Documented ", first, flags=re.IGNORECASE)
    first = re.sub(r"^feat\([^)]*\):\s*", "Added ", first, flags=re.IGNORECASE)
    first = re.sub(r"^feat:\s*", "Added ", first, flags=re.IGNORECASE)
    first = re.sub(r"^fix\([^)]*\):\s*", "Fixed ", first, flags=re.IGNORECASE)
    first = re.sub(r"^fix:\s*", "Fixed ", first, flags=re.IGNORECASE)
    first = re.sub(r"\s*\(FAL-\d+\)", "", first)
    return first or "Repository update"


def sentence(value: str) -> str:
    value = value.strip()
    if not value:
        return value
    return value if value.endswith(('.', '!', '?')) else value + "."


def labels_for(issue: dict) -> set[str]:
    return {l["name"] for l in issue.get("labels", {}).get("nodes", [])}


def issue_theme(issue: dict) -> str:
    haystack = f"{issue['title']} {' '.join(labels_for(issue))}".lower()
    for theme, keywords in THEME_KEYWORDS.items():
        if any(k in haystack for k in keywords):
            return theme
    return "General delivery"


def group_themes(issues: list[dict], commits: list[dict]) -> list[tuple[str, int]]:
    counter = Counter(issue_theme(issue) for issue in issues)
    for commit in commits:
        msg = commit["message"].lower()
        matched = False
        for theme, keywords in THEME_KEYWORDS.items():
            if any(k in msg for k in keywords):
                counter[theme] += 1
                matched = True
                break
        if not matched:
            counter["General delivery"] += 1
    return counter.most_common()


def unique(items: list[str], limit: int | None = None) -> list[str]:
    seen = set()
    out = []
    for item in items:
        item = sentence(item)
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
        if limit and len(out) >= limit:
            break
    return out


def build_sections(project: dict, issues: list[dict], commits_by_repo: dict[str, list[dict]]) -> dict[str, list[str]]:
    commits = [c for commits in commits_by_repo.values() for c in commits]
    completed = [i for i in issues if i["state"]["type"] == "completed"]
    active = [i for i in issues if i["state"]["type"] == "started"]
    blocked = [i for i in issues if "blocked" in labels_for(i)]

    theme_lines = []
    for theme, count in group_themes(issues, commits)[:4]:
        if theme == "General delivery" and count < 2:
            continue
        theme_lines.append(f"{theme}: {count} tracked update{'s' if count != 1 else ''}")

    changed = unique([phrase_from_issue(i) for i in completed] + [phrase_from_commit(c) for c in commits], limit=10)
    progress = unique([phrase_from_issue(i) for i in active], limit=8)
    blockers = unique([phrase_from_issue(i) for i in blocked], limit=6)

    if not blockers:
        blockers = ["No blocked items are currently tagged in Linear."]

    if progress:
        next_steps = [f"Continue review/build on: {p.rstrip('.')}" for p in progress[:4]]
    elif project["id"] == "motofi":
        next_steps = ["Move the MVP brief into small build tickets for the first scaffold and workflow screens."]
    else:
        next_steps = ["Continue final polish, compliance review, and launch-readiness checks."]

    def plural(count: int, singular: str, plural_word: str | None = None) -> str:
        return singular if count == 1 else (plural_word or singular + "s")

    summary = []
    if changed:
        summary.append(f"{project['displayName']} had {len(changed)} client-relevant tracked {plural(len(changed), 'update')} in this window.")
    else:
        summary.append(f"No completed client-facing changes were detected for {project['displayName']} in this window.")
    summary.extend(theme_lines[:3])
    if progress:
        summary.append(f"There {'is' if len(progress) == 1 else 'are'} {len(progress)} active {plural(len(progress), 'item')} still in progress or review.")

    return {
        "summary": unique(summary, limit=6),
        "changed": changed or ["No completed changes were detected yet."],
        "progress": progress or ["Nothing is marked as in progress/review in Linear."],
        "blockers": blockers,
        "next_steps": unique(next_steps, limit=5),
    }


def render_list(items: list[str], empty: str) -> str:
    if not items:
        return f"<li>{html.escape(empty)}</li>"
    return "\n".join(f"<li>{html.escape(sentence(x))}</li>" for x in items)


def render_report(project: dict, since_local: dt.datetime, now_local: dt.datetime, issues: list[dict], commits_by_repo: dict[str, list[dict]]) -> str:
    sections = build_sections(project, issues, commits_by_repo)
    issue_link_items = [f'{i["identifier"]}: {clean_text(i["title"])} ({i["state"]["name"]})' for i in issues]
    repo_items = []
    for repo, commits in commits_by_repo.items():
        for c in commits:
            repo_items.append(f'{repo}@{c["sha"][:7]} — {phrase_from_commit(c)}')

    title = f"{project['displayName']} update — {now_local:%d %b %Y}"
    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>{html.escape(title)}</title>
  <style>
    body {{ margin: 0; font-family: Inter, Segoe UI, system-ui, sans-serif; color: #14201c; background: #f2f5f4; line-height: 1.6; }}
    .page {{ max-width: 900px; margin: 0 auto; padding: 32px 20px 56px; }}
    .hero {{ background: linear-gradient(145deg, #07141c, #0f2a36 60%, #08785d 130%); color: white; border-radius: 16px; padding: 32px; box-shadow: 0 16px 40px rgba(7,20,28,.1); }}
    .label {{ text-transform: uppercase; letter-spacing: .12em; opacity: .72; font-weight: 800; font-size: 12px; }}
    h1 {{ margin: 8px 0 8px; font-size: clamp(28px, 5vw, 42px); line-height: 1.1; }}
    h2 {{ margin-top: 28px; }}
    section {{ background: white; margin-top: 18px; padding: 22px; border: 1px solid #d8e3de; border-radius: 14px; }}
    .meta {{ color: #5a6a64; }}
    li {{ margin: 7px 0; }}
    .draft {{ display: inline-block; margin-top: 10px; padding: 4px 10px; border-radius: 999px; background: #fff3cd; color: #6b4e00; font-weight: 700; }}
    details {{ margin-top: 18px; }}
    summary {{ cursor: pointer; font-weight: 800; }}
  </style>
</head>
<body>
  <main class=\"page\">
    <header class=\"hero\">
      <div class=\"label\">Draft stakeholder update</div>
      <h1>{html.escape(title)}</h1>
      <p>Audience: {html.escape(project['clientAudience'])}. Generated from Linear and GitHub activity between {since_local:%d %b %Y %H:%M} and {now_local:%d %b %Y %H:%M} NZ time.</p>
      <span class=\"draft\">Draft for Corbyn review — not client-sent</span>
    </header>

    <section>
      <h2>Plain-language summary</h2>
      <ul>{render_list(sections['summary'], 'No tracked activity found in this reporting window.')}</ul>
    </section>

    <section>
      <h2>What changed</h2>
      <ul>{render_list(sections['changed'], 'No completed changes were detected yet.')}</ul>
    </section>

    <section>
      <h2>Currently in progress</h2>
      <ul>{render_list(sections['progress'], 'Nothing is marked as in progress/review in Linear.')}</ul>
    </section>

    <section>
      <h2>Next</h2>
      <ul>{render_list(sections['next_steps'], 'Confirm priorities for the next work window.')}</ul>
    </section>

    <section>
      <h2>Blockers / decisions needed</h2>
      <ul>{render_list(sections['blockers'], 'No blocked items were tagged in Linear.')}</ul>
    </section>

    <section>
      <h2>Source activity for Corbyn</h2>
      <p class=\"meta\">This appendix is for review, not necessarily for clients.</p>
      <details open>
        <summary>Linear issues</summary>
        <ul>{render_list(issue_link_items, 'No Linear issue changes found.')}</ul>
      </details>
      <details>
        <summary>GitHub commits</summary>
        <ul>{render_list(repo_items, 'No GitHub commits found.')}</ul>
      </details>
    </section>
  </main>
</body>
</html>
"""


def prepend_update_entry(entry: dict) -> None:
    data = load_json(UPDATES_PATH)
    data["updates"] = [u for u in data["updates"] if u["id"] != entry["id"]]
    data["updates"].insert(0, entry)
    save_json(UPDATES_PATH, data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", choices=["all", "eloanz", "motofi"], default="all")
    parser.add_argument("--lookback-days", type=int)
    parser.add_argument("--write", action="store_true", help="write report files and update data/updates.json")
    args = parser.parse_args()

    sources = load_json(SOURCES_PATH)
    lookback = args.lookback_days or sources["reporting"]["defaultLookbackDays"]
    now_utc = dt.datetime.now(dt.timezone.utc)
    since_utc = now_utc - dt.timedelta(days=lookback)
    try:
        from zoneinfo import ZoneInfo
        nz = ZoneInfo(sources["reporting"].get("timezone", "Pacific/Auckland"))
    except Exception:
        nz = dt.timezone(dt.timedelta(hours=12))
    now_local = now_utc.astimezone(nz)
    since_local = since_utc.astimezone(nz)

    generated = []
    for project in sources["projects"]:
        if args.project != "all" and project["id"] != args.project:
            continue
        issues = fetch_linear_issues(project["linearProject"], iso_z(since_utc))
        commits_by_repo = {repo: fetch_commits(repo, iso_z(since_utc)) for repo in project["githubRepos"]}
        html_doc = render_report(project, since_local, now_local, issues, commits_by_repo)
        date_slug = now_local.strftime("%Y-%m-%d")
        report_id = f"{project['id']}-{date_slug}-auto-update"
        rel_path = pathlib.Path("updates") / project["id"] / f"{date_slug}-auto-update.html"
        out_path = ROOT / rel_path
        total_commits = sum(len(v) for v in commits_by_repo.values())
        entry = {
            "id": report_id,
            "projectId": project["id"],
            "title": f"{project['displayName']} auto-generated progress update",
            "date": date_slug,
            "category": sources["reporting"]["category"],
            "summary": f"Draft update generated from {len(issues)} Linear issue changes and {total_commits} non-merge GitHub commits.",
            "path": "/" + rel_path.as_posix(),
            "audience": project["clientAudience"],
            "tags": project.get("defaultTags", []) + ["auto-generated", "draft"]
        }
        if args.write:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(html_doc, encoding="utf-8")
            prepend_update_entry(entry)
        generated.append({"project": project["id"], "path": str(out_path), "issues": len(issues), "commits": total_commits, "written": args.write})

    print(json.dumps({"generated": generated}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
