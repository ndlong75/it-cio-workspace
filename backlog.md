# BACKLOG.md — Everything Still Left To Do
# Project: IT CIO Workspace
# Updated: 2026-03-15

---

## 🔴 IMMEDIATE (do this before using the system)

- [ ] **Enable GitHub Pages**
  `github.com/ndlong75/it-cio-workspace → Settings → Pages → main / root → Save`
  Result: HTML diagrams viewable at `https://ndlong75.github.io/it-cio-workspace/output/`

- [ ] **Fill config/people.yaml**
  Add real names, emails, Teams IDs for:
  CIO · Dev Lead · PM · Infra Lead · Security Lead · Snow Lead · On-call · CEO · CFO · Legal · HR

- [ ] **Copy .env.example → .env and fill API keys**
  ANTHROPIC_API_KEY · JIRA_URL + TOKEN · GITHUB_TOKEN · M365 credentials

- [ ] **Test workspace in Claude Code**
  `claude code /path/to/it-cio-workspace`
  Test: `/daily` · `/incident test` · `/request test`

---

## 🟡 SETUP (need before full automation)

- [ ] **Connect MCP connectors in Claude Desktop**
  Jira MCP · GitHub MCP · Microsoft 365 MCP (needs Team/Enterprise plan)

- [ ] **Set up Snow webhook → Claude Code trigger**
  ServiceNow: Business Rule → HTTP POST → Claude Code endpoint on P1/P2 create
  Target: Snow Agent W3 (Incident Auto-Response) fires in <2 minutes

- [ ] **Configure Microsoft Entra Admin for M365 connector**
  Required for: reading Outlook emails, Teams messages, calendar
  Needs: Global Admin or App Registration in Azure AD

- [ ] **Create skills/ folder .md files**
  Referenced in CLAUDE.md but not yet created:
  - `skills/read_jira.md`
  - `skills/read_github.md`
  - `skills/analyze_incident.md`
  - `skills/write_report.md`
  - `skills/risk_assessment.md`

- [ ] **Set up Telegram Bot (optional)**
  For T2 Tele workflows — alternative to Teams for mobile notifications
  BotFather → get token → add to .env as TELEGRAM_BOT_TOKEN

---

## 🟢 ENHANCEMENTS (nice to have)

### Missing Scripts
- [ ] `scripts/get_snow_data.py` — ServiceNow API connector
  Modules: INC · REQ · CHG · PRB · SLA · CMDB · KB
- [ ] `scripts/send_teams_notification.py` — Microsoft Teams webhook sender
- [ ] `scripts/get_infra_status.py` — Monitoring API connector
- [ ] `scripts/get_ad_users.py` — Active Directory user export for Security Agent

### Missing Workflow Files
- [ ] `workflows/weekly_scorecard.md` — CIO W2
- [ ] `workflows/adhoc_request.md` — CIO W3
- [ ] `workflows/security_watch.md` — Security W1
- [ ] `workflows/deploy_check.md` — Dev W3
- [ ] `workflows/cab_review.md` — Snow W4
- [ ] `workflows/itsm_report.md` — Snow W5

### HTML Diagrams (potential new ones)
- [ ] `output/snow-workflow.html` — Detailed Snow Agent flow (all 6 modules)
- [ ] `output/compliance-map.html` — TT50 / PDPD / IAIS requirements map
- [ ] `output/onboarding.html` — Step-by-step setup guide for new team member

### GitHub & Documentation
- [ ] **Push updated files to GitHub** (memory.md, restart.md, backlog.md, people.yaml)
- [ ] **Add README.md to repo root** — overview, setup instructions, diagram links
- [ ] **Set up GitHub Actions** — auto-validate YAML/MD files on push
- [ ] **GitHub Pages** — add index.html linking to all 10 diagrams

### Integrations
- [ ] **ServiceNow → Jira sync** — auto-create Jira story when Snow REQ approved
- [ ] **GitHub → Snow CHG** — auto-create CHG when PR merged to main
- [ ] **Monitoring → Snow INC** — auto-create P2 when threshold exceeded
- [ ] **Active Directory → Security Agent** — nightly export of user changes

---

## 📊 PROGRESS TRACKER

| Area | Status | Notes |
|------|--------|-------|
| 6 Agent personas | ✅ Done | agents/*.md |
| 30 Workflows design | ✅ Done | Documented in agent-flows HTML |
| 10 HTML diagrams | ✅ Done | output/*.html |
| Core scripts (4) | ✅ Done | scripts/*.py |
| Core workflows (3) | ✅ Done | workflows/*.md |
| Config/people.yaml | ⏳ Template only | Need real data |
| GitHub repo | ✅ Public | ndlong75/it-cio-workspace |
| GitHub Pages | ⏳ Not set up | Settings → Pages |
| .env / API keys | ⏳ Not set up | .env.example ready |
| MCP connectors | ❌ Not started | Jira, GitHub, M365 |
| Snow webhook | ❌ Not started | Needs ServiceNow admin |
| Skills folder | ❌ Not started | 5 skill files needed |
| Missing scripts (4) | ❌ Not started | Snow, Teams, Infra, AD |
| Missing workflows (6) | ❌ Not started | See list above |

---

## 🗓️ SUGGESTED ORDER

```
Week 1:  GitHub Pages → people.yaml → .env → Claude Code test
Week 2:  MCP connectors → Snow webhook → skills/ files
Week 3:  Missing scripts → missing workflow files
Week 4:  GitHub Actions → README → Integrations
```
