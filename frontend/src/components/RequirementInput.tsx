import { Send, Sparkles, Wand2 } from 'lucide-react'
import { useState } from 'react'
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'
import { toast } from 'sonner'
import { startSession } from '../lib/api'
import type { SessionState } from '../lib/types'

interface RequirementInputProps {
  onSessionUpdate: (session: SessionState) => void
}

const EXAMPLE_REQUIREMENTS = [
  'Build a real-time chat application supporting 10,000 concurrent users',
  'Design an e-commerce platform with inventory management and payment processing',
  'Create a microservices architecture for a video streaming service',
]

export default function RequirementInput({ onSessionUpdate }: RequirementInputProps) {
  const [requirement, setRequirement] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!requirement.trim()) return

    setLoading(true)
    setError(null)
    toast.info('Analyzing system requirements...', {
      description: 'The AI architect is processing your input.',
      icon: <Wand2 className="w-4 h-4" />,
    })

    try {
      const session = await startSession(requirement)
      onSessionUpdate(session)
      toast.success('Architecture generated!', {
        description: 'Your system design is ready for review.',
      })
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to start session'
      setError(msg)
      toast.error('Generation failed', { description: msg })
    } finally {
      setLoading(false)
    }
  }

  const useExample = (example: string) => {
    setRequirement(example)
    toast.info('Example loaded', { description: 'Hit "Generate" to begin.' })
  }

  return (
    <div className="glass-panel">
      {/* Header */}
      <div className="flex items-center gap-2.5 mb-5">
        <div className="p-2 rounded-lg bg-gradient-to-br from-violet-500/20 to-indigo-500/20 border border-violet-500/20">
          <Sparkles className="w-4 h-4 text-violet-400" />
        </div>
        <div>
          <h2 className="text-base font-semibold text-primary">
            System Requirements
          </h2>
          <p className="text-xs text-muted">
            Describe what you want to build
          </p>
        </div>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <textarea
            value={requirement}
            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setRequirement(e.target.value)}
            placeholder="Describe your system requirements in natural language..."
            className="input-glass h-32 resize-none scrollbar-thin"
            disabled={loading}
          />
        </div>

        {error && (
          <div className="p-3 rounded-xl text-sm animate-slide-up bg-red-500/10 border border-red-500/20 text-red-400">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !requirement.trim()}
          className="btn-primary w-full flex items-center justify-center gap-2.5 py-3"
        >
          {loading ? (
            <>
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Generating Architecture...
            </>
          ) : (
            <>
              <Send className="w-4 h-4" />
              Generate Architecture
            </>
          )}
        </button>
      </form>

      {/* Skeleton state while loading */}
      {loading && (
        <div className="mt-5 space-y-3 animate-fade-in">
          <Skeleton height={12} width="80%" />
          <Skeleton height={12} width="60%" />
          <Skeleton height={12} width="90%" />
          <Skeleton height={40} borderRadius={12} />
        </div>
      )}

      {/* Examples */}
      <div className="mt-5 pt-5 border-t border-glass">
        <p className="text-[11px] font-medium tracking-widest uppercase mb-3 text-muted">
          Try an example
        </p>
        <div className="flex flex-col gap-2">
          {EXAMPLE_REQUIREMENTS.map((example, i) => (
            <button
              key={i}
              onClick={() => useExample(example)}
              className="text-left px-3.5 py-2.5 rounded-xl glass text-xs text-secondary transition-all hover:scale-[1.01] active:scale-[0.99]"
            >
              <span className="opacity-50 mr-2">→</span>
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
