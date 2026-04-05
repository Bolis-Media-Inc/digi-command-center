# Digi Command Center — Deployment Guide

## ✅ Quick Start (2 min setup)

### Step 1: Deploy Supabase Schema

Open Supabase SQL Editor and run the SQL from `schema.sql`:

**Link:** https://app.supabase.com/project/ynyeuuxynwfzukvvxxlp/sql

**Steps:**
1. Go to the SQL Editor
2. Create a new query
3. Copy entire contents of `~/.hermes/digi-command-center/schema.sql`
4. Click "Run" (▶️)
5. Verify all tables created ✅

**What gets created:**
- `teams` — Agent teams
- `agents` — Individual agent roles
- `agent_runs` — Execution records
- `agent_logs` — Real-time progress logs
- `agent_outputs` — Deliverables
- `agent_metrics` — Performance data
- Indexes + RLS policies

---

### Step 2: Seed Teams & Agents

After schema is deployed, run this in SQL Editor:

```sql
-- Insert Digi Content Team
INSERT INTO teams (name, description, component)
VALUES (
  'Digi Content Team',
  'Core content sourcing, ranking, packaging, approval, publishing, and analytics pipeline',
  'digi'
);

-- Get the team ID
SELECT id INTO team_id FROM teams WHERE name = 'Digi Content Team' LIMIT 1;

-- Insert agents
INSERT INTO agents (team_id, name, role, personality) VALUES
  (
    (SELECT id FROM teams WHERE name = 'Digi Content Team' LIMIT 1),
    'Scout',
    'sourcer',
    '{"style": "Relentless hunter, pattern spotter, trend detector", "traits": ["Curious", "Pattern recognition", "Multi-channel aware", "Opportunity-focused"]}'::jsonb
  ),
  (
    (SELECT id FROM teams WHERE name = 'Digi Content Team' LIMIT 1),
    'Judge',
    'ranker',
    '{"style": "Critical analyst, quality gatekeeper", "traits": ["Analytically rigorous", "Context-aware ranking", "ML-informed", "Systematic"]}'::jsonb
  ),
  (
    (SELECT id FROM teams WHERE name = 'Digi Content Team' LIMIT 1),
    'Artisan',
    'packager',
    '{"style": "Creative formatter, brand voice embodiment", "traits": ["Format optimizing", "Brand voice guardian", "Platform-native", "Visual harmonist"]}'::jsonb
  ),
  (
    (SELECT id FROM teams WHERE name = 'Digi Content Team' LIMIT 1),
    'Guardian',
    'approver',
    '{"style": "Final checkpoint, brand protection", "traits": ["Brand alignment obsessive", "Risk-aware", "Fast gates", "Escalation-savvy"]}'::jsonb
  ),
  (
    (SELECT id FROM teams WHERE name = 'Digi Content Team' LIMIT 1),
    'Executor',
    'publisher',
    '{"style": "Distribution strategist, timing expert", "traits": ["Timing-sensitive", "Multi-channel coordinator", "Reliability focused", "Performance tracker"]}'::jsonb
  ),
  (
    (SELECT id FROM teams WHERE name = 'Digi Content Team' LIMIT 1),
    'Oracle',
    'analytics',
    '{"style": "Data scientist, feedback loop designer", "traits": ["Pattern synthesizer", "Feedback mechanism builder", "Story-teller", "Continuous optimizer"]}'::jsonb
  );
```

---

### Step 3: Create Environment File

Create `~/.hermes/digi-command-center/.env.local`:

```bash
# Supabase
SUPABASE_URL=https://ynyeuuxynwfzukvvxxlp.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlueWV1dXh5bndmenVrdnZ4eGxwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjI1NjYyNCwiZXhwIjoyMDg3ODMyNjI0fQ.yK9zsYBlMco3ExSn8JlKZvrFIseFHHlMkF8g1fIyRqU

# Dashboard (public/anon key — get from Supabase)
NEXT_PUBLIC_SUPABASE_URL=https://ynyeuuxynwfzukvvxxlp.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlueWV1dXh5bndmenVrdnZ4eGxwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIyNTY2MjQsImV4cCI6MjA4NzgzMjYyNH0.qYxkY0N_yfnXM1qXpUIQb5zXjZcVwEZbC0Y7QDXZ2hs

# Obsidian
OBSIDIAN_VAULT=/Users/connorgreene/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault
```

---

### Step 4: Test Logger

```bash
cd ~/.hermes/digi-command-center
python3 logger.py
```

Expected output:
```
[INFO] Scout: Initializing Scout agent
[INFO] Scout: Scanning Instagram feeds
[MILESTONE] Scout: Found 5 trending posts
[INFO] Scout: Filtering for quality
[MILESTONE] Scout: Output added: analysis
[MILESTONE] Scout: Run completed: Success
```

Files created:
- Supabase: 1 run + logs
- Obsidian: `Digi/agent_runs/test-sourcer-001.md`
- JSON: `~/.hermes/digi-logs/test-sourcer-001.jsonl`

---

## 🎯 What's Next

After deployment:

1. **Build Dashboard** (MVP: agent grid + logs + metrics)
2. **Extend Obsidian Sync** (integrate with existing cron)
3. **Test End-to-End** (single agent run with full logging)
4. **Deploy to Railway** (web UI)

**Timeline:** ~3-4 hours for full system

---

## 🔗 Useful Links

- **Supabase Dashboard:** https://app.supabase.com/project/ynyeuuxynwfzukvvxxlp
- **SQL Editor:** https://app.supabase.com/project/ynyeuuxynwfzukvvxxlp/sql
- **API Docs:** https://app.supabase.com/project/ynyeuuxynwfzukvvxxlp/api

---

## ❓ Troubleshooting

**Schema deployment fails:**
- Check that you're logged in to Supabase
- Use the dashboard SQL editor instead of CLI

**Logger can't connect:**
- Verify `.env.local` has correct URL + service key
- Check firewall/proxy settings

**Obsidian sync fails:**
- Verify `OBSIDIAN_VAULT` path exists
- Check folder permissions

---

## Files Location

All deployment files ready at:
```
~/.hermes/digi-command-center/
├── schema.sql                 ✅
├── agent_personas.yaml        ✅
├── logger.py                  ✅
├── deploy_schema.py           ✅
├── .env.local                 (create this)
└── dashboard/                 (next phase)
```
