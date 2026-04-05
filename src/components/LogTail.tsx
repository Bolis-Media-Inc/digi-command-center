'use client'

import { AgentLog } from '@/lib/supabase'
import { useEffect, useRef } from 'react'

interface LogTailProps {
  logs: AgentLog[]
  isLive?: boolean
}

export function LogTail({ logs, isLive = true }: LogTailProps) {
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (scrollRef.current && isLive) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [logs, isLive])

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'error':
        return 'text-red-600 bg-red-50'
      case 'warning':
        return 'text-yellow-600 bg-yellow-50'
      case 'milestone':
        return 'text-green-600 bg-green-50'
      case 'debug':
        return 'text-gray-500 bg-gray-50'
      default:
        return 'text-gray-700 bg-white'
    }
  }

  return (
    <div className="border rounded-lg bg-white">
      <div className="border-b bg-gray-50 px-4 py-2">
        <h3 className="font-semibold text-sm">Live Logs</h3>
      </div>
      <div
        ref={scrollRef}
        className="h-96 overflow-y-auto font-mono text-sm space-y-1 p-4"
      >
        {logs.length === 0 ? (
          <p className="text-gray-400">No logs yet</p>
        ) : (
          logs.map((log) => (
            <div
              key={log.id}
              className={`px-2 py-1 rounded ${getLevelColor(log.level)}`}
            >
              <span className="text-gray-500 text-xs">
                {new Date(log.created_at).toLocaleTimeString()}
              </span>
              {' '}
              <span className="font-semibold capitalize">[{log.level}]</span>
              {' '}
              <span>{log.message}</span>
              {log.metadata && Object.keys(log.metadata).length > 0 && (
                <div className="text-xs mt-1 opacity-75">
                  {JSON.stringify(log.metadata)}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}
