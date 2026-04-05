# Digi Command Center — Next Steps

**Date:** Apr 4, 2026 | **Status:** Architecture phase

---

## Context
- **Structure:** Architect Holdings (parent) → Digi (tech/infra) + Bolis Media (content ops)
- **Current:** 7 Digi agents running (de72651628fc, 316172aab9dc, 756709f6c09f, 34b86463ef67, 5a98d2a2adb8, ef026f1ab21a, 9e4c1564e159)
- **Issue:** Agent completion spam to Telegram — need to pause all delivery and restructure logging
- **Goal:** Build logging + visualization layer for agent framework

---

## Phase 1: Foundation (Priority)

### 1.1 Supabase Schema Setup
- [ ] Create Digi schema in Supabase (use existing project or ask Connor for URL/API keys)
- [ ] Tables: `teams`, `agents`, `agent_runs`, `agent_logs`, `agent_outputs`
- [ ] Indexes for performance (run_id, status, created_at)
- [ ] Service role key for programmatic access

**File:** `~/.hermes/digi-command-center/schema.sql`

### 1.2 Agent Personalities + Naming
Define unique personas for 6-agent pipeline:
- **Sourcer** — Role, traits, decision style
- **Ranker** — Role, traits, decision style  
- **Packager** — Role, traits, decision style
- **Approver** — Role, traits, decision style
- **Publisher** — Role, traits, decision style
- **Analytics** — Role, traits, decision style

**Output:** `~/.hermes/digi-command-center/agent_personas.yaml`

### 1.3 Structured Logging Integration
- [ ] Python logger that writes to:
  - Supabase (real-time)
  - Obsidian Central Intel (searchable narrative)
  - Local JSON (backup + debugging)
- [ ] Hook into existing cron job system (7 agents report metrics/progress)
- [ ] Suppress Telegram delivery during runs (only high-level summaries after completion)

**File:** `~/.hermes/digi-command-center/logger.py`

### 1.4 Pause All Active Agent Deliveries
- [ ] Update 7 running jobs to deliver to `local` only (not `origin`)
- [ ] Kill the monitor cronjob (8a32046031be)
- [ ] Test: Confirm no messages sent to Telegram during agent runs

---

## Phase 2: Dashboard + Visualization

### 2.1 Web Dashboard (Next.js on Railway)
- [ ] Real-time job status + progress bars
- [ ] Live log tail (last 50 messages)
- [ ] Agent performance metrics (completion time, error rate)
- [ ] Team view (Digi content team + future teams)
- [ ] Error tracking + alerting

**Stack:** Next.js + Supabase + Tailwind

### 2.2 Obsidian Integration
- [ ] Auto-sync agent_runs + agent_logs to Obsidian Central Intel
- [ ] Daily summary view (Daily/YYYY-MM-DD.md)
- [ ] Historical archive (Digi/agent_runs/)

**Cron:** Already exists (supabase_content_intel_sync.py) — extend it

---

## Phase 3: Operational Launch

### 3.1 Define Teams
- **Digi Content Team** (initial): Sourcer → Ranker → Packager → Approver → Publisher → Analytics
- Plan for future teams (Bolis, Command Center sub-teams, etc.)

### 3.2 Job Registry
- Assign job IDs to agent roles (persistent mapping)
- Document SOP for triggering teams

### 3.3 Monitoring + Alerting
- High-level Telegram alerts (only errors + completion summaries, not progress spam)
- Dashboard as source of truth

---

## Files to Create
1. `~/.hermes/digi-command-center/schema.sql` — Supabase schema
2. `~/.hermes/digi-command-center/agent_personas.yaml` — Agent personalities
3. `~/.hermes/digi-command-center/logger.py` — Structured logging
4. `~/.hermes/digi-command-center/dashboard/` — Next.js app
5. `~/.hermes/digi-command-center/IMPLEMENTATION.md` — Technical spec

---

## Immediate Actions (Restart Session)
1. **Pause/kill all monitors** (confirm no more Telegram spam)
2. **Create Supabase schema** (ask Connor for connection details if needed)
3. **Define agent personas** (get Connor's input on personality types)
4. **Build logger integration** (hook into existing cron system)
5. **Sketch dashboard** (minimal MVP: job list + status + logs)

---

## Notes
- Connor prefers morning workflow: scan 2-3 min, plan day
- Logging should be everywhere but Telegram notifications minimal (errors + summaries only)
- Railway deployment ready (master-telegram + other services already there)
- Use Obsidian as persistent record, dashboard as live view
