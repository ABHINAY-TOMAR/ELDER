import { Bot, PlayCircle, CheckCircle, XCircle, Clock, Loader2, Zap } from 'lucide-react'
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'
import { useState } from 'react'
import type { SessionState, AgentDispatch, InteractionOption } from '../lib/types'
import { stepSession } from '../lib/api'

interface DispatchPanelProps {
  session: SessionState | null
  onSessionUpdate: (session: SessionState) => void
}

const STATUS_CONFIG = {
  queued: { icon: Clock, color: 'var(--text-muted)', bg: 'var(--surface-glass)', border: 'var(--border-glass)', spin: false },
  running: { icon: Loader2, color: '#a78bfa', bg: 'rgba(99, 102, 241, 0.06)', border: 'rgba(99, 102, 241, 0.2)', spin: true },
  completed: { icon: CheckCircle, color: '#4ade80', bg: 'rgba(34, 197, 94, 0.06)', border: 'rgba(34, 197, 94, 0.2)', spin: false },
  failed: { icon: XCircle, color: '#f87171', bg: 'rgba(239, 68, 68, 0.06)', border: 'rgba(239, 68, 68, 0.2)', spin: false },
}

function InteractionCard({ 
  question, 
  options, 
  field, 
  sessionId, 
  onUpdate 
}: { 
  question: string; 
  options: InteractionOption[]; 
  field: string; 
  sessionId: string;
  onUpdate: (s: SessionState) => void 
}) {
  const [loadingId, setLoadingId] = useState<string | null>(null);

  const handleSelect = async (optionId: string) => {
    try {
      setLoadingId(optionId);
      const updated = await stepSession(sessionId, optionId);
      onUpdate(updated);
    } catch (error) {
      console.error('Failed to respond to interaction:', error);
    } finally {
      setLoadingId(null);
    }
  };

  return (
    <div className="glass-card p-6 border-primary bg-primary/5 animate-pulse-subtle mb-6">
      <div className="flex items-center gap-3 mb-4 text-primary">
        <Bot className="w-5 h-5 text-violet-400" />
        <h3 className="font-semibold text-sm">Action Required</h3>
      </div>
      
      <p className="text-sm font-medium mb-5 text-secondary">
        {question}
      </p>

      <div className="grid grid-cols-1 gap-2.5">
        {options.map((option) => (
          <button
            key={option.id}
            onClick={() => handleSelect(option.id)}
            disabled={loadingId !== null}
            className={`flex items-center justify-between px-4 py-3 rounded-xl border transition-all text-xs font-medium ${
              option.recommended 
                ? 'border-violet-500/30 bg-violet-500/10 text-violet-400 hover:bg-violet-500/20' 
                : 'border-glass bg-surface-glass hover:bg-surface-glass-light text-secondary'
            }`}
          >
            <span>{option.label}</span>
            {loadingId === option.id ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
            ) : (
              option.recommended && <Zap className="w-3 h-3 fill-current" />
            )}
          </button>
        ))}
      </div>
      
      <p className="mt-4 text-[10px] text-muted text-center uppercase tracking-widest">
        Field: {field.replace('_', ' ')}
      </p>
    </div>
  );
}

function DispatchCard({ dispatch, index }: { dispatch: AgentDispatch; index: number }) {
  const config = STATUS_CONFIG[dispatch.status]
  const StatusIcon = config.icon

  return (
    <div
      className={`glass-card p-5 animate-slide-up stagger-${Math.min(index + 1, 5)} border-glass`}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-lg bg-violet-500/10">
            <Bot className="w-4 h-4 text-violet-400" />
          </div>
          <span className="font-semibold text-sm text-primary">
            {dispatch.agent_name}
          </span>
        </div>
        <span
          className={`badge ${
            dispatch.status === 'running' ? 'badge-info' :
            dispatch.status === 'completed' ? 'badge-success' :
            dispatch.status === 'failed' ? 'badge-error' :
            'badge-info opacity-70'
          }`}
        >
          <StatusIcon className={`w-3 h-3 ${config.spin ? 'animate-spin' : ''}`} />
          {dispatch.status}
        </span>
      </div>

      <p className="text-sm mb-3 text-secondary">
        {dispatch.task}
      </p>

      {dispatch.result && (
        <div className="p-3 rounded-xl text-xs font-mono overflow-auto max-h-32 scrollbar-thin bg-surface-glass-light border border-glass text-muted">
          {dispatch.result}
        </div>
      )}

      {dispatch.error && (
        <div className="p-3 rounded-xl text-xs bg-red-500/5 border border-red-500/20 text-red-400">
          {dispatch.error}
        </div>
      )}

      <div className="mt-3 pt-3 flex items-center justify-between text-xs border-t border-glass text-muted">
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

function DispatchSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {[1, 2].map((i) => (
        <div key={i} className="glass-card p-5">
          <div className="flex items-center gap-2.5 mb-3">
            <Skeleton circle width={32} height={32} />
            <Skeleton width={120} height={16} />
          </div>
          <Skeleton count={2} height={12} />
          <div className="mt-3">
            <Skeleton height={40} borderRadius={12} />
          </div>
        </div>
      ))}
    </div>
  )
}

export default function DispatchPanel({ session, onSessionUpdate }: DispatchPanelProps) {
  const dispatches = session?.dispatches || []
  const runningCount = dispatches.filter((d) => d.status === 'running').length
  const completedCount = dispatches.filter((d) => d.status === 'completed').length
  const failedCount = dispatches.filter((d) => d.status === 'failed').length

  return (
    <div className="glass-panel">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-gradient-to-br from-violet-500/20 to-indigo-500/20 border border-violet-500/20">
            <Zap className="w-4 h-4 text-violet-400" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-primary">
              Agent Dispatch
            </h2>
            <p className="text-xs text-muted">
              {dispatches.length > 0 ? 'Active agents' : 'Agent orchestration'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3 text-xs">
          {runningCount > 0 && (
            <span className="badge badge-info">
              <Loader2 className="w-3 h-3 animate-spin" />
              {runningCount} running
            </span>
          )}
          {completedCount > 0 && (
            <span className="badge badge-success">
              <CheckCircle className="w-3 h-3" />
              {completedCount} done
            </span>
          )}
          {failedCount > 0 && (
            <span className="badge badge-error">
              <XCircle className="w-3 h-3" />
              {failedCount} failed
            </span>
          )}
        </div>
      </div>

      {session?.pending_interaction && (
        <InteractionCard 
          {...session.pending_interaction} 
          sessionId={session.id}
          onUpdate={onSessionUpdate}
        />
      )}

      {!session ? (
        <DispatchSkeleton />
      ) : (dispatches.length === 0 && !session.pending_interaction) ? (
        <div className="text-center py-14">
          <div className="w-16 h-16 mx-auto mb-4 rounded-2xl flex items-center justify-center bg-surface-glass-light">
            <PlayCircle className="w-8 h-8 text-muted" />
          </div>
          <h3 className="text-base font-medium mb-1.5 text-secondary">No Agents Dispatched</h3>
          <p className="text-sm text-muted">
            Agents will appear here when dispatched
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {dispatches.map((dispatch, i) => (
            <DispatchCard key={dispatch.id} dispatch={dispatch} index={i} />
          ))}
        </div>
      )}
    </div>
  )
}
