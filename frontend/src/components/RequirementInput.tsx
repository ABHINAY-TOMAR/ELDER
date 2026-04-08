import { Send, Sparkles } from 'lucide-react'
import { useState } from 'react'
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

    try {
      const session = await startSession(requirement)
      onSessionUpdate(session)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start session')
    } finally {
      setLoading(false)
    }
  }

  const useExample = (example: string) => {
    setRequirement(example)
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-5 h-5 text-violet-400" />
        <h2 className="text-lg font-semibold">System Requirements</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <textarea
            value={requirement}
            onChange={(e) => setRequirement(e.target.value)}
            placeholder="Describe your system requirements in natural language..."
            className="w-full h-32 px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent resize-none"
            disabled={loading}
          />
        </div>

        {error && (
          <div className="p-3 bg-red-900/30 border border-red-800 rounded-lg text-red-400 text-sm">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !requirement.trim()}
          className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-all"
        >
          {loading ? (
            <>
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Generating Architecture...
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              Generate Architecture
            </>
          )}
        </button>
      </form>

      <div className="mt-4 pt-4 border-t border-slate-800">
        <p className="text-xs text-slate-500 mb-2">Try an example:</p>
        <div className="flex flex-wrap gap-2">
          {EXAMPLE_REQUIREMENTS.map((example, i) => (
            <button
              key={i}
              onClick={() => useExample(example)}
              className="px-3 py-1.5 text-xs bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-300 rounded-full transition-colors"
            >
              {example.split(' ').slice(0, 5).join(' ')}...
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
