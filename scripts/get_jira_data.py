#!/usr/bin/env python3
"""
Script: get_jira_data.py
Mô tả: Kéo data từ Jira API cho IT Dept Head daily briefing
Usage: python scripts/get_jira_data.py [--output json|text]
"""

import requests
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# ── CONFIG ──────────────────────────────────────────────
JIRA_URL   = os.getenv("JIRA_URL", "https://your-company.atlassian.net")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "your_email@company.com")
JIRA_TOKEN = os.getenv("JIRA_TOKEN", "your_api_token")
IT_PROJECT = os.getenv("JIRA_PROJECT", "IT")  # Jira project key

AUTH = (JIRA_EMAIL, JIRA_TOKEN)
HEADERS = {"Accept": "application/json"}

# ── HELPER ──────────────────────────────────────────────
def jira_search(jql: str, fields: list) -> list:
    """Query Jira với JQL, trả về list issues"""
    try:
        resp = requests.get(
            f"{JIRA_URL}/rest/api/3/search",
            auth=AUTH, headers=HEADERS,
            params={"jql": jql, "fields": ",".join(fields), "maxResults": 50}
        )
        resp.raise_for_status()
        return resp.json().get("issues", [])
    except Exception as e:
        print(f"[ERROR] Jira API: {e}")
        return []

def fmt_issue(issue: dict) -> dict:
    """Format issue thành dict dễ đọc"""
    f = issue["fields"]
    return {
        "key":      issue["key"],
        "title":    f.get("summary", ""),
        "status":   f.get("status", {}).get("name", ""),
        "priority": f.get("priority", {}).get("name", ""),
        "assignee": (f.get("assignee") or {}).get("displayName", "Unassigned"),
        "due":      f.get("duedate", "No due date"),
        "updated":  f.get("updated", "")[:10],
        "type":     f.get("issuetype", {}).get("name", ""),
    }

# ── QUERIES ──────────────────────────────────────────────
FIELDS = ["summary", "status", "priority", "assignee", "duedate",
          "updated", "issuetype", "comment"]

def get_critical_tickets():
    """P1/P2 tickets đang open"""
    issues = jira_search(
        f'project = {IT_PROJECT} AND priority in (Highest, High) '
        f'AND status != Done ORDER BY priority DESC',
        FIELDS
    )
    return [fmt_issue(i) for i in issues]

def get_overdue_tickets():
    """Tickets quá deadline"""
    today = datetime.now().strftime("%Y-%m-%d")
    issues = jira_search(
        f'project = {IT_PROJECT} AND duedate < "{today}" '
        f'AND status != Done ORDER BY duedate ASC',
        FIELDS
    )
    return [fmt_issue(i) for i in issues]

def get_sla_breach():
    """Tickets In Progress quá 3 ngày"""
    three_days_ago = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    issues = jira_search(
        f'project = {IT_PROJECT} AND status = "In Progress" '
        f'AND updated <= "{three_days_ago}" ORDER BY updated ASC',
        FIELDS
    )
    return [fmt_issue(i) for i in issues]

def get_unassigned_tickets():
    """Tickets chưa có assignee"""
    issues = jira_search(
        f'project = {IT_PROJECT} AND assignee is EMPTY '
        f'AND status != Done ORDER BY created DESC',
        FIELDS
    )
    return [fmt_issue(i) for i in issues]

def get_today_created():
    """Tickets mới hôm nay"""
    today = datetime.now().strftime("%Y-%m-%d")
    issues = jira_search(
        f'project = {IT_PROJECT} AND created >= "{today}" '
        f'ORDER BY created DESC',
        FIELDS
    )
    return [fmt_issue(i) for i in issues]

def get_sprint_progress():
    """Sprint hiện tại: tổng quan"""
    issues = jira_search(
        f'project = {IT_PROJECT} AND sprint in openSprints() '
        f'ORDER BY status ASC',
        FIELDS
    )
    total = len(issues)
    done  = sum(1 for i in issues if i["fields"]["status"]["name"] in ["Done", "Closed"])
    blocked = sum(1 for i in issues if i["fields"]["status"]["name"] == "Blocked")
    return {
        "total": total,
        "done":  done,
        "in_progress": total - done - blocked,
        "blocked": blocked,
        "completion_pct": round(done / total * 100, 1) if total else 0
    }

# ── MAIN ─────────────────────────────────────────────────
def main():
    print(f"[INFO] Fetching Jira data from {JIRA_URL}...")

    result = {
        "fetched_at": datetime.now().isoformat(),
        "project": IT_PROJECT,
        "summary": {
            "critical_tickets":   get_critical_tickets(),
            "overdue_tickets":    get_overdue_tickets(),
            "sla_breach":         get_sla_breach(),
            "unassigned":         get_unassigned_tickets(),
            "new_today":          get_today_created(),
            "sprint_progress":    get_sprint_progress(),
        }
    }

    # Stats nhanh
    s = result["summary"]
    print(f"\n{'='*50}")
    print(f"JIRA SUMMARY — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'='*50}")
    print(f"🔴 Critical/High open:  {len(s['critical_tickets'])}")
    print(f"⏰ Overdue tickets:     {len(s['overdue_tickets'])}")
    print(f"🐢 SLA breach (>3d):   {len(s['sla_breach'])}")
    print(f"👤 Unassigned:         {len(s['unassigned'])}")
    print(f"🆕 New today:          {len(s['new_today'])}")
    sprint = s["sprint_progress"]
    print(f"📊 Sprint progress:    {sprint['done']}/{sprint['total']} ({sprint['completion_pct']}%)")
    print(f"{'='*50}\n")

    # Output JSON
    with open("/tmp/jira_today.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("[OK] Saved to /tmp/jira_today.json")
    return result

if __name__ == "__main__":
    main()
