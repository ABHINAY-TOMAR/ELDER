import { Bot, PlayCircle, CheckCircle, XCircle, Clock, Loader2 } from 'lucide-react'
import clsx from 'clsx'
import type { SessionState, AgentDispatch } from '../lib/types'

interface DispatchPanelProps {
  session: SessionState | null
}

const STATUS_ICONS = {
  queued: Clock,
  running: Loader2,
  completed: CheckCircle,
  failed: XCircle,
}

const STATUS_STYLES = {
  queued: 'text-slate-400 bg-slate-400/10',
  running: 'text-violet-400 bg-violet-400/10 animate-pulse',
  completed: 'text-green-400 bg-green-400/10',
  failed: 'text-red-400 bg-red-400/10',
}

function DispatchCard({ dispatch }: { dispatch: AgentDispatch }) {
  const StatusIcon = STATUS_ICONS[dispatch.status]

  return (
    <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <Bot className="w-4 h-4 text-violet-400" />
          <span className="font-medium text-slate-200">{dispatch.agent_name}</span>
        </div>
        <span className={clsx('flex items-center gap-1 px-2 py-0.5 text-xs rounded-full', STATUS_STYLES[dispatch.status])}>
          {dispatch.status === 'running' ? (
            <StatusIcon className="w-3 h-3 animate-spin" />
          ) : (
            <StatusIcon className="w-3 h-3" />
          )}
          {dispatch.status}
        </span>
      </div>

      <p className="text-sm text-slate-400 mb-3">{dispatch.task}</p>

      {dispatch.result && (
        <div className="p-3 bg-slate-900/50 rounded text-xs text-slate-500 font-mono overflow-auto max-h-32">
          {dispatch.result}
        </div>
      )}

      {dispatch.error && (
        <div className="p-3 bg-red-900/20 border border-red-800/30 rounded text-xs text-red-400">
          {dispatch.error}
        </div>
      )}

      <div className="mt-3 pt-3 border-t border-slate-700/50 flex items-center justify-between text-xs text-slate-500">
        {dispatch.started_at && (
          <span>Started {new Date(dispatch.started_at).toLocaleTimeString()}</span>
        )}
        {dispatch.completed_at && (
          <span>Completed {new Date(dispatch.completed_at).toLocaleTimeString()}</span>
        )}
      </div>
    </div>
  )
}

export default function DispatchPanel({ session }: DispatchPanelProps) {
  if (!session) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4">
          <Bot className="w-5 h-5 text-violet-400" />
          <h2 className="text-lg font-semibold">Agent Dispatch</h2>
        </div>
        <p className="text-sm text-slate-500 text-center py-8">
          No agent dispatches yet
        </p>
      </div>
    )
  }

  const dispatches = session.dispatches || []
  const runningCount = dispatches.filter((d) => d.status === 'running').length
  const completedCount = dispatches.filter((d) => d.status === 'completed').length
  const failedCount = dispatches.filter((d) => d.status === 'failed').length

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Bot className="w-5 h-5 text-violet-400" />
          <h2 className="text-lg font-semibold">Agent Dispatch</h2>
        </div>
        <div className="flex items-center gap-4 text-xs">
          {runningCount > 0 && (
            <span className="flex items-center gap-1 text-violet-400">
              <Loader2 className="w-3 h-3 animate-spin" />
              {runningCount} running
            </span>
          )}
          {completedCount > 0 && (
            <span className="flex items-center gap-1 text-green-400">
              <CheckCircle className="w-3 h-3" />
              {completedCount} completed
            </span>
          )}
          {failedCount > 0 && (
            <span className="flex items-center gap-1 text-red-400">
              <XCircle className="w-3 h-3" />
              {failedCount} failed
            </span>
          )}
        </div>
      </div>

      {dispatches.length === 0 ? (
        <div className="text-center py-12">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-slate-800 flex items-center justify-center">
            <PlayCircle className="w-8 h-8 text-slate-600" />
          </div>
          <h3 className="text-lg font-medium text-slate-400 mb-2">No Agents Dispatched</h3>
          <p className="text-sm text-slate-500">Agents will appear here when dispatched</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {dispatches.map((dispatch) => (
            <DispatchCard key={dispatch.id} dispatch={dispatch} />
          ))}
        </div>
      )}
    </div>
  )
}
