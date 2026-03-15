# 📥 INPUTS — Thư Mục Dữ Liệu Đầu Vào
# File: inputs/README.md
# Mục đích: Chứa toàn bộ tài liệu thô để Claude đọc và xử lý

---

## 📁 Cấu Trúc

```
inputs/
├── meetings/          ← Meeting minutes, biên bản họp
├── notes/             ← Ghi chú nhanh, scratch pad
├── pdfs/              ← Tài liệu PDF: hợp đồng, báo cáo, spec
├── emails/            ← Email quan trọng cần phân tích
├── reports/           ← Báo cáo từ các phòng ban, vendor
└── decisions/         ← Quyết định đã được duyệt, CAB records
```

---

## 📂 CHI TIẾT TỪNG FOLDER

### 📋 meetings/
```
Chứa:
- Biên bản họp IT (meeting minutes)
- Action items từ cuộc họp
- Transcript họp (nếu có)

Tên file gợi ý:
  YYYY-MM-DD_[loại-họp]_[chủ-đề].md
  
Ví dụ:
  2026-03-15_weekly_it-review.md
  2026-03-10_vendor_jira-renewal.md
  2026-03-01_steering_digital-transform.md

Lệnh dùng với Claude:
  "Đọc meetings/2026-03-15_weekly_it-review.md
   Tóm tắt action items và assign cho đúng agent"
```

### 📝 notes/
```
Chứa:
- Ghi chú nhanh trong ngày
- Ý tưởng, brainstorm
- TODO list thô chưa vào Jira

Tên file gợi ý:
  YYYY-MM-DD_[chủ-đề].md
  
Ví dụ:
  2026-03-15_infra-upgrade-ideas.md
  2026-03-14_cto-meeting-notes.md
  2026-03-10_budget-scratch.md

Lệnh dùng với Claude:
  "Đọc notes/ hôm nay, tạo Jira tickets từ những ghi chú này"
```

### 📄 pdfs/
```
Chứa:
- Hợp đồng vendor (PDF)
- Báo cáo kiểm toán
- Technical specification
- Regulatory documents (Thông tư, Nghị định)
- SLA documents từ vendors

Tên file gợi ý:
  [vendor/type]_[document-name]_YYYY.pdf
  
Ví dụ:
  vendor_oracle-license-agreement_2026.pdf
  audit_it-security-report_Q1-2026.pdf
  regulatory_thong-tu-50_BTC.pdf
  sla_core-system-support_2026.pdf

Lệnh dùng với Claude:
  "Đọc pdfs/vendor_oracle-license-agreement_2026.pdf
   Tóm tắt các điều khoản SLA và penalty clause"
```

### 📧 emails/
```
Chứa:
- Email quan trọng từ vendor (copy paste hoặc .eml)
- Yêu cầu từ BGĐ qua email
- Escalation emails
- Thông báo từ Bộ Tài chính / cơ quan nhà nước

Tên file gợi ý:
  YYYY-MM-DD_[from]_[chủ-đề].md
  
Ví dụ:
  2026-03-14_ceo_request-dashboard-actuarial.md
  2026-03-12_vendor-oracle_license-expiry-notice.md
  2026-03-10_btc_circular-update-it-security.md

Lệnh dùng với Claude:
  "Đọc emails/2026-03-14_ceo_request-dashboard-actuarial.md
   Chạy workflow /request và tạo feasibility assessment"
```

### 📊 reports/
```
Chứa:
- Báo cáo từ vendor (uptime, SLA, invoice)
- Báo cáo từ phòng ban gửi IT
- Export từ monitoring tools
- Kết quả pen test, security audit

Tên file gợi ý:
  [source]_[type]_YYYY-MM.md hoặc .pdf
  
Ví dụ:
  vendor_aws-cost-report_2026-03.pdf
  security_pentest-report_Q1-2026.pdf
  monitoring_monthly-uptime_2026-03.csv
  dept_finance_it-requirements_2026-03.md

Lệnh dùng với Claude:
  "Đọc reports/security_pentest-report_Q1-2026.pdf
   Liệt kê critical findings và tạo remediation plan"
```

### ✅ decisions/
```
Chứa:
- CAB (Change Advisory Board) records
- Quyết định đầu tư IT đã được duyệt
- Architecture Decision Records (ADR)
- Approved project charters

Tên file gợi ý:
  CAB_YYYY-MM-DD_[change-description].md
  ADR_[số]_[decision-title].md
  
Ví dụ:
  CAB_2026-03-15_core-system-patch-v12.md
  CAB_2026-03-10_network-firewall-upgrade.md
  ADR_001_cloud-strategy-hybrid.md
  ADR_002_database-oracle-vs-postgresql.md

Lệnh dùng với Claude:
  "Đọc decisions/ tháng này
   Liệt kê tất cả changes đã approved và status hiện tại"
```

---

## 🤖 LỆNH CLAUDE HAY DÙNG VỚI INPUTS

```bash
# Xử lý meeting minutes → action items
"Đọc inputs/meetings/[file].md
 Tạo action items theo format Jira,
 assign cho đúng agent (dev/pm/infra/sec),
 đặt deadline dựa trên nội dung họp"

# Phân tích PDF vendor
"Đọc inputs/pdfs/[file].pdf
 So sánh SLA cam kết với KPI thực tế trong daily_log/
 Flag bất kỳ SLA breach nào"

# Email → task
"Đọc inputs/emails/[file].md
 Xác định: ai yêu cầu gì, deadline là khi nào
 Chạy /request workflow và tạo response draft"

# Tổng hợp tất cả inputs hôm nay
"Đọc tất cả files trong inputs/ được tạo/sửa hôm nay
 Tóm tắt những việc cần làm và add vào CIO action list"

# Trước EOD: clear inputs đã xử lý
"Đọc inputs/ — file nào đã được xử lý (có action items rồi)?
 Move sang archive/ với summary đính kèm"
```

---

## 📌 QUY TẮC ĐẶT FILE

```
✅ Luôn có ngày ở đầu tên file (YYYY-MM-DD)
✅ Dùng dấu gạch ngang thay khoảng trắng
✅ Tên file mô tả rõ nội dung
✅ Markdown (.md) cho text, giữ nguyên .pdf cho PDF

❌ Không đặt tên: "meeting.md", "notes.md", "doc1.pdf"
❌ Không để file quá cũ (>30 ngày) trong inputs/ — move sang archive/
```

---

## 🔄 LIFECYCLE CỦA MỘT FILE INPUT

```
1. DROP    → Bạn thả file vào đúng subfolder
2. PROCESS → Claude đọc và xử lý (tạo tickets, tasks, reports)
3. LOG     → Kết quả được log vào daily_log/
4. ARCHIVE → File gốc move sang archive/ sau khi xử lý xong
```
