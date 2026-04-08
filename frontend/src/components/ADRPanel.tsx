import { FileText, CheckCircle, XCircle, Clock, BookOpen, UserCheck, Loader2 } from 'lucide-react'
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'
import { useState } from 'react'
import type { SessionState, ADR } from '../lib/types'
import { stepSession } from '../lib/api'

interface ADRPanelProps {
  session: SessionState | null
  onSessionUpdate: (session: SessionState) => void
}

const STATUS_CONFIG = {
  proposed: { Icon: Clock, color: '#fbbf24', bg: 'rgba(245, 158, 11, 0.08)', border: 'rgba(245, 158, 11, 0.2)' },
  accepted: { Icon: CheckCircle, color: '#4ade80', bg: 'rgba(34, 197, 94, 0.08)', border: 'rgba(34, 197, 94, 0.2)' },
  deprecated: { Icon: XCircle, color: '#94a3b8', bg: 'rgba(148, 163, 184, 0.08)', border: 'rgba(148, 163, 184, 0.2)' },
}

function ADRCard({ 
  adr, 
  index, 
  sessionId, 
  onUpdate 
}: { 
  adr: ADR; 
  index: number; 
  sessionId: string; 
  onUpdate: (s: SessionState) => void 
}) {
  const [isApproving, setIsApproving] = useState(false)
  const config = STATUS_CONFIG[adr.status]
  const StatusIcon = config.Icon

  const handleApprove = async () => {
    try {
      setIsApproving(true)
      const updated = await stepSession(sessionId, `approve_adr:${adr.id}`)
      onUpdate(updated)
    } finally {
      setIsApproving(false)
    }
  }

  return (
    <div
      className={`glass-card p-5 animate-slide-up stagger-${Math.min(index + 1, 5)} ${
        adr.status === 'proposed' ? 'border-amber-500/30 bg-amber-500/5' : ''
      }`}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2.5">
          <div
            className="p-1.5 rounded-lg bg-indigo-500/10"
          >
            <BookOpen className="w-3.5 h-3.5 text-violet-400" />
          </div>
          <span className="font-semibold text-sm text-primary">
            {adr.title}
          </span>
        </div>
        <span
          className={`badge ${
            adr.status === 'proposed' ? 'badge-warning' :
            adr.status === 'accepted' ? 'badge-success' :
            'badge-info'
          }`}
        >
          <StatusIcon className="w-3 h-3" />
          {adr.status}
        </span>
      </div>

      <p className="text-sm mb-4 text-secondary">
        {adr.decision}
      </p>

      <div className="space-y-3">
        <div>
          <p className="text-[10px] font-medium tracking-widest uppercase mb-1 text-muted">
            Rationale
          </p>
          <p className="text-sm text-secondary">
            {adr.rationale}
          </p>
        </div>

        {adr.consequences.length > 0 && (
          <div>
            <p className="text-[10px] font-medium tracking-widest uppercase mb-1.5 text-muted">
              Consequences ({adr.consequences.length})
            </p>
            <ul className="space-y-1">
              {adr.consequences.map((consequence, i) => (
                <li
                  key={i}
                  className="text-sm flex items-start gap-2 text-secondary"
                >
                  <span className="mt-0.5 text-violet-500 opacity-60">•</span>
                  {consequence}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {adr.status === 'proposed' && (
        <div className="mt-5 pt-4 border-t border-amber-500/10 flex items-center justify-between">
          <div className="flex items-center gap-2 text-[10px] text-amber-500 font-medium uppercase tracking-wider">
             <Clock className="w-3 h-3" />
             Review Pending
          </div>
          <button
            onClick={handleApprove}
            disabled={isApproving}
            className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-500 text-xs font-semibold hover:bg-amber-500/20 active:scale-95 transition-all disabled:opacity-50"
          >
            {isApproving ? (
              <Loader2 className="w-3 h-3 animate-spin" />
            ) : (
              <UserCheck className="w-3 h-3" />
            )}
            Approve Decision
          </button>
        </div>
      )}
    </div>
  )
}

function ADRSkeleton() {
  return (
    <div className="space-y-4">
      {[1, 2].map((i) => (
        <div key={i} className="glass-card p-5">
          <div className="flex items-center justify-between mb-3">
            <Skeleton width={180} height={16} />
            <Skeleton width={70} height={22} borderRadius={20} />
          </div>
          <Skeleton count={2} height={12} />
          <div className="mt-3">
            <Skeleton width={80} height={10} />
            <Skeleton height={12} width="90%" className="mt-1" />
          </div>
        </div>
      ))}
    </div>
  )
}

export default function ADRPanel({ session, onSessionUpdate }: ADRPanelProps) {
  const adrs = session?.adrs || []
  const proposedCount = adrs.filter(a => a.status === 'proposed').length

  return (
    <div className="glass-panel">
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-gradient-to-br from-violet-500/20 to-indigo-500/20 border border-violet-500/20">
            <FileText className="w-4 h-4 text-violet-400" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-primary">
              Architecture Decisions
            </h2>
            <p className="text-xs text-muted">
              {adrs.length > 0 ? `${adrs.length} ADRs recorded` : 'Decisions will appear here'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          {proposedCount > 0 && (
            <span className="badge badge-warning animate-pulse-subtle">
              {proposedCount} Pending Review
            </span>
          )}
          {adrs.length > 0 && (
            <span className="badge badge-info">{adrs.length} Total</span>
          )}
        </div>
      </div>

      {!session ? (
        <ADRSkeleton />
      ) : adrs.length === 0 ? (
        <div className="text-center py-10">
          <div className="w-14 h-14 mx-auto mb-3 rounded-2xl flex items-center justify-center bg-surface-glass-light">
            <FileText className="w-7 h-7 text-muted" />
          </div>
          <p className="text-sm text-muted">
            No architecture decisions recorded yet
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {adrs.map((adr, i) => (
            <ADRCard 
              key={adr.id} 
              adr={adr} 
              index={i} 
              sessionId={session.id}
              onUpdate={onSessionUpdate}
            />
          ))}
        </div>
      )}
    </div>
  )
}
