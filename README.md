# Digi Command Center

**Status:** Phase 1 Complete ✅ | Phase 2 Ready

---

## 🎯 What This Is

A complete logging + visualization system for Digi's 6-agent content pipeline:
- **Scout** (Sourcer) → **Judge** (Ranker) → **Artisan** (Packager) → **Guardian** (Approver) → **Executor** (Publisher) → **Oracle** (Analytics)

Every agent run is logged to **Supabase** (real-time) + **Obsidian** (persistent) + **JSON** (backup).

Dashboard (coming Phase 2) provides live web UI on Railway.

---

## 📋 Phase 1: Foundation ✅ Complete

### What's Built

**1. Agent Personalities** (`agent_personas.yaml`)
- Each agent has unique role, traits, decision-making style
- Humanizes the pipeline: Scout hunts trends, Judge gates quality, etc.

**2. Supabase Schema** (`schema.sql`)
- 6 core tables: teams, agents, agent_runs, agent_logs, agent_outputs, agent_metrics
- Indexes for performance, RLS policies for security
- Ready to deploy

**3. Logging Library** (`logger.py`)
- Simple Python class: `DigiLogger`
- Writes to: Supabase + Obsidian + JSON
- Usage: `logger.start_run()` → `logger.log()` → `logger.complete()`

**4. Implementation Spec** (`IMPLEMENTATION.md`)
- Full technical roadmap
- Phase 2 & 3 details
- Success metrics

---

## 🚀 Phase 2: Dashboard (Next)

### Requirements
- Real-time agent status grid (6 agents, progress bars)
- Live log tail (last 50 messages, color-coded)
- Performance metrics (completion time, error rate)
- Team selector
- Error details panel

### Stack
- Next.js 14 + Supabase + Tailwind + Lucide
- Deployed to Railway

### Files
- `dashboard/package.json` (starter config)
- Starter: Next pages + Supabase client components

---

## 📝 Quick Start (2 min)

### 1. Deploy Schema

Read: `DEPLOYMENT_GUIDE.md` → Run `schema.sql` in Supabase SQL Editor

### 2. Test Logger

```bash
python3 logger.py
```

Verify logs appear in:
- Supabase: agent_runs + agent_logs tables
- Obsidian: `Digi/agent_runs/test-sourcer-001.md`
- JSON: `~/.hermes/digi-logs/test-sourcer-001.jsonl`

### 3. Integrate with Agents

In each agent cron job:
```python
from logger import DigiLogger

logger = DigiLogger("Scout", "sourcer", job_id="job-123")
logger.start_run()
logger.log("Starting scan", level="info")
logger.set_progress(50)
logger.add_output("analysis", content="...")
logger.complete("completed")
```

---

## 🔗 Important URLs

- **Supabase Project:** https://app.supabase.com/project/ynyeuuxynwfzukvvxxlp
- **SQL Editor:** https://app.supabase.com/project/ynyeuuxynwfzukvvxxlp/sql
- **API Reference:** https://app.supabase.com/project/ynyeuuxynwfzukvvxxlp/api

---

## 🏗️ Architecture

```
Digi Agents (6 roles)
        ↓
  DigiLogger (Python)
        ↓
  ┌─────┼─────┐
  ↓     ↓     ↓
 SUP  OBS   JSON
  ↓     ↓     ↓
 RT   SEARCH BACKUP
  
Dashboard (Next.js on Railway) ← reads from Supabase
                                reads from Obsidian
```

**Data Flow:**
1. Agent runs → logger writes to 3 destinations
2. Dashboard polls Supabase every 2sec (live)
3. Obsidian sync pulls data every 30min
4. Connor reviews daily in Obsidian Daily.md

---

## 📂 File Structure

```
~/.hermes/digi-command-center/
├── README.md                   ← You are here
├── NEXT_STEPS.md              ← Original plan
├── DEPLOYMENT_GUIDE.md        ← How to deploy
├── IMPLEMENTATION.md          ← Technical spec
│
├── schema.sql                 ← Supabase schema (deploy this)
├── agent_personas.yaml        ← 6 agent definitions
├── logger.py                  ← Logging library
├── deploy_schema.py           ← Schema deployment script
│
└── dashboard/                 ← Phase 2 (Next.js app)
    └── package.json           ← Starter config
```

---

## ✅ Success Checklist

- [ ] Schema deployed to Supabase
- [ ] Teams + agents seeded in database
- [ ] `.env.local` created with credentials
- [ ] `logger.py` tested (creates files)
- [ ] Dashboard MVP built
- [ ] Obsidian sync extended
- [ ] First agent run integrated
- [ ] Telegram alerts configured (errors only)
- [ ] Deployed to Railway

---

## 🎓 Key Design Decisions

1. **Structured Logging Everywhere**
   - Supabase: Real-time, queryable, integrations
   - Obsidian: Human-readable, searchable, part of daily workflow
   - JSON: Machine-readable, backup, debugging

2. **Agent Personalities**
   - Names (Scout, Judge, etc.) make logs more readable
   - Persona docs define decision-making style
   - Future: Can use personality in prompt context

3. **No Telegram Spam During Runs**
   - Dashboard is source of truth for live view
   - Only high-level alerts sent to Telegram (errors + summaries)
   - Obsidian Daily.md has quick summary for morning

4. **Railway Deployment**
   - Master-telegram MCP already on Railway
   - Dashboard can share same Railway project
   - Easy CI/CD via git push

---

## 🔧 Development

### Add New Agent

1. Add to `agent_personas.yaml`
2. Run SQL to seed agents table
3. Assign job_id from cron registry
4. Agent code imports DigiLogger and logs to all destinations

### Extend Logger

Edit `logger.py` to add:
- Custom metrics (current: progress %)
- File uploads
- Integration with other services (Slack, Discord, etc.)

### Build Dashboard

1. Create Next.js pages in `dashboard/src/app`
2. Components: AgentGrid.tsx, LogTail.tsx, ProgressBar.tsx
3. Real-time via Supabase `on('postgres_changes')` subscriptions
4. Deploy to Railway

---

## 📞 Support

**Questions about:**
- **Logger:** Check `logger.py` docstrings + example usage at bottom
- **Schema:** See `schema.sql` comments
- **Deployment:** Read `DEPLOYMENT_GUIDE.md`
- **Architecture:** See `IMPLEMENTATION.md`

---

**Last Updated:** Apr 4, 2026  
**Maintainer:** Hermes (Claude Code)  
**License:** Internal (Architect Holdings)
