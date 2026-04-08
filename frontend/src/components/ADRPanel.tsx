import { FileText, CheckCircle, XCircle, Clock } from 'lucide-react'
import clsx from 'clsx'
import type { SessionState, ADR } from '../lib/types'

interface ADRPanelProps {
  session: SessionState | null
}

const STATUS_ICONS = {
  proposed: Clock,
  accepted: CheckCircle,
  deprecated: XCircle,
}

const STATUS_STYLES = {
  proposed: 'text-amber-400 bg-amber-400/10 border-amber-400/20',
  accepted: 'text-green-400 bg-green-400/10 border-green-400/20',
  deprecated: 'text-slate-400 bg-slate-400/10 border-slate-400/20',
}

function ADRCard({ adr }: { adr: ADR }) {
  const StatusIcon = STATUS_ICONS[adr.status]

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-4">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4 text-violet-400" />
          <span className="font-medium text-slate-200">{adr.title}</span>
        </div>
        <span
          className={clsx(
            'flex items-center gap-1 px-2 py-0.5 text-xs rounded-full border',
            STATUS_STYLES[adr.status]
          )}
        >
          <StatusIcon className="w-3 h-3" />
          {adr.status}
        </span>
      </div>

      <p className="text-sm text-slate-400 mb-3">{adr.decision}</p>

      <div className="space-y-2">
        <div>
          <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">Rationale</p>
          <p className="text-sm text-slate-300">{adr.rationale}</p>
        </div>

        {adr.consequences.length > 0 && (
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">
              Consequences ({adr.consequences.length})
            </p>
            <ul className="space-y-1">
              {adr.consequences.map((consequence, i) => (
                <li key={i} className="text-sm text-slate-400 flex items-start gap-2">
                  <span className="text-slate-600 mt-1">•</span>
                  {consequence}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default function ADRPanel({ session }: ADRPanelProps) {
  if (!session) {
    return null
  }

  const adrs = session.adrs || []

  if (adrs.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4">
          <FileText className="w-5 h-5 text-violet-400" />
          <h2 className="text-lg font-semibold">Architecture Decisions</h2>
        </div>
        <p className="text-sm text-slate-500 text-center py-8">
          No architecture decisions recorded yet
        </p>
      </div>
    )
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <FileText className="w-5 h-5 text-violet-400" />
          <h2 className="text-lg font-semibold">Architecture Decisions</h2>
        </div>
        <span className="text-sm text-slate-500">{adrs.length} ADRs</span>
      </div>

      <div className="space-y-4">
        {adrs.map((adr) => (
          <ADRCard key={adr.id} adr={adr} />
        ))}
      </div>
    </div>
  )
}
