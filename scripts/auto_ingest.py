#!/usr/bin/env python3
"""
Script: auto_ingest.py
Mô tả: Tự động kéo data từ O365 (Email, Teams, SharePoint)
       vào đúng subfolder trong inputs/
       Chạy: python scripts/auto_ingest.py [--source all|email|teams|sharepoint]
"""

import os, json, re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()

# ── CONFIG ───────────────────────────────────────────────
WORKSPACE    = Path(__file__).parent.parent
INPUTS       = WORKSPACE / "inputs"
GRAPH_TOKEN  = os.getenv("M365_GRAPH_TOKEN", "")   # Từ MCP hoặc OAuth
GRAPH_BASE   = "https://graph.microsoft.com/v1.0"
MY_EMAIL     = os.getenv("JIRA_EMAIL", "")

# Keywords phân loại email → folder
EMAIL_RULES = {
    "meetings":  ["meeting", "họp", "minutes", "biên bản", "agenda"],
    "decisions": ["approved", "duyệt", "CAB", "change request", "decision"],
    "reports":   ["report", "báo cáo", "monthly", "weekly", "quarterly"],
    "emails":    [],  # fallback
}

def graph_get(path: str, params: dict = None) -> dict:
    """Call Microsoft Graph API"""
    if not GRAPH_TOKEN:
        print("[WARN] M365_GRAPH_TOKEN not set — skipping O365 fetch")
        return {}
    resp = requests.get(
        f"{GRAPH_BASE}{path}",
        headers={"Authorization": f"Bearer {GRAPH_TOKEN}"},
        params=params
    )
    if resp.ok:
        return resp.json()
    print(f"[ERROR] Graph API {path}: {resp.status_code}")
    return {}

def classify_email(subject: str, body: str) -> str:
    """Phân loại email vào đúng folder dựa trên nội dung"""
    text = (subject + " " + body).lower()
    for folder, keywords in EMAIL_RULES.items():
        if any(kw in text for kw in keywords):
            return folder
    return "emails"

def sanitize_filename(text: str) -> str:
    """Tạo tên file an toàn từ text"""
    return re.sub(r'[^\w\-]', '-', text)[:50].strip('-').lower()

# ── INGEST: OUTLOOK EMAILS ────────────────────────────────
def ingest_emails(since_hours: int = 24):
    """Kéo emails quan trọng từ Outlook trong N giờ qua"""
    print(f"\n[EMAIL] Fetching emails from last {since_hours}h...")

    since = (datetime.now(timezone.utc) - timedelta(hours=since_hours)).isoformat()
    data = graph_get(
        f"/me/messages",
        {
            "$filter": f"receivedDateTime ge {since} and importance eq 'high'",
            "$select": "subject,from,receivedDateTime,body,importance",
            "$top": 20
        }
    )

    emails = data.get("value", [])
    saved = 0

    for email in emails:
        subject  = email.get("subject", "no-subject")
        sender   = email.get("from", {}).get("emailAddress", {}).get("address", "unknown")
        received = email.get("receivedDateTime", "")[:10]
        body     = email.get("body", {}).get("content", "")

        # Strip HTML tags
        body_clean = re.sub(r'<[^>]+>', '', body).strip()[:2000]

        # Classify
        folder = classify_email(subject, body_clean)
        target_dir = INPUTS / folder
        target_dir.mkdir(exist_ok=True)

        # Tạo tên file
        sender_short = sender.split("@")[0]
        filename = f"{received}_{sender_short}_{sanitize_filename(subject)}.md"
        filepath = target_dir / filename

        # Skip nếu đã có
        if filepath.exists():
            continue

        # Ghi file
        content = f"""# EMAIL: {subject}

## Metadata
- **From:** {sender}
- **Received:** {received}
- **Auto-classified:** {folder}
- **Source:** Outlook (auto-ingest)

## Nội dung
{body_clean}

---
*File được tạo tự động bởi auto_ingest.py*
*Lệnh Claude: "Đọc file này và xử lý action items nếu có"*
"""
        filepath.write_text(content, encoding="utf-8")
        print(f"  ✅ {folder}/{filename}")
        saved += 1

    print(f"[EMAIL] Saved {saved}/{len(emails)} emails")
    return saved

# ── INGEST: TEAMS MESSAGES ────────────────────────────────
def ingest_teams_mentions(since_hours: int = 24):
    """Kéo Teams messages có @mention hoặc từ kênh IT"""
    print(f"\n[TEAMS] Fetching Teams mentions...")

    # Lấy danh sách chats
    chats = graph_get("/me/chats", {"$top": 20}).get("value", [])
    saved = 0

    for chat in chats:
        chat_id = chat["id"]
        messages = graph_get(
            f"/me/chats/{chat_id}/messages",
            {"$top": 10}
        ).get("value", [])

        for msg in messages:
            created = msg.get("createdDateTime", "")[:10]
            body    = msg.get("body", {}).get("content", "")
            body_clean = re.sub(r'<[^>]+>', '', body).strip()

            # Chỉ lấy messages có mention hoặc có action keywords
            action_keywords = ["please", "cần", "deadline", "urgent", "gấp", "approve", "review"]
            if not any(kw in body_clean.lower() for kw in action_keywords):
                continue

            sender = msg.get("from", {}).get("user", {}).get("displayName", "unknown")
            filename = f"{created}_{sanitize_filename(sender)}_teams-message.md"
            filepath = INPUTS / "notes" / filename

            if filepath.exists():
                continue

            content = f"""# TEAMS MESSAGE — {created}

## Metadata
- **From:** {sender}
- **Date:** {created}
- **Source:** Microsoft Teams (auto-ingest)

## Nội dung
{body_clean[:1000]}

---
*Lệnh Claude: "Có action item nào trong message này không? Nếu có, tạo Jira ticket"*
"""
            filepath.write_text(content, encoding="utf-8")
            saved += 1

    print(f"[TEAMS] Saved {saved} messages")
    return saved

# ── INGEST: SHAREPOINT DOCS ───────────────────────────────
def ingest_sharepoint_recent(since_hours: int = 48):
    """Kéo documents mới được share/update trên SharePoint"""
    print(f"\n[SHAREPOINT] Fetching recent documents...")

    since = (datetime.now(timezone.utc) - timedelta(hours=since_hours)).isoformat()
    items = graph_get(
        "/me/drive/recent",
        {"$top": 10}
    ).get("value", [])

    saved = 0
    for item in items:
        name     = item.get("name", "")
        modified = item.get("lastModifiedDateTime", "")[:10]
        url      = item.get("webUrl", "")
        size     = item.get("size", 0)

        # Chỉ lấy PDF và Word docs
        if not any(name.endswith(ext) for ext in [".pdf", ".docx", ".xlsx"]):
            continue

        # Tạo reference file (không download, chỉ log URL)
        safe_name = sanitize_filename(name.rsplit(".", 1)[0])
        filename  = f"{modified}_{safe_name}_sharepoint-ref.md"
        filepath  = INPUTS / "reports" / filename

        if filepath.exists():
            continue

        content = f"""# SHAREPOINT DOCUMENT REFERENCE

## File Info
- **Name:** {name}
- **Modified:** {modified}
- **Size:** {size:,} bytes
- **URL:** {url}
- **Source:** SharePoint (auto-ingest)

## Hướng dẫn
File này là reference. Để Claude đọc nội dung đầy đủ:
"Fetch document từ SharePoint URL: {url} và phân tích nội dung"

---
*Lệnh Claude: "Đọc document SharePoint này và tóm tắt nội dung quan trọng"*
"""
        filepath.write_text(content, encoding="utf-8")
        print(f"  ✅ reports/{filename}")
        saved += 1

    print(f"[SHAREPOINT] Saved {saved} document references")
    return saved

# ── WATCH: LOCAL FOLDER ───────────────────────────────────
def scan_unprocessed_inputs() -> list:
    """Tìm files trong inputs/ chưa được xử lý"""
    unprocessed = []
    processed_marker = "[PROCESSED]"

    for folder in ["meetings", "notes", "pdfs", "emails", "reports", "decisions"]:
        folder_path = INPUTS / folder
        if not folder_path.exists():
            continue
        for f in folder_path.iterdir():
            if f.name.startswith("TEMPLATE_") or f.name == ".gitkeep":
                continue
            if f.suffix in [".md", ".txt", ".pdf", ".docx"]:
                # Kiểm tra xem đã có processed marker chưa
                if f.suffix == ".md":
                    content = f.read_text(encoding="utf-8", errors="ignore")
                    if processed_marker not in content:
                        unprocessed.append(str(f.relative_to(WORKSPACE)))
                else:
                    # PDF, docx — luôn cần xử lý
                    unprocessed.append(str(f.relative_to(WORKSPACE)))

    return unprocessed

# ── MAIN ─────────────────────────────────────────────────
def main():
    print("=" * 55)
    print(f"AUTO INGEST — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 55)

    total_saved = 0
    total_saved += ingest_emails(since_hours=24)
    total_saved += ingest_teams_mentions(since_hours=24)
    total_saved += ingest_sharepoint_recent(since_hours=48)

    # Scan unprocessed
    unprocessed = scan_unprocessed_inputs()

    print(f"\n{'='*55}")
    print(f"INGEST SUMMARY")
    print(f"{'='*55}")
    print(f"📥 New files ingested:    {total_saved}")
    print(f"⏳ Awaiting processing:   {len(unprocessed)}")
    if unprocessed:
        print(f"\nFiles cần Claude xử lý:")
        for f in unprocessed:
            print(f"  → {f}")
    print(f"\nLệnh xử lý tất cả:")
    print(f'  "Đọc và xử lý tất cả files chưa processed trong inputs/"')
    print("=" * 55)

    # Save manifest
    manifest = {
        "run_at": datetime.now().isoformat(),
        "ingested": total_saved,
        "unprocessed": unprocessed
    }
    (WORKSPACE / "daily_log").mkdir(exist_ok=True)
    manifest_path = WORKSPACE / "daily_log" / "ingest_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"\n[OK] Manifest saved: daily_log/ingest_manifest.json")

if __name__ == "__main__":
    main()
