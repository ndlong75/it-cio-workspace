# WORKFLOW: END OF DAY (EOD)
# File: workflows/eod_summary.md
# Trigger: T1 Auto — 5:30 PM | hoặc /eod
# Agent: CIO (orchestrate)

---

## MỤC TIÊU
1. Xử lý tất cả inputs/ chưa được xử lý
2. Tổng hợp ngày hôm nay
3. Tạo to-do list cho ngày mai
4. Auto-archive files đã xử lý
5. Send EOD report lên Teams

---

## EXECUTION STEPS

```
STEP 1 — PROCESS UNPROCESSED INPUTS
├── python scripts/auto_ingest.py      # Kéo thêm từ O365 nếu có
├── Đọc daily_log/ingest_manifest.json  # Xem files nào chưa xử lý
└── Xử lý từng file theo loại:
    ├── meetings/ → extract action items → tạo Jira tickets
    ├── emails/   → identify requests → tạo tasks hoặc draft reply
    ├── notes/    → organize → add to tomorrow's to-do
    ├── pdfs/     → summarize key points → save summary
    ├── reports/  → extract metrics → update KPI tracker
    └── decisions/→ log trong CAB register

STEP 2 — DAILY REVIEW (từ 4 agents)
├── /infra  → tổng kết ngày: incidents, uptime final
├── /dev    → commits, PRs merged, deployments
├── /pm     → milestones đạt/miss, stakeholder updates sent
└── /sec    → alerts handled, access reviews done

STEP 3 — GENERATE EOD REPORT

STEP 4 — AUTO ARCHIVE
└── python scripts/auto_archive.py
    → Move tất cả [PROCESSED] files sang archive/YYYY-MM/

STEP 5 — SEND TEAMS NOTIFICATION
└── python scripts/send_teams_notification.py --type eod
```

---

## OUTPUT TEMPLATE

```
════════════════════════════════════════
🌙 IT EOD SUMMARY — [Ngày/Tháng/Năm]
════════════════════════════════════════

📥 INPUTS PROCESSED HÔM NAY
├── Meetings: [số] files → [số] action items → Jira
├── Emails:   [số] files → [số] tasks tạo mới
├── PDFs:     [số] files → summarized
├── Notes:    [số] files → organized
└── Reports:  [số] files → metrics extracted

─────────────────────────────────────────
✅ HOÀN THÀNH HÔM NAY
─────────────────────────────────────────
[List những việc đã done]

─────────────────────────────────────────
⏳ CHUYỂN SANG NGÀY MAI
─────────────────────────────────────────
[List việc chưa xong, carry over]

─────────────────────────────────────────
📋 TO-DO NGÀY MAI (ưu tiên)
─────────────────────────────────────────
1. [Việc quan trọng nhất]
2. [Việc thứ 2]
3. [Việc thứ 3]

─────────────────────────────────────────
📦 ARCHIVED HÔM NAY
─────────────────────────────────────────
[Số] files đã archive sang archive/[YYYY-MM]/

─────────────────────────────────────────
🔴 CẦN CIO BIẾT TRƯỚC KHI ĐI VỀ
─────────────────────────────────────────
[Critical items nếu có, NONE nếu không]

════════════════════════════════════════
Ngày mai bắt đầu: 8:00 AM Daily Briefing
════════════════════════════════════════
```

---

## FILE LIFECYCLE (Claude tự quản lý)

```
inputs/meetings/2026-03-15_weekly.md
        ↓ Claude đọc + xử lý
        ↓ Tạo Jira tickets
        ↓ Draft email participants
        ↓ Mark [PROCESSED] trong file
        ↓ Log vào daily_log/2026-03-15.md
        ↓ python auto_archive.py
archive/2026-03/meetings/2026-03-15_weekly.md ✅
```
