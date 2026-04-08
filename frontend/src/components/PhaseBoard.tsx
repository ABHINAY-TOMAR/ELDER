import { Columns, CheckCircle, Circle, PlayCircle, XCircle, Clock, Layers, Loader2 } from 'lucide-react'
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'
import { useState } from 'react'
import type { SessionState, Phase, Task } from '../lib/types'
import { stepSession } from '../lib/api'

interface PhaseBoardProps {
  session: SessionState | null
  onSessionUpdate: (session: SessionState) => void
}

const STATUS_ICONS = {
  pending: Circle,
  in_progress: PlayCircle,
  completed: CheckCircle,
  failed: XCircle,
}

const PHASE_GRADIENTS: Record<string, string> = {
  discovery: 'from-blue-500/20 to-cyan-500/20',
  design: 'from-violet-500/20 to-purple-500/20',
  planning: 'from-amber-500/20 to-orange-500/20',
  foundation: 'from-indigo-500/20 to-blue-500/20',
  implementation: 'from-green-500/20 to-emerald-500/20',
}

function TaskItem({ 
  task, 
  sessionId, 
  onUpdate 
}: { 
  task: Task; 
  sessionId: string; 
  onUpdate: (s: SessionState) => void 
}) {
  const [isUpdating, setIsUpdating] = useState(false)
  const TaskIcon = STATUS_ICONS[task.status]

  const handleToggle = async () => {
    try {
      setIsUpdating(true)
      const updated = await stepSession(sessionId, `toggle_task:${task.id}`)
      onUpdate(updated)
    } finally {
      setIsUpdating(false)
    }
  }

  return (
    <button
      onClick={handleToggle}
      disabled={isUpdating}
      className={`group w-full flex items-center gap-2.5 px-2.5 py-1.5 rounded-lg transition-all text-left ${
        task.status === 'completed' 
          ? 'bg-surface-glass-light opacity-60' 
          : 'hover:bg-surface-glass-light hover:translate-x-0.5'
      }`}
    >
      {isUpdating ? (
        <Loader2 className="w-3.5 h-3.5 animate-spin text-muted" />
      ) : (
        <TaskIcon className={`w-3.5 h-3.5 flex-shrink-0 transition-transform group-hover:scale-110 ${
          task.status === 'completed' ? 'text-green-400' :
          task.status === 'in_progress' ? 'text-violet-400' :
          task.status === 'failed' ? 'text-red-400' : 'text-muted'
        }`} />
      )}
      <span
        className={`text-xs ${
          task.status === 'completed' ? 'line-through text-muted' : 'text-secondary font-medium'
        }`}
      >
        {task.title}
      </span>
    </button>
  )
}

function PhaseCard({ 
  phase, 
  index, 
  sessionId, 
  onUpdate 
}: { 
  phase: Phase; 
  index: number; 
  sessionId: string;
  onUpdate: (s: SessionState) => void 
}) {
  const StatusIcon = STATUS_ICONS[phase.status]
  const phaseType = phase.name.toLowerCase().split(' ')[0]
  const gradient = PHASE_GRADIENTS[phaseType] || PHASE_GRADIENTS.design

  return (
    <div
      className={`glass-card p-5 animate-slide-up stagger-${Math.min(index + 1, 5)} ${
        phase.status === 'in_progress' ? 'border-primary/50 shadow-lg shadow-primary/5 bg-primary/5' : ''
      }`}
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2.5">
          <div className={`p-2 rounded-xl bg-gradient-to-br ${gradient} border border-white/5 shadow-inner`}>
            <StatusIcon className="w-4 h-4 text-white" />
          </div>
          <span className="font-semibold text-sm text-primary">
            {phase.name}
          </span>
        </div>
        <span className={`text-[10px] font-medium tracking-widest uppercase ${
          phase.status === 'completed' ? 'text-green-400' :
          phase.status === 'in_progress' ? 'text-violet-400' :
          phase.status === 'failed' ? 'text-red-400' : 'text-muted'
        }`}>
          {phase.status.replace('_', ' ')}
        </span>
      </div>

      {phase.tasks.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between px-1">
            <p className="text-[10px] font-medium tracking-widest uppercase text-muted">
              Tasks
            </p>
            <p className="text-[10px] font-mono text-muted">
              {phase.tasks.filter((t) => t.status === 'completed').length}/{phase.tasks.length}
            </p>
          </div>
          <div className="space-y-1">
            {phase.tasks.map((task) => (
              <TaskItem 
                key={task.id} 
                task={task} 
                sessionId={sessionId}
                onUpdate={onUpdate}
              />
            ))}
          </div>
        </div>
      )}

      {phase.started_at && (
        <div className="mt-5 pt-3 flex items-center gap-2 text-[10px] border-t border-glass text-muted italic">
          <Clock className="w-3 h-3" />
          Modified {new Date(phase.started_at).toLocaleTimeString()}
        </div>
      )}
    </div>
  )
}

function PhaseSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {[1, 2, 3].map((i) => (
        <div key={i} className="glass-card p-5">
          <div className="flex items-center gap-2.5 mb-4">
            <Skeleton circle width={36} height={36} />
            <Skeleton width={120} height={16} />
          </div>
          <Skeleton height={10} width={80} className="mb-2" />
          <Skeleton count={3} height={12} />
        </div>
      ))}
    </div>
  )
}

export default function PhaseBoard({ session, onSessionUpdate }: PhaseBoardProps) {
  const phases = session?.phases || []
  const completedPhases = phases.filter((p) => p.status === 'completed').length
  const progress = phases.length > 0 ? (completedPhases / phases.length) * 100 : 0

  return (
    <div className="glass-panel">
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-br from-violet-500/20 to-indigo-500/20 border border-violet-500/20 shadow-lg">
            <Layers className="w-5 h-5 text-violet-400" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-primary">
              Project Lifecycle
            </h2>
            <p className="text-xs text-muted">
              {phases.length > 0 ? 'Interactive task management' : 'No phases generated'}
            </p>
          </div>
        </div>
        {phases.length > 0 && (
          <div className="flex items-center gap-4">
            <div className="hidden sm:flex flex-col items-end gap-1">
              <span className="text-[10px] font-medium text-muted uppercase tracking-widest">Global Progress</span>
              <div className="w-32 h-1.5 rounded-full overflow-hidden bg-surface-glass-strong">
                <div
                  className="h-full rounded-full transition-all duration-700 ease-out bg-gradient-to-r from-violet-500 to-indigo-500 shadow-[0_0_10px_rgba(139,92,246,0.3)]"
                  style={{ width: `${progress}%` } as React.CSSProperties}
                />
              </div>
            </div>
            <div className="flex flex-col items-center justify-center p-2 rounded-xl bg-surface-glass border border-glass min-w-[50px]">
               <span className="text-sm font-bold text-primary">{Math.round(progress)}%</span>
            </div>
          </div>
        )}
      </div>

      {!session ? (
        <PhaseSkeleton />
      ) : phases.length === 0 ? (
        <div className="text-center py-14">
          <div className="w-16 h-16 mx-auto mb-4 rounded-2xl flex items-center justify-center bg-surface-glass-light">
            <Columns className="w-8 h-8 text-muted" />
          </div>
          <h3 className="text-base font-medium mb-1.5 text-secondary">
            Project Plan Needed
          </h3>
          <p className="text-sm text-muted">
            Generation will produce a phased execution board here
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {phases.map((phase, i) => (
            <PhaseCard 
              key={phase.id} 
              phase={phase} 
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
