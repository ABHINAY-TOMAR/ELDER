import { ArrowRight, Cpu, Database, GitBranch, Layers, Shield, Zap } from 'lucide-react'
import { useState } from 'react'
import RequirementInput from './components/RequirementInput'
import ArchitectureViewer from './components/ArchitectureViewer'
import ADRPanel from './components/ADRPanel'
import FailureModesPanel from './components/FailureModesPanel'
import PhaseBoard from './components/PhaseBoard'
import DispatchPanel from './components/DispatchPanel'
import type { SessionState } from './lib/types'

export default function App() {
  const [session, setSession] = useState<SessionState | null>(null)
  const [activeTab, setActiveTab] = useState<'architecture' | 'phases' | 'dispatch'>('architecture')

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-violet-600 to-indigo-600 rounded-lg">
              <Cpu className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent">
                Architect Agent
              </h1>
              <p className="text-xs text-slate-500">ELDER System Design Engine</p>
            </div>
          </div>
          <nav className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab('architecture')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeTab === 'architecture'
                  ? 'bg-violet-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              Architecture
            </button>
            <button
              onClick={() => setActiveTab('phases')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeTab === 'phases'
                  ? 'bg-violet-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              Phases
            </button>
            <button
              onClick={() => setActiveTab('dispatch')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeTab === 'dispatch'
                  ? 'bg-violet-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              Dispatch
            </button>
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1 space-y-6">
            <RequirementInput onSessionUpdate={setSession} />
            <FailureModesPanel session={session} />
          </div>
          <div className="lg:col-span-2 space-y-6">
            {activeTab === 'architecture' && (
              <>
                <ArchitectureViewer session={session} />
                <ADRPanel session={session} />
              </>
            )}
            {activeTab === 'phases' && <PhaseBoard session={session} />}
            {activeTab === 'dispatch' && <DispatchPanel session={session} />}
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-800 mt-12 py-6">
        <div className="max-w-7xl mx-auto px-4 flex items-center justify-between text-sm text-slate-500">
          <div className="flex items-center gap-6">
            <span className="flex items-center gap-2">
              <Layers className="w-4 h-4" />
              ELDER v0.1.0
            </span>
            <span className="flex items-center gap-2">
              <Database className="w-4 h-4" />
              {session?.memory?.length ?? 0} memories
            </span>
          </div>
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1">
              <Zap className="w-4 h-4 text-amber-500" />
              {session?.tokens?.total ?? 0} tokens
            </span>
          </div>
        </div>
      </footer>
    </div>
  )
}
