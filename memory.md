# MEMORY.md — Key Facts & Decisions
# Project: IT CIO Workspace with Claude AI
# Updated: 2026-03-15

---

## 👤 WHO YOU ARE
- **Role:** IT Dept Head (IT Head) tại công ty **bảo hiểm nhân thọ Việt Nam**
- **GitHub:** ndlong75
- **Repo:** https://github.com/ndlong75/it-cio-workspace (PUBLIC)
- **Tools at company:** Jira · GitHub · Office 365 · ServiceNow (Snow) · Claude Code
- **Claude plan:** Paid (Pro/Team)

---

## 🏗️ WHAT WAS BUILT

### Core System
- **6 AI Agents:** CIO · Dev · PM · Infra · Security · Snow/ITSM
- **30 PDCA Workflows** (5 per agent): T1 Auto · T2 Tele · T3 Deep · On-demand
- **Multi-agent interaction map** — Snow is central dispatcher, CIO is decision-maker

### File Structure
```
it-cio-workspace/
├── CLAUDE.md              ← Entry point for Claude Code
├── .env.example           ← API keys template
├── .gitignore
├── config/
│   └── people.yaml        ← ⚠️ NOT YET FILLED with real names/emails
├── output/                ← 10 HTML diagrams
├── agents/                ← 6 agent .md persona files
├── workflows/             ← daily_briefing, eod_summary, incident_response
├── scripts/               ← get_jira, get_github, auto_ingest, auto_archive
└── inputs/                ← meetings/, notes/, pdfs/, emails/, reports/, decisions/
```

### 10 HTML Diagrams (all in output/)
1. `cosmic-diagram.html` — Animated universe, hover for agent details
2. `it-breakdown.html` — 6 agents × 30 workflows breakdown table
3. `daily-flow-vi.html` — Daily workflow timeline (Vietnamese)
4. `daily-flow-en.html` — Daily workflow timeline (English)
5. `agent-daily-flows-vi.html` — Per-agent daily flows, tabs UI (VI)
6. `agent-daily-flows-en.html` — Per-agent daily flows, tabs UI (EN)
7. `agent-flows-vi.html` — Full workflows + source systems, scroll layout (VI)
8. `agent-flows-en.html` — Full workflows + source systems, scroll layout (EN)
9. `agent-interactions.html` — Agent interaction matrix + daily timeline
10. `human-intervention.html` — Human vs AI decision map

---

## 🔑 KEY DECISIONS MADE

| Decision | Choice | Reason |
|----------|--------|--------|
| Snow Agent | Dedicated agent (Hướng 1) | Centralized queue ownership |
| Daily flow | TOC + scroll (not tabs) | Easier to read all at once |
| HTML output | Separate output/ folder | Clean separation |
| Source systems | Shown per workflow | User wanted explicit data sources |
| Human loop | ~30 min/day | Read briefing, approve CHG, handle P1>30min |
| Notification | people.yaml config | Agents lookup file, not hardcoded |
| Git repo | Public | For GitHub Pages later |

---

## 📊 WORKFLOW COUNTS
- **T1 Auto:** 11 (run on schedule automatically)
- **T2 Tele:** 9 (triggered by command)
- **T3 Deep:** 10 (deep analysis, periodic)
- **On-demand:** 4 (webhook/event driven, OD type)
- **Total:** 30 workflows · 30 prompts

---

## 🔗 DATA SOURCES INTEGRATED
ServiceNow · Jira · GitHub · Office 365 (Graph API) · Monitoring API ·
SIEM · Active Directory · SonarQube · CVE/NVD · Backup System · Core Insurance System

---

## ⚠️ THINGS NOT YET DONE
- `config/people.yaml` — real names/emails not filled in
- GitHub Pages — not yet enabled (repo just made public)
- `.env` — API keys not yet configured
- Snow webhook — not yet set up
- MCP connectors — not yet connected in Claude Desktop
- Skills folder — defined in CLAUDE.md but .md files not created
