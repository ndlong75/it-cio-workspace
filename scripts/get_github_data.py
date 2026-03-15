#!/usr/bin/env python3
"""
Script: get_github_data.py
Mô tả: Kéo data từ GitHub API cho IT Dev Agent daily standup
Usage: python scripts/get_github_data.py
"""

import requests
import json
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "ghp_your_token")
GITHUB_ORG   = os.getenv("GITHUB_ORG", "your-company")   # hoặc username cá nhân
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
BASE = "https://api.github.com"

def gh_get(path: str, params: dict = None) -> dict | list:
    """GET request tới GitHub API"""
    try:
        resp = requests.get(f"{BASE}{path}", headers=HEADERS, params=params)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ERROR] GitHub API {path}: {e}")
        return []

def get_repos() -> list:
    """Lấy danh sách repo của org/user"""
    repos = gh_get(f"/orgs/{GITHUB_ORG}/repos", {"type": "all", "per_page": 50})
    if not repos:  # Thử với user nếu org không có
        repos = gh_get(f"/users/{GITHUB_ORG}/repos", {"per_page": 50})
    return repos if isinstance(repos, list) else []

def get_open_prs(repo: str) -> list:
    """PRs đang open của một repo"""
    prs = gh_get(f"/repos/{GITHUB_ORG}/{repo}/pulls", {"state": "open", "per_page": 20})
    result = []
    for pr in (prs if isinstance(prs, list) else []):
        created = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
        age_days = (datetime.now(timezone.utc) - created).days
        result.append({
            "number":    pr["number"],
            "title":     pr["title"],
            "author":    pr["user"]["login"],
            "age_days":  age_days,
            "reviewers": len(pr.get("requested_reviewers", [])),
            "url":       pr["html_url"],
        })
    return result

def get_recent_commits(repo: str, since_hours: int = 24) -> list:
    """Commits trong N giờ qua"""
    since = (datetime.now(timezone.utc) - timedelta(hours=since_hours)).isoformat()
    commits = gh_get(f"/repos/{GITHUB_ORG}/{repo}/commits",
                     {"since": since, "per_page": 20})
    return [{
        "sha":     c["sha"][:7],
        "message": c["commit"]["message"].split("\n")[0],
        "author":  c["commit"]["author"]["name"],
        "time":    c["commit"]["author"]["date"][:16],
    } for c in (commits if isinstance(commits, list) else [])]

def get_workflow_runs(repo: str) -> dict:
    """CI/CD workflow runs mới nhất"""
    runs = gh_get(f"/repos/{GITHUB_ORG}/{repo}/actions/runs", {"per_page": 5})
    if not isinstance(runs, dict):
        return {"pass": 0, "fail": 0, "pending": 0}
    items = runs.get("workflow_runs", [])
    return {
        "pass":    sum(1 for r in items if r["conclusion"] == "success"),
        "fail":    sum(1 for r in items if r["conclusion"] == "failure"),
        "pending": sum(1 for r in items if r["status"] == "in_progress"),
        "latest":  items[0]["conclusion"] if items else "unknown"
    }

def get_open_issues(repo: str) -> int:
    """Số issues đang open"""
    issues = gh_get(f"/repos/{GITHUB_ORG}/{repo}/issues",
                    {"state": "open", "per_page": 1})
    return len(issues) if isinstance(issues, list) else 0

# ── MAIN ─────────────────────────────────────────────────
def main():
    print(f"[INFO] Fetching GitHub data for org: {GITHUB_ORG}...")

    repos = get_repos()
    repo_names = [r["name"] for r in repos]
    print(f"[INFO] Found {len(repo_names)} repos: {', '.join(repo_names[:10])}")

    all_prs       = []
    all_commits   = []
    cicd_summary  = {"pass": 0, "fail": 0, "pending": 0}
    stale_prs     = []  # PR > 2 ngày chưa review

    for repo in repo_names:
        # PRs
        prs = get_open_prs(repo)
        for pr in prs:
            pr["repo"] = repo
            all_prs.append(pr)
            if pr["age_days"] >= 2 and pr["reviewers"] == 0:
                stale_prs.append(pr)

        # Commits hôm nay
        commits = get_recent_commits(repo, since_hours=24)
        for c in commits:
            c["repo"] = repo
            all_commits.append(c)

        # CI/CD
        cicd = get_workflow_runs(repo)
        cicd_summary["pass"]    += cicd["pass"]
        cicd_summary["fail"]    += cicd["fail"]
        cicd_summary["pending"] += cicd["pending"]

    result = {
        "fetched_at":    datetime.now().isoformat(),
        "org":           GITHUB_ORG,
        "repos_scanned": len(repo_names),
        "open_prs":      all_prs,
        "stale_prs":     stale_prs,
        "commits_today": all_commits,
        "cicd_summary":  cicd_summary,
    }

    print(f"\n{'='*50}")
    print(f"GITHUB SUMMARY — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'='*50}")
    print(f"📦 Repos scanned:     {len(repo_names)}")
    print(f"🔀 Open PRs:          {len(all_prs)}")
    print(f"⚠️  Stale PRs (>2d):  {len(stale_prs)}")
    print(f"💻 Commits today:     {len(all_commits)}")
    print(f"✅ CI/CD pass:        {cicd_summary['pass']}")
    print(f"❌ CI/CD fail:        {cicd_summary['fail']}")
    print(f"⏳ CI/CD pending:     {cicd_summary['pending']}")
    print(f"{'='*50}\n")

    if stale_prs:
        print("⚠️  STALE PRs NEED ATTENTION:")
        for pr in stale_prs:
            print(f"  [{pr['repo']}] #{pr['number']} — {pr['title'][:50]} ({pr['age_days']}d) by {pr['author']}")

    with open("/tmp/github_today.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("\n[OK] Saved to /tmp/github_today.json")
    return result

if __name__ == "__main__":
    main()
