import { AlertTriangle, ChevronDown, ChevronUp } from 'lucide-react'
import { useState } from 'react'
import clsx from 'clsx'
import type { SessionState, FailureMode } from '../lib/types'

interface FailureModesPanelProps {
  session: SessionState | null
}

const PROBABILITY_STYLES = {
  low: 'text-green-400 bg-green-400/10',
  medium: 'text-amber-400 bg-amber-400/10',
  high: 'text-red-400 bg-red-400/10',
}

const IMPACT_STYLES = {
  low: 'text-green-400 bg-green-400/10',
  medium: 'text-amber-400 bg-amber-400/10',
  high: 'text-red-400 bg-red-400/10',
}

function FailureModeRow({ mode }: { mode: FailureMode }) {
  const [expanded, setExpanded] = useState(false)
  const riskScore = { low: 1, medium: 2, high: 3 }[mode.probability] * { low: 1, medium: 2, high: 3 }[mode.impact]

  return (
    <div className="border-b border-slate-800 last:border-b-0">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between p-4 hover:bg-slate-800/50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <AlertTriangle className={clsx(
            'w-4 h-4',
            riskScore >= 6 ? 'text-red-400' : riskScore >= 3 ? 'text-amber-400' : 'text-green-400'
          )} />
          <div className="text-left">
            <p className="text-sm font-medium text-slate-200">{mode.component}</p>
            <p className="text-xs text-slate-500">{mode.failure_type}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className={clsx('px-2 py-0.5 text-xs rounded', PROBABILITY_STYLES[mode.probability])}>
            {mode.probability}
          </span>
          <span className={clsx('px-2 py-0.5 text-xs rounded', IMPACT_STYLES[mode.impact])}>
            {mode.impact}
          </span>
          {expanded ? <ChevronUp className="w-4 h-4 text-slate-500" /> : <ChevronDown className="w-4 h-4 text-slate-500" />}
        </div>
      </button>

      {expanded && (
        <div className="px-4 pb-4 pt-2 ml-7">
          <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">Mitigation</p>
          <p className="text-sm text-slate-400">{mode.mitigation}</p>
        </div>
      )}
    </div>
  )
}

export default function FailureModesPanel({ session }: FailureModesPanelProps) {
  if (!session) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4">
          <AlertTriangle className="w-5 h-5 text-amber-400" />
          <h2 className="text-lg font-semibold">Failure Modes</h2>
        </div>
        <p className="text-sm text-slate-500 text-center py-8">
          No failure modes identified yet
        </p>
      </div>
    )
  }

  const failureModes = session.failure_modes || []

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-400" />
          <h2 className="text-lg font-semibold">Failure Modes</h2>
        </div>
        <span className="text-sm text-slate-500">{failureModes.length} identified</span>
      </div>

      {failureModes.length === 0 ? (
        <p className="text-sm text-slate-500 text-center py-8">
          No failure modes identified yet
        </p>
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
