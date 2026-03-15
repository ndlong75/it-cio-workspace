# WORKFLOW: INCIDENT RESPONSE
# File: workflows/incident_response.md
# Trigger: T2 Tele — /incident [mô tả] hoặc monitoring alert
# Primary Agent: Infra (P1/P2 infra) | Security (P1/P2 security) | CIO (escalation)

---

## PHÂN LOẠI SEVERITY

```
P1 — CRITICAL (response ≤15 phút)
     Core Insurance System down
     Data breach suspected
     Toàn bộ hoặc phần lớn user không làm việc được
     Revenue/regulatory impact trực tiếp

P2 — HIGH (response ≤1h)
     Một system down, workaround có thể
     Performance degradation >50%
     Một department bị ảnh hưởng

P3 — MEDIUM (response ≤4h)
     Cảnh báo, chưa có user impact
     Performance degradation nhẹ
     Lỗi intermittent

P4 — LOW (response ≤24h)
     Minor issue, không ảnh hưởng production
     Câu hỏi, request
```

---

## EXECUTION STEPS

```
BƯỚC 1 — INTAKE & CLASSIFY (5 phút)
├── Đọc mô tả incident
├── Classify: P1 / P2 / P3 / P4
├── Identify: Infra issue hay Security issue?
└── Activate đúng agent

BƯỚC 2 — INVESTIGATE (15-30 phút)
├── Pull data từ monitoring / logs
├── Check recent changes (deploy, config, patch)
├── Identify scope of impact
└── Find probable root cause

BƯỚC 3 — CONTAIN & FIX
├── Apply fix theo runbook nếu có
├── Rollback nếu recent change là cause
├── Escalate nếu không tự fix được
└── Workaround nếu fix takes time

BƯỚC 4 — COMMUNICATE
├── P1: Notify CIO ngay → CEO nếu >30 phút
├── P2: Notify CIO trong 1h
├── Notify affected departments
└── Update incident ticket real-time

BƯỚC 5 — POST-MORTEM (bắt buộc P1, optional P2)
├── Timeline của incident
├── Root cause (5-Why analysis)
├── What worked, what didn't
└── Action items để prevent recurrence
```

---

## OUTPUT TEMPLATE

```
🚨 INCIDENT REPORT — [ID] — [Severity]
Time: [bắt đầu] → [kết thúc / ongoing]
Status: [Investigating / Contained / Resolved]

📍 IMPACT
Systems: [tên hệ thống]
Users affected: [số lượng / phòng ban]
Business impact: [mô tả ngắn]

🔍 ROOT CAUSE
[Mô tả nguyên nhân — hoặc "Under investigation"]

✅ ACTIONS TAKEN
1. [Action + timestamp]
2. [Action + timestamp]

📋 NEXT STEPS
1. [Action — Owner — Deadline]

⏱️ TIMELINE
[HH:MM] Incident detected / reported
[HH:MM] CIO notified
[HH:MM] Root cause identified
[HH:MM] Fix applied
[HH:MM] Service restored
[HH:MM] Incident closed
```
