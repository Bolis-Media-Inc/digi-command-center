# Digi Command Center — Implementation Spec

**Status:** Phase 1 Foundation (In Progress)  
**Last Updated:** Apr 4, 2026

---

## ✅ Phase 1 Complete

### 1.1 Supabase Schema
- **File:** `schema.sql`
- **Status:** Ready to deploy
- **Next:** Execute SQL in Supabase console
- **Tables:** `teams`, `agents`, `agent_runs`, `agent_logs`, `agent_outputs`, `agent_metrics`
- **Security:** RLS policies enabled (public read, authenticated write)

### 1.2 Agent Personalities
- **File:** `agent_personas.yaml`
- **Status:** Complete with 6 roles
- **Roles Defined:**
  - **Scout** (Sourcer) — Trend hunter, pattern spotter
  - **Judge** (Ranker) — Quality gatekeeper, ML-informed
  - **Artisan** (Packager) — Format optimizer, brand voice
  - **Guardian** (Approver) — Brand protector, final gate
  - **Executor** (Publisher) — Distribution strategist, timing expert
  - **Oracle** (Analytics) — Performance translator, feedback designer

### 1.3 Logging Integration
- **File:** `logger.py`
- **Status:** Ready for integration
- **Destinations:** Supabase + Obsidian + JSON
- **Usage:** Import `DigiLogger` in agent code, call `start_run()` → `log()` → `complete()`
- **Example:** See end of `logger.py`

### 1.4 Agent Cleanup
- **Status:** Done
- **Actions Taken:**
  - ✅ Removed monitor cronjob (8a32046031be)
  - ✅ All 7 agents completed and local-only
  - ✅ Telegram spam eliminated

---

## 🚀 Phase 2: Dashboard + Visualization

### 2.1 Dashboard Requirements
**Location:** Railway deployment  
**Tech Stack:** Next.js 14 + Supabase + Tailwind + Lucide icons

**MVP Features:**
- [ ] Real-time agent status grid (6 agents, status badges)
- [ ] Live log tail (last 50 messages, color-coded by level)
- [ ] Progress bars per agent
- [ ] Performance metrics (avg completion time, error rate, today's runs)
- [ ] Team selector (Digi Content Team + future teams)
- [ ] Error details panel

**File Structure:**
```
dashboard/
├── package.json
├── next.config.js
├── public/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── api/
│   │       └── logs/route.ts (Supabase query endpoint)
│   ├── components/
│   │   ├── AgentGrid.tsx
│   │   ├── LogTail.tsx
│   │   ├── ProgressBar.tsx
│   │   └── MetricsCard.tsx
│   ├── lib/
│   │   ├── supabase.ts (client)
│   │   └── types.ts
│   └── styles/
│       └── globals.css
└── tailwind.config.js
```

### 2.2 Obsidian Integration
**Cron Job:** Extend existing `supabase_content_intel_sync.py`  
**Sync:** Every 30 min during agent runs, daily summary

**Output Location:**
- Central Intel: Daily/YYYY-MM-DD.md (summary section)
- Archive: Digi/agent_runs/[run-date].md (detailed logs)

### 2.3 Deployment
**Platform:** Railway (existing master-telegram setup)  
**Environment Variables:**
```
SUPABASE_URL=https://...
SUPABASE_KEY=...
NEXT_PUBLIC_SUPABASE_URL=https://...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
```

**Deploy:**
```bash
cd dashboard
git push railway main
```

---

## 📋 Phase 3: Operational Launch

### 3.1 Setup Checklist
- [ ] Deploy schema.sql to Supabase
- [ ] Seed agents table from agent_personas.yaml
- [ ] Assign job IDs from cron registry to agents
- [ ] Deploy dashboard to Railway
- [ ] Extend Obsidian sync cron
- [ ] Configure Telegram alerts (errors + summaries only)

### 3.2 Job Registry
**Purpose:** Map cron job IDs to agent roles

**Format:** `digi-agents.yaml`
```yaml
digi_content_team:
  sourcer:
    job_id: [to-assign]
    schedule: "0 1 * * *"  # 01:30 AM
  ranker:
    job_id: [to-assign]
    schedule: "0 2 * * *"  # 02:00 AM
  # ... etc
```

### 3.3 Telegram Alerting Strategy
**During runs:** Silent (no messages)  
**On completion:** Summary (errors + key metrics)  
**On failure:** Error alert to @operations_bolismedia

**Logic:**
```
if status == "failed":
  send_telegram(error_details)
elif status == "completed":
  send_telegram(summary_metrics)
```

---

## 🔧 Integration Points

### With Existing Cron System
- Logger writes job_id → Supabase `agent_runs.job_id`
- Cronjob engine reads `agent_runs.status` to coordinate pipeline
- Future: Agent outputs trigger next agent in pipeline

### With Obsidian
- Daily sync pulls `agent_runs` from Supabase
- Inserts into Central Intel for morning review
- Historical archive for trend analysis

### With Telegram
- master-telegram MCP monitors for delivery config
- Sends alerts to @operations_bolismedia
- Dashboard link for live viewing

---

## 📝 Configuration

### Environment Setup
```bash
# .env.local (for local development)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-key
OBSIDIAN_VAULT=/Users/connorgreene/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault

# For dashboard (public/anon key for frontend)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### Obsidian Vault Structure
```
Central Intel/
├── Daily/
│   └── 2026-04-04.md (includes Digi Agent Summary section)
└── Digi/
    ├── agent_runs/
    │   └── [job-id].md (detailed run logs)
    └── metrics/
        └── 2026-04.md (monthly aggregates)
```

---

## 🎯 Success Metrics

- ✅ Zero Telegram spam during agent runs
- ✅ <1 sec dashboard page load (real-time via Supabase)
- ✅ 100% log capture (Supabase + Obsidian + JSON)
- ✅ Agent personality system adopted (names used in logs/outputs)
- ✅ Morning review: Connor scans Digi summary in Daily.md in <2 min

---

## 🚨 Known Issues / Blockers

**None yet. Ready to build!**

---

## Next Steps
1. **Confirm Supabase credentials** with Connor
2. **Deploy schema.sql** to Supabase
3. **Build dashboard MVP** (AgentGrid + LogTail)
4. **Extend Obsidian sync cron**
5. **Test end-to-end** with a single agent run
