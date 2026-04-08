import { AlertTriangle, ChevronDown, ChevronUp, ShieldAlert } from 'lucide-react'
import { useState } from 'react'
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'
import type { SessionState, FailureMode } from '../lib/types'

interface FailureModesPanelProps {
  session: SessionState | null
}

function FailureModeRow({ mode }: { mode: FailureMode }) {
  const [expanded, setExpanded] = useState(false)
  const riskScore =
    ({ low: 1, medium: 2, high: 3 }[mode.probability] ?? 1) *
    ({ low: 1, medium: 2, high: 3 }[mode.impact] ?? 1)
  const riskColor = riskScore >= 6 ? '#f87171' : riskScore >= 3 ? '#fbbf24' : '#4ade80'

  return (
    <div className="border-b border-glass last:border-b-0">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between p-4 transition-colors hover:bg-white/[0.02]"
      >
        <div className="flex items-center gap-3">
          <AlertTriangle className="w-4 h-4" style={{ color: riskColor }} />
          <div className="text-left">
            <p className="text-sm font-medium text-primary">
              {mode.component}
            </p>
            <p className="text-xs text-muted">
              {mode.failure_type}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span
            className={`badge ${
              mode.probability === 'low' ? 'badge-success' :
              mode.probability === 'medium' ? 'badge-warning' :
              'badge-error'
            }`}
          >
            {mode.probability}
          </span>
          <span
            className={`badge ${
              mode.impact === 'low' ? 'badge-success' :
              mode.impact === 'medium' ? 'badge-warning' :
              'badge-error'
            }`}
          >
            {mode.impact}
          </span>
          {expanded ? (
            <ChevronUp className="w-4 h-4 text-muted" />
          ) : (
            <ChevronDown className="w-4 h-4 text-muted" />
          )}
        </div>
      </button>

      {expanded && (
        <div className="px-4 pb-4 pt-1 ml-7 animate-slide-down">
          <p className="text-[10px] font-medium tracking-widest uppercase mb-1 text-muted">
            Mitigation
          </p>
          <p className="text-sm text-secondary">
            {mode.mitigation}
          </p>
        </div>
      )}
    </div>
  )
}

function FailureSkeleton() {
  return (
    <div className="space-y-3 p-4">
      {[1, 2, 3].map((i) => (
        <div key={i} className="flex items-center gap-3">
          <Skeleton circle width={20} height={20} />
          <div className="flex-1">
            <Skeleton height={12} width="60%" />
            <Skeleton height={10} width="40%" className="mt-1" />
          </div>
          <Skeleton width={50} height={20} borderRadius={20} />
        </div>
      ))}
    </div>
  )
}

export default function FailureModesPanel({ session }: FailureModesPanelProps) {
  const failureModes = session?.failure_modes || []

  return (
    <div className="glass-panel !p-0 overflow-hidden">
      <div className="flex items-center justify-between px-5 py-4 border-b border-glass">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-orange-500/10 border border-orange-500/20">
            <ShieldAlert className="w-4 h-4 text-amber-400" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-primary">Failure Modes</h2>
            <p className="text-xs text-muted">
              {failureModes.length > 0 ? `${failureModes.length} identified` : 'Risk analysis'}
            </p>
          </div>
        </div>
        {failureModes.length > 0 && (
          <span className="badge badge-warning">{failureModes.length}</span>
        )}
      </div>

      {!session ? (
        <FailureSkeleton />
      ) : failureModes.length === 0 ? (
        <div className="text-center py-10 px-5">
          <div className="w-14 h-14 mx-auto mb-3 rounded-2xl flex items-center justify-center bg-surface-glass-light">
            <ShieldAlert className="w-7 h-7 text-muted" />
          </div>
          <p className="text-sm text-muted">
            No failure modes identified yet
          </p>
        </div>
      ) : (
        <div>
          {failureModes.map((mode, i) => (
            <FailureModeRow key={i} mode={mode} />
          ))}
        </div>
      )}
    </div>
  )
}
