import { Columns, CheckCircle, Circle, PlayCircle, XCircle, Clock } from 'lucide-react'
import clsx from 'clsx'
import type { SessionState, Phase } from '../lib/types'

interface PhaseBoardProps {
  session: SessionState | null
}

const STATUS_ICONS = {
  pending: Circle,
  in_progress: PlayCircle,
  completed: CheckCircle,
  failed: XCircle,
}

const STATUS_STYLES = {
  pending: 'border-slate-700 bg-slate-800/30',
  in_progress: 'border-violet-500 bg-violet-500/10',
  completed: 'border-green-500 bg-green-500/10',
  failed: 'border-red-500 bg-red-500/10',
}

const PHASE_COLORS = {
  discovery: 'from-blue-600 to-cyan-600',
  design: 'from-violet-600 to-purple-600',
  planning: 'from-amber-600 to-orange-600',
  implementation: 'from-green-600 to-emerald-600',
}

function PhaseCard({ phase }: { phase: Phase }) {
  const StatusIcon = STATUS_ICONS[phase.status]
  const phaseType = phase.name.toLowerCase().split(' ')[0]
  const colorClass = PHASE_COLORS[phaseType as keyof typeof PHASE_COLORS] || PHASE_COLORS.design

  return (
    <div className={clsx('rounded-lg border p-4', STATUS_STYLES[phase.status])}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className={clsx('p-1.5 rounded bg-gradient-to-br', colorClass)}>
            <StatusIcon className="w-4 h-4 text-white" />
          </div>
          <span className="font-medium text-slate-200">{phase.name}</span>
        </div>
        <span className="text-xs text-slate-500 uppercase">{phase.status.replace('_', ' ')}</span>
      </div>

      {phase.tasks.length > 0 && (
        <div className="space-y-2">
          <p className="text-xs text-slate-500 uppercase tracking-wider">
            Tasks ({phase.tasks.filter((t) => t.status === 'completed').length}/{phase.tasks.length})
          </p>
          <div className="space-y-1.5">
            {phase.tasks.slice(0, 5).map((task) => {
              const TaskIcon = STATUS_ICONS[task.status]
              return (
                <div key={task.id} className="flex items-center gap-2 text-sm">
                  <TaskIcon className={clsx(
                    'w-3.5 h-3.5',
                    task.status === 'completed' ? 'text-green-400' :
                    task.status === 'in_progress' ? 'text-violet-400' :
                    task.status === 'failed' ? 'text-red-400' : 'text-slate-500'
                  )} />
                  <span className={clsx(
                    task.status === 'completed' ? 'text-slate-400 line-through' : 'text-slate-300'
                  )}>
                    {task.title}
                  </span>
                </div>
              )
            })}
            {phase.tasks.length > 5 && (
              <p className="text-xs text-slate-500 pl-5">+{phase.tasks.length - 5} more tasks</p>
            )}
          </div>
        </div>
      )}

      {phase.started_at && (
        <div className="mt-3 pt-3 border-t border-slate-800 flex items-center gap-2 text-xs text-slate-500">
          <Clock className="w-3.5 h-3.5" />
          Started {new Date(phase.started_at).toLocaleTimeString()}
        </div>
      )}
    </div>
  )
}

export default function PhaseBoard({ session }: PhaseBoardProps) {
  if (!session) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center">
        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-slate-800 flex items-center justify-center">
          <Columns className="w-8 h-8 text-slate-600" />
        </div>
        <h3 className="text-lg font-medium text-slate-400 mb-2">No Phases Yet</h3>
        <p className="text-sm text-slate-500">Start a session to see the phase board</p>
      </div>
    )
  }

  const phases = session.phases || []
  const completedPhases = phases.filter((p) => p.status === 'completed').length
  const progress = phases.length > 0 ? (completedPhases / phases.length) * 100 : 0

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Columns className="w-5 h-5 text-violet-400" />
          <h2 className="text-lg font-semibold">Phase Board</h2>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="w-32 h-2 bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-violet-500 to-indigo-500 transition-all"
                style={{ width: `${progress}%` }}
              />
            </div>
            <span className="text-sm text-slate-500">{Math.round(progress)}%</span>
          </div>
        </div>
      </div>

      {phases.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-slate-500">No phases generated yet</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {phases.map((phase) => (
            <PhaseCard key={phase.id} phase={phase} />
          ))}
        </div>
      )}
    </div>
  )
}
