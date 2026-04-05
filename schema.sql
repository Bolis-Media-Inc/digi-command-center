-- Digi Command Center — Agent Logging Schema
-- Architect Holdings → Digi (tech/infra) + Bolis Media (content ops)
-- Supabase implementation

-- ============================================================================
-- TEAMS & AGENTS (Structure)
-- ============================================================================

CREATE TABLE IF NOT EXISTS teams (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  description TEXT,
  component TEXT NOT NULL CHECK (component IN ('digi', 'bolis', 'command_center')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  role TEXT NOT NULL,
  personality JSONB, -- {style, traits, decision_making, key_question}
  job_id TEXT UNIQUE, -- Cron job ID
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'deprecated', 'testing')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  CONSTRAINT unique_team_role UNIQUE(team_id, role)
);

-- ============================================================================
-- RUNS & LOGS (Execution)
-- ============================================================================

CREATE TABLE IF NOT EXISTS agent_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
  job_id TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'running', 'completed', 'failed', 'cancelled')),
  progress_percent INT DEFAULT 0 CHECK (progress_percent >= 0 AND progress_percent <= 100),
  started_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE,
  error_message TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  CONSTRAINT valid_dates CHECK (started_at IS NULL OR completed_at IS NULL OR completed_at >= started_at)
);

CREATE TABLE IF NOT EXISTS agent_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_run_id UUID NOT NULL REFERENCES agent_runs(id) ON DELETE CASCADE,
  level TEXT NOT NULL CHECK (level IN ('info', 'warning', 'error', 'milestone', 'debug')),
  message TEXT NOT NULL,
  metadata JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- OUTPUTS (Deliverables)
-- ============================================================================

CREATE TABLE IF NOT EXISTS agent_outputs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_run_id UUID NOT NULL REFERENCES agent_runs(id) ON DELETE CASCADE,
  output_type TEXT NOT NULL, -- 'code', 'analysis', 'decision', 'metrics', 'file'
  title TEXT,
  content TEXT,
  metadata JSONB,
  file_path TEXT, -- For local file references
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- PERFORMANCE & ANALYTICS
-- ============================================================================

CREATE TABLE IF NOT EXISTS agent_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
  agent_run_id UUID REFERENCES agent_runs(id) ON DELETE SET NULL,
  metric_name TEXT NOT NULL,
  metric_value NUMERIC,
  unit TEXT, -- 'ms', 'percent', 'count', 'score'
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- INDEXES (Performance)
-- ============================================================================

CREATE INDEX idx_teams_component ON teams(component);
CREATE INDEX idx_agents_team_id ON agents(team_id);
CREATE INDEX idx_agents_job_id ON agents(job_id);
CREATE INDEX idx_agent_runs_agent_id ON agent_runs(agent_id);
CREATE INDEX idx_agent_runs_status ON agent_runs(status);
CREATE INDEX idx_agent_runs_created ON agent_runs(created_at DESC);
CREATE INDEX idx_agent_logs_run_id ON agent_logs(agent_run_id);
CREATE INDEX idx_agent_logs_created ON agent_logs(created_at DESC);
CREATE INDEX idx_agent_logs_level ON agent_logs(level);
CREATE INDEX idx_agent_outputs_run_id ON agent_outputs(agent_run_id);
CREATE INDEX idx_agent_metrics_agent_id ON agent_metrics(agent_id);
CREATE INDEX idx_agent_metrics_created ON agent_metrics(created_at DESC);

-- ============================================================================
-- ROW LEVEL SECURITY (Optional)
-- ============================================================================

ALTER TABLE teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_outputs ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_metrics ENABLE ROW LEVEL SECURITY;

-- Public read, authenticated write
CREATE POLICY "teams_read" ON teams FOR SELECT USING (true);
CREATE POLICY "teams_write" ON teams FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "agents_read" ON agents FOR SELECT USING (true);
CREATE POLICY "agents_write" ON agents FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "agent_runs_read" ON agent_runs FOR SELECT USING (true);
CREATE POLICY "agent_runs_write" ON agent_runs FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "agent_logs_read" ON agent_logs FOR SELECT USING (true);
CREATE POLICY "agent_logs_write" ON agent_logs FOR INSERT USING (auth.role() = 'authenticated');

CREATE POLICY "agent_outputs_read" ON agent_outputs FOR SELECT USING (true);
CREATE POLICY "agent_outputs_write" ON agent_outputs FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "agent_metrics_read" ON agent_metrics FOR SELECT USING (true);
CREATE POLICY "agent_metrics_write" ON agent_metrics FOR INSERT USING (auth.role() = 'authenticated');
