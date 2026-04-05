import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || ''
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Types
export interface Team {
  id: string
  name: string
  description: string
  component: 'digi' | 'bolis' | 'command_center'
}

export interface Agent {
  id: string
  team_id: string
  name: string
  role: string
  personality: Record<string, any>
  job_id: string | null
  status: 'active' | 'deprecated' | 'testing'
}

export interface AgentRun {
  id: string
  agent_id: string
  job_id: string
  status: 'scheduled' | 'running' | 'completed' | 'failed' | 'cancelled'
  progress_percent: number
  started_at: string | null
  completed_at: string | null
  error_message: string | null
}

export interface AgentLog {
  id: string
  agent_run_id: string
  level: 'info' | 'warning' | 'error' | 'milestone' | 'debug'
  message: string
  metadata: Record<string, any>
  created_at: string
}
