import { ArrowRight, Cpu, Database, GitBranch, Layers, Shield, Zap, Sun, Moon, Menu, X } from 'lucide-react'
import { useState, useEffect } from 'react'
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
  const [isDarkMode, setIsDarkMode] = useState(true)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      setIsDarkMode(savedTheme === 'dark')
    } else if (window.matchMedia('(prefers-color-scheme: light)').matches) {
      setIsDarkMode(false)
    }
  }, [])

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.remove('light')
      document.body.classList.remove('light')
    } else {
      document.documentElement.classList.add('light')
      document.body.classList.add('light')
    }
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light')
  }, [isDarkMode])

  const tabs = [
    { id: 'architecture' as const, label: 'Architecture' },
    { id: 'phases' as const, label: 'Phases' },
    { id: 'dispatch' as const, label: 'Dispatch' },
  ]

  return (
    <div className="min-h-screen bg-slate-950 dark:bg-slate-950 light:bg-slate-50 text-slate-100 dark:text-slate-100 light:text-slate-900 transition-colors duration-300">
      <header className="border-b border-slate-800 dark:border-slate-800 light:border-slate-200 bg-slate-900/50 dark:bg-slate-900/50 light:bg-slate-50/80 backdrop-blur-sm sticky top-0 z-50 transition-colors duration-300">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3 animate-fade-in">
              <div className="p-2 bg-gradient-to-br from-violet-600 to-indigo-600 rounded-lg">
                <Cpu className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent dark:from-violet-400 dark:to-indigo-400 light:from-violet-600 light:to-indigo-600">
                  Architect Agent
                </h1>
                <p className="text-xs text-slate-500 dark:text-slate-500 light:text-slate-500">ELDER System Design Engine</p>
              </div>
            </div>

            <div className="hidden md:flex items-center gap-2">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                    activeTab === tab.id
                      ? 'bg-violet-600 text-white shadow-lg shadow-violet-600/25'
                      : 'text-slate-400 dark:text-slate-400 light:text-slate-600 hover:text-white dark:hover:text-white light:hover:text-slate-900 hover:bg-slate-800 dark:hover:bg-slate-800 light:hover:bg-slate-100'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
              <button
                onClick={() => setIsDarkMode(!isDarkMode)}
                className="ml-2 p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 dark:text-slate-400 dark:hover:text-white dark:hover:bg-slate-800 light:text-slate-600 light:hover:text-slate-900 light:hover:bg-slate-100 transition-all duration-200"
                aria-label="Toggle theme"
              >
                {isDarkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
            </div>

            <div className="flex md:hidden items-center gap-2">
              <button
                onClick={() => setIsDarkMode(!isDarkMode)}
                className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 dark:text-slate-400 dark:hover:text-white dark:hover:bg-slate-800 light:text-slate-600 light:hover:text-slate-900 light:hover:bg-slate-100 transition-all duration-200"
                aria-label="Toggle theme"
              >
                {isDarkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 dark:text-slate-400 dark:hover:text-white dark:hover:bg-slate-800 light:text-slate-600 light:hover:text-slate-900 light:hover:bg-slate-100 transition-all duration-200"
                aria-label="Toggle menu"
              >
                {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </button>
            </div>
          </div>

          <div className={`md:hidden mt-4 pb-2 ${isMobileMenuOpen ? 'block' : 'hidden'}`}>
            <div className="flex flex-col gap-2">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => {
                    setActiveTab(tab.id)
                    setIsMobileMenuOpen(false)
                  }}
                  className={`px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 text-left ${
                    activeTab === tab.id
                      ? 'bg-violet-600 text-white'
                      : 'text-slate-400 dark:text-slate-400 light:text-slate-600 hover:bg-slate-800 dark:hover:bg-slate-800 light:hover:bg-slate-100'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1 space-y-6">
            <div className="animate-slide-up stagger-1">
              <RequirementInput onSessionUpdate={setSession} />
            </div>
            <div className="animate-slide-up stagger-2">
              <FailureModesPanel session={session} />
            </div>
          </div>
          <div className="lg:col-span-2 space-y-6">
            {activeTab === 'architecture' && (
              <>
                <div className="animate-fade-in">
                  <ArchitectureViewer session={session} />
                </div>
                <div className="animate-fade-in stagger-1">
                  <ADRPanel session={session} />
                </div>
              </>
            )}
            {activeTab === 'phases' && (
              <div className="animate-fade-in">
                <PhaseBoard session={session} />
              </div>
            )}
            {activeTab === 'dispatch' && (
              <div className="animate-fade-in">
                <DispatchPanel session={session} />
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-800 dark:border-slate-800 light:border-slate-200 mt-12 py-6 transition-colors duration-300">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-slate-500 dark:text-slate-500 light:text-slate-500">
          <div className="flex items-center gap-6">
            <span className="flex items-center gap-2">
              <Layers className="w-4 h-4" />
              ELDER v1.0.0
            </span>
            <span className="hidden sm:flex items-center gap-2">
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
