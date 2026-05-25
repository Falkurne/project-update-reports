#!/usr/bin/env python3
"""Generate draft stakeholder update reports from Linear + GitHub activity.

Default behaviour is safe/draft-only:
- writes an HTML report under updates/<project>/
- prepends an entry to data/updates.json
- does not commit, push, or send to clients
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import pathlib
import subprocess
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES_PATH = ROOT / "data" / "reporting-sources.json"
UPDATES_PATH = ROOT / "data" / "updates.json"


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
        if line.strip():
            commits.append(json.loads(line))
    return commits


def humanise_issue(issue: dict) -> str:
    title = issue["title"].strip().rstrip(".")
    state = issue["state"]["name"]
    if issue["state"]["type"] == "completed":
        return f"Completed: {title}."
    if issue["state"]["type"] == "started":
        return f"In progress/review: {title}."
    return f"Queued: {title}."


def humanise_commit(commit: dict) -> str:
    first = commit["message"].splitlines()[0].strip().rstrip(".")
    return first[0].upper() + first[1:] + "." if first else "Repository update."


def render_report(project: dict, since_local: dt.datetime, now_local: dt.datetime, issues: list[dict], commits_by_repo: dict[str, list[dict]]) -> str:
    issue_lines = [humanise_issue(i) for i in issues]
    commit_lines = [humanise_commit(c) for commits in commits_by_repo.values() for c in commits]
    completed = [i for i in issues if i["state"]["type"] == "completed"]
    active = [i for i in issues if i["state"]["type"] == "started"]
    blocked = [i for i in issues if any(l["name"] == "blocked" for l in i.get("labels", {}).get("nodes", []))]

    def li(items: list[str], empty: str) -> str:
        if not items:
            return f"<li>{html.escape(empty)}</li>"
        return "\n".join(f"<li>{html.escape(x)}</li>" for x in items)

    issue_link_items = [f'{i["identifier"]}: {i["title"]} ({i["state"]["name"]})' for i in issues]
    repo_items = []
    for repo, commits in commits_by_repo.items():
        for c in commits:
            repo_items.append(f'{repo}@{c["sha"][:7]} — {c["message"].splitlines()[0]}')

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
      <ul>
        {li(issue_lines[:8] + commit_lines[:5], 'No tracked activity found in this reporting window.')}
      </ul>
    </section>

    <section>
      <h2>What changed</h2>
      <ul>{li([humanise_issue(i) for i in completed] + commit_lines[:8], 'No completed changes were detected yet.')}</ul>
    </section>

    <section>
      <h2>Currently in progress</h2>
      <ul>{li([humanise_issue(i) for i in active], 'Nothing is marked as in progress/review in Linear.')}</ul>
    </section>

    <section>
      <h2>Blockers / decisions needed</h2>
      <ul>{li([i['title'] for i in blocked], 'No blocked items were tagged in Linear.')}</ul>
    </section>

    <section>
      <h2>Source activity</h2>
      <p class=\"meta\">Linear issues</p>
      <ul>{li(issue_link_items, 'No Linear issue changes found.')}</ul>
      <p class=\"meta\">GitHub commits</p>
      <ul>{li(repo_items, 'No GitHub commits found.')}</ul>
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
        entry = {
            "id": report_id,
            "projectId": project["id"],
            "title": f"{project['displayName']} auto-generated progress update",
            "date": date_slug,
            "category": sources["reporting"]["category"],
            "summary": f"Draft update generated from {len(issues)} Linear issue changes and {sum(len(v) for v in commits_by_repo.values())} GitHub commits.",
            "path": "/" + rel_path.as_posix(),
            "audience": project["clientAudience"],
            "tags": project.get("defaultTags", []) + ["auto-generated", "draft"]
        }
        if args.write:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(html_doc, encoding="utf-8")
            prepend_update_entry(entry)
        generated.append({"project": project["id"], "path": str(out_path), "issues": len(issues), "commits": sum(len(v) for v in commits_by_repo.values()), "written": args.write})

    print(json.dumps({"generated": generated}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
