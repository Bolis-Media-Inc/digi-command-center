'use client'

import { useEffect, useState } from 'react'
import { supabase, Team, Agent, AgentRun, AgentLog } from '@/lib/supabase'
import { AgentCard } from '@/components/AgentCard'
import { LogTail } from '@/components/LogTail'
import { RefreshCw } from 'lucide-react'

export default function Dashboard() {
  const [team, setTeam] = useState<Team | null>(null)
  const [agents, setAgents] = useState<Agent[]>([])
  const [runs, setRuns] = useState<Record<string, AgentRun>>({})
  const [logs, setLogs] = useState<AgentLog[]>([])
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)

  // Fetch team and agents
  useEffect(() => {
    const loadTeam = async () => {
      try {
        // Get Digi Content Team
        const { data: teams, error: teamError } = await supabase
          .from('teams')
          .select('*')
          .eq('name', 'Digi Content Team')
          .single()

        if (teamError) throw teamError
        setTeam(teams)

        // Get agents for this team
        const { data: agentList, error: agentError } = await supabase
          .from('agents')
          .select('*')
          .eq('team_id', teams.id)
          .order('role', { ascending: true })

        if (agentError) throw agentError
        setAgents(agentList || [])

        // Get latest runs for each agent
        if (agentList && agentList.length > 0) {
          const runsMap: Record<string, AgentRun> = {}
          for (const agent of agentList) {
            const { data: latestRun } = await supabase
              .from('agent_runs')
              .select('*')
              .eq('agent_id', agent.id)
              .order('created_at', { ascending: false })
              .limit(1)
              .single()

            if (latestRun) {
              runsMap[agent.id] = latestRun
            }
          }
          setRuns(runsMap)

          // Get recent logs
          const runIds = Object.values(runsMap).map(r => r.id)
          if (runIds.length > 0) {
            const { data: recentLogs } = await supabase
              .from('agent_logs')
              .select('*')
              .in('agent_run_id', runIds)
              .order('created_at', { ascending: false })
              .limit(50)

            setLogs((recentLogs || []).reverse())
          }
        }
      } catch (error) {
        console.error('Failed to load team:', error)
      } finally {
        setLoading(false)
      }
    }

    loadTeam()
  }, [])

  // Real-time subscriptions
  useEffect(() => {
    if (!team) return

    // Subscribe to agent_runs changes
    const runsSubscription = supabase
      .from(`agent_runs:agent_id=in.(${agents.map(a => `${a.id}`).join(',')})`)
      .on('*', (payload) => {
        if (payload.eventType === 'INSERT' || payload.eventType === 'UPDATE') {
          setRuns(prev => ({
            ...prev,
            [payload.new.agent_id]: payload.new
          }))
        }
      })
      .subscribe()

    // Subscribe to agent_logs
    const logsSubscription = supabase
      .from('agent_logs')
      .on('INSERT', (payload) => {
        setLogs(prev => [...prev, payload.new as AgentLog].slice(-50))
      })
      .subscribe()

    return () => {
      runsSubscription.unsubscribe()
      logsSubscription.unsubscribe()
    }
  }, [team, agents])

  const handleRefresh = async () => {
    setRefreshing(true)
    try {
      // Refresh runs
      const runsMap: Record<string, AgentRun> = {}
      for (const agent of agents) {
        const { data: latestRun } = await supabase
          .from('agent_runs')
          .select('*')
          .eq('agent_id', agent.id)
          .order('created_at', { ascending: false })
          .limit(1)
          .single()

        if (latestRun) {
          runsMap[agent.id] = latestRun
        }
      }
      setRuns(runsMap)

      // Refresh logs
      const runIds = Object.values(runsMap).map(r => r.id)
      if (runIds.length > 0) {
        const { data: recentLogs } = await supabase
          .from('agent_logs')
          .select('*')
          .in('agent_run_id', runIds)
          .order('created_at', { ascending: false })
          .limit(50)

        setLogs((recentLogs || []).reverse())
      }
    } finally {
      setRefreshing(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-pulse mb-4">🤖</div>
          <p className="text-gray-600">Loading Digi Command Center...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          <h1 className="text-4xl font-bold">Digi Command Center</h1>
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="p-2 hover:bg-gray-200 rounded-lg transition disabled:opacity-50"
            title="Refresh"
          >
            <RefreshCw className={`w-5 h-5 ${refreshing ? 'animate-spin' : ''}`} />
          </button>
        </div>
        <p className="text-gray-600">{team?.description}</p>
      </div>

      {/* Agent Grid */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Agents</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {agents.map((agent) => (
            <AgentCard
              key={agent.id}
              agent={agent}
              latestRun={runs[agent.id] || null}
            />
          ))}
        </div>
      </div>

      {/* Logs */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Activity Log</h2>
        <LogTail logs={logs} isLive={true} />
      </div>
    </div>
  )
}
