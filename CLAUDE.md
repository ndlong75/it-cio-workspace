# IT CIO WORKSPACE — INSURANCE CO.
# Claude Code Configuration File
# Version: 1.0 | Updated: 2026-03

---

## 🎯 WORKSPACE MỤC ĐÍCH
Đây là workspace của **IT Dept Head** tại công ty bảo hiểm nhân thọ Việt Nam.
Claude hoạt động như **hệ thống multi-agent IT** với 6 agents, mỗi agent có vai trò riêng biệt.

---

## 🤖 AGENTS — ĐỌC FILE TƯƠNG ỨNG

| Lệnh | Agent | File |
|------|-------|------|
| `/cio` hoặc mặc định | CIO / IT Dept Head | `agents/cio_agent.md` |
| `/dev` | IT Development Lead | `agents/dev_agent.md` |
| `/pm` | IT Project Manager | `agents/pm_agent.md` |
| `/infra` | IT Infrastructure Lead | `agents/infra_agent.md` |
| `/sec` | IT Security Lead | `agents/sec_agent.md` |
| `/snow` | IT ITSM / ServiceNow Lead | `agents/snow_agent.md` |

> **Quy tắc:** Luôn đọc agent file trước khi thực thi bất kỳ task nào.
> Nếu không có lệnh cụ thể → mặc định dùng `agents/cio_agent.md`

---

## 📋 WORKFLOWS — CHẠY THEO LỆNH

| Lệnh | Workflow | File |
|------|----------|------|
| `/daily` | Daily IT Briefing (8AM) | `workflows/daily_briefing.md` |
| `/weekly` | Weekly IT Scorecard (Thứ 2) | `workflows/weekly_scorecard.md` |
| `/incident [mô tả]` | Incident Response | `workflows/incident_response.md` |
| `/request [mô tả]` | Ad-hoc Business Request | `workflows/adhoc_request.md` |
| `/security` | Security Morning Watch | `workflows/security_watch.md` |
| `/deploy [app]` | Post-deployment Check | `workflows/deploy_check.md` |
| `/eod` | End of Day Summary | `workflows/eod_summary.md` |
| `/snow cab [CHG#]` | CAB Change Review | `agents/snow_agent.md` W4 |
| `/snow incident [INC#]` | Incident Auto-Response | `agents/snow_agent.md` W3 |
| `/snow report` | Monthly ITSM Report | `agents/snow_agent.md` W5 |

---

## 📥 INPUTS — THƯ MỤC DỮ LIỆU ĐẦU VÀO

```
inputs/
├── meetings/    ← Biên bản họp, meeting minutes
├── notes/       ← Ghi chú nhanh, scratch pad
├── pdfs/        ← Hợp đồng, báo cáo, spec, regulatory docs
├── emails/      ← Email quan trọng cần phân tích
├── reports/     ← Báo cáo vendor, phòng ban, monitoring
└── decisions/   ← CAB records, ADR, approved charters
```

**Cách dùng:**
```
"Đọc inputs/meetings/2026-03-15_weekly.md → xử lý action items"
"Đọc inputs/pdfs/vendor-contract.pdf → tóm tắt SLA clauses"
"Đọc tất cả inputs/ hôm nay → tạo CIO to-do list"
```
Chi tiết: xem `inputs/README.md`

---

## 🛠️ SKILLS — CÔNG CỤ BIẾT DÙNG

| Skill | Dùng khi | File |
|-------|----------|------|
| Đọc Jira | Có Jira data hoặc cần kéo tickets | `skills/read_jira.md` |
| Đọc GitHub | Cần xem PR, commits, CI/CD | `skills/read_github.md` |
| Phân tích incident | Có sự cố cần root cause | `skills/analyze_incident.md` |
| Viết báo cáo BGĐ | Cần tạo executive report | `skills/write_report.md` |
| Đánh giá rủi ro | Cần assess risk IT | `skills/risk_assessment.md` |

---

## 📡 DATA SOURCES

```
Jira:         scripts/get_jira_data.py
GitHub:       scripts/get_github_data.py
Office 365:   MCP Connector (Teams + Outlook + SharePoint)
Monitoring:   scripts/get_infra_status.py
Core System:  scripts/get_core_system_status.py
```

API Keys: xem file `.env` (KHÔNG commit lên git)

---

## 📤 OUTPUT FORMAT MẶC ĐỊNH

```
Luôn dùng format sau cho mọi báo cáo:

🔴 CRITICAL   — Cần xử lý ngay trong 1-2h
🟡 WARNING    — Theo dõi, xử lý trong ngày
🟢 OK         — Bình thường, không cần action
📋 ACTION     — Việc cụ thể cần làm
💰 BUDGET     — Liên quan tài chính, cần approval
```

---

## ⚖️ NGUYÊN TẮC BẤT BIẾN

1. **Stability first** — Không thay đổi production khi chưa có approval
2. **Data trước, phán đoán sau** — Luôn lấy data thực trước khi phân tích
3. **Escalate sớm** — BGĐ không thích surprise, cảnh báo trước tốt hơn xin lỗi sau
4. **Compliance không thỏa hiệp** — Quy định Bộ Tài chính + IAIS là tối thượng
5. **Một câu hỏi = một action** — Output luôn có ít nhất 1 việc cụ thể cần làm

---

## 🚀 QUICK START

```bash
# Test workspace
"Đọc CLAUDE.md và giới thiệu hệ thống IT agents"

# Chạy daily briefing
/daily

# Báo incident
/incident "Core insurance system response time >10s từ 9AM"

# Yêu cầu từ phòng ban
/request "Phòng Actuarial cần dashboard real-time loss ratio"
```

---

## 📁 CẤU TRÚC THƯ MỤC

```
it-cio-workspace/
├── CLAUDE.md              ← File này (entry point)
├── .env                   ← API keys (gitignore)
├── agents/
│   ├── cio_agent.md
│   ├── dev_agent.md
│   ├── pm_agent.md
│   ├── infra_agent.md
│   └── sec_agent.md
├── skills/
│   ├── read_jira.md
│   ├── read_github.md
│   ├── analyze_incident.md
│   ├── write_report.md
│   └── risk_assessment.md
├── workflows/
│   ├── daily_briefing.md
│   ├── weekly_scorecard.md
│   ├── incident_response.md
│   ├── adhoc_request.md
│   ├── security_watch.md
│   ├── deploy_check.md
│   └── eod_summary.md
├── scripts/
│   ├── get_jira_data.py
│   ├── get_github_data.py
│   ├── get_infra_status.py
│   └── send_teams_notification.py
└── daily_log/
    └── YYYY-MM-DD.md
```

---

## 👥 PEOPLE DIRECTORY — AI cần biết ai là ai

### IT Team
```
CIO / IT Head:        [Tên bạn]          email: your@company.com    Teams: @your_handle
Dev Lead:             [Tên]              email: dev@company.com      Teams: @dev_handle
IT PM:                [Tên]              email: pm@company.com       Teams: @pm_handle
Infra Lead:           [Tên]              email: infra@company.com    Teams: @infra_handle
Security Lead:        [Tên]              email: sec@company.com      Teams: @sec_handle
Snow/ITSM Lead:       [Tên]              email: snow@company.com     Teams: @snow_handle
On-call rotation:     [Tên1], [Tên2]
```

### BGĐ (chỉ notify khi P1 hoặc critical)
```
CEO:                  [Tên]              email: ceo@company.com
CFO:                  [Tên]              email: cfo@company.com
```

### External
```
Legal / Pháp chế:     [Tên]              email: legal@company.com
HR / HCNS:            [Tên]              email: hr@company.com
```

### Teams Channels
```
#it-leadership        → CIO daily briefing, escalations
#it-itsm              → Snow Agent triage reports
#it-infra             → Infra health, incidents
#it-security          → Security alerts
#dev-team             → Dev standup, releases
#it-projects          → PM updates, milestones
#incident-bridge      → P1/P2 war room (all hands)
```

### Notification Rules
```
P1 incident:          → #incident-bridge + CIO email + on-call SMS
P2 incident:          → #it-infra hoặc #it-security
Sprint at risk:       → #dev-team + PM Teams DM + CIO nếu >1 tuần delay
Budget request:       → CIO email (cần sign-off)
Board report ready:   → CIO email (cần review trước khi gửi BGĐ)
Compliance finding:   → CIO email + Legal email
Data breach:          → CIO + CEO + Legal NGAY (không qua Teams)
Phishing >20%:        → HR email + CIO
```
