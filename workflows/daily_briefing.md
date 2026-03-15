# WORKFLOW: DAILY IT BRIEFING
# File: workflows/daily_briefing.md
# Trigger: T1 Auto — 8:00 AM hằng ngày
# Agent: CIO (aggregate từ 4 sub-agents)

---

## EXECUTION STEPS

```
STEP 1 — Activate sub-agents (parallel)
├── /infra → chạy W1: Infrastructure Health Check
├── /dev   → chạy W1: Daily Dev Standup
├── /pm    → chạy W1: Daily Project Pulse
└── /sec   → chạy W1: Security Morning Watch

STEP 2 — CIO aggregate tất cả reports

STEP 3 — Generate Daily IT Briefing

STEP 4 — Send output
├── Teams: #it-leadership (full report)
├── Teams: #cio-only (sensitive items)
└── Log: daily_log/[YYYY-MM-DD].md
```

---

## OUTPUT TEMPLATE

```
════════════════════════════════════════
🏢 IT DAILY BRIEFING — [Ngày/Tháng/Năm]
[Tên công ty] | IT Dept Head
════════════════════════════════════════

⚡ TỔNG QUAN (30 giây đọc)
[2-3 câu mô tả ngày hôm nay: bình thường / có vấn đề / critical]

─────────────────────────────────────────
🔴 CRITICAL — CẦN XỬ LÝ TRONG 2H
─────────────────────────────────────────
[Danh sách nếu có, NONE nếu không]

─────────────────────────────────────────
🟡 WARNING — THEO DÕI HÔM NAY
─────────────────────────────────────────
[Danh sách nếu có]

─────────────────────────────────────────
🟢 STATUS BY DOMAIN
─────────────────────────────────────────
🖥️  INFRA:    [OK/WARNING/CRITICAL] — [1 câu]
💻  DEV:      [OK/WARNING/CRITICAL] — [1 câu]
📋  PROJECTS: [OK/WARNING/CRITICAL] — [1 câu]
🔐  SECURITY: [OK/WARNING/CRITICAL] — [1 câu]

─────────────────────────────────────────
📋 CIO ACTION LIST HÔM NAY
─────────────────────────────────────────
1. [Action cụ thể] — Deadline: [giờ] — Owner: [CIO/Dev/PM/Infra/Sec]
2. [Action cụ thể] — Deadline: [giờ] — Owner: [...]
3. [Action cụ thể] — Deadline: [giờ] — Owner: [...]

─────────────────────────────────────────
💰 BUDGET ALERT (nếu có)
─────────────────────────────────────────
[Chỉ hiện nếu có budget issue, bỏ qua nếu không]

════════════════════════════════════════
Next briefing: ngày mai 8:00 AM
════════════════════════════════════════
```

---

## DATA INPUTS CẦN CÓ

```bash
# Chạy trước khi generate briefing
python scripts/get_infra_status.py    > /tmp/infra_status.json
python scripts/get_jira_data.py       > /tmp/jira_today.json
python scripts/get_github_data.py     > /tmp/github_today.json
python scripts/get_core_system_status.py > /tmp/core_status.json
```
