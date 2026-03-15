# RESTART.md — What Was Being Done & Where We Stopped
# Use this to resume the conversation with Claude

---

## 📍 LAST STATE (2026-03-15)

### What just happened
1. ✅ Built entire IT CIO Workspace from scratch
2. ✅ Pushed to GitHub: https://github.com/ndlong75/it-cio-workspace
3. ✅ Reviewed all 29 files — all PASS
4. ✅ Made repo public
5. ⏳ GitHub Pages — tried to enable but couldn't find Settings → Pages
6. 📝 Created memory.md / restart.md / backlog.md (this session end)

### Last conversation topic
Trying to enable **GitHub Pages** to view HTML files online.
Issue: User couldn't find "Pages" in Settings menu.
Likely cause: Repo was private — now public so Pages should appear.

### How to resume
```
Tell Claude: "Read restart.md and continue where we left off"
```

---

## 🔄 IMMEDIATE NEXT STEPS (in order)

### 1. Enable GitHub Pages (5 min)
```
github.com/ndlong75/it-cio-workspace
→ Settings → Pages (left sidebar, under "Code and automation")
→ Source: Deploy from branch
→ Branch: main, folder: / (root)
→ Save
→ Wait ~2 min
→ All HTML live at: https://ndlong75.github.io/it-cio-workspace/output/[filename].html
```

### 2. Fill in config/people.yaml (10 min)
```
Open: it-cio-workspace/config/people.yaml
Fill in real names, emails, Teams IDs for:
- cio, dev_lead, pm, infra_lead, security_lead, snow_lead
- on_call rotation (2 people + phone numbers)
- ceo, cfo, legal, hr
- Teams channel IDs/names
```

### 3. Copy .env.example → .env and fill API keys (20 min)
```
cp .env.example .env
Fill in:
- ANTHROPIC_API_KEY
- JIRA_URL + JIRA_EMAIL + JIRA_TOKEN
- GITHUB_TOKEN + GITHUB_ORG
- M365 connector (via Cowork settings, not manual)
```

### 4. Open workspace in Claude Code (5 min)
```
claude code /path/to/it-cio-workspace
→ "Read CLAUDE.md and introduce the system"
→ Test: /daily
→ Test: /incident "test incident"
```

---

## 💬 HOW TO RESTART CONVERSATION WITH CLAUDE

Paste this at the start of new conversation:
```
I'm the IT Head at a Vietnamese insurance company.
Read my restart.md file — it has context on what we built.
GitHub repo: https://github.com/ndlong75/it-cio-workspace

What I need next: [your specific task]
```

---

## 📁 KEY FILES TO KNOW

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Entry point — Claude reads this first |
| `config/people.yaml` | Who gets notified for what |
| `agents/cio_agent.md` | CIO agent persona + all 5 workflows |
| `output/cosmic-diagram.html` | Visual overview of whole system |
| `output/agent-flows-en.html` | Full detailed workflows with sources |
| `output/human-intervention.html` | When/how human must intervene |
