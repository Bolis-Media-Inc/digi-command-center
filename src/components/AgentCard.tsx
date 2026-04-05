'use client'

import { Agent, AgentRun } from '@/lib/supabase'
import { Activity, AlertCircle, CheckCircle2, Clock } from 'lucide-react'

interface AgentCardProps {
  agent: Agent
  latestRun: AgentRun | null
}

export function AgentCard({ agent, latestRun }: AgentCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'bg-blue-50 border-blue-200'
      case 'completed':
        return 'bg-green-50 border-green-200'
      case 'failed':
        return 'bg-red-50 border-red-200'
      default:
        return 'bg-gray-50 border-gray-200'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running':
        return <Activity className="w-4 h-4 text-blue-600 animate-pulse" />
      case 'completed':
        return <CheckCircle2 className="w-4 h-4 text-green-600" />
      case 'failed':
        return <AlertCircle className="w-4 h-4 text-red-600" />
      default:
        return <Clock className="w-4 h-4 text-gray-600" />
    }
  }

  const status = latestRun?.status || 'idle'
  const progress = latestRun?.progress_percent || 0

  return (
    <div className={`border rounded-lg p-4 ${getStatusColor(status)}`}>
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-semibold text-lg">{agent.name}</h3>
          <p className="text-sm text-gray-600 capitalize">{agent.role}</p>
        </div>
        {getStatusIcon(status)}
      </div>

      {latestRun && (
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Status:</span>
            <span className="font-medium capitalize">{status}</span>
          </div>

          {status === 'running' && (
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
          )}

          {latestRun.started_at && (
            <div className="text-xs text-gray-500">
              Started: {new Date(latestRun.started_at).toLocaleTimeString()}
            </div>
          )}
        </div>
      )}

      {!latestRun && (
        <p className="text-sm text-gray-500">No runs yet</p>
      )}
    </div>
  )
}
