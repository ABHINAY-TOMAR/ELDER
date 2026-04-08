import { Cpu, Database, Layers, Zap, Sun, Moon, Menu, X } from 'lucide-react'
import { useState, useEffect } from 'react'
import { Toaster } from 'sonner'
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
    { id: 'architecture' as const, label: 'Architecture', icon: '◆' },
    { id: 'phases' as const, label: 'Phases', icon: '◇' },
    { id: 'dispatch' as const, label: 'Dispatch', icon: '▸' },
  ]

  return (
    <div className="min-h-screen transition-colors duration-300">
      <Toaster
        theme={isDarkMode ? 'dark' : 'light'}
        position="top-right"
        toastOptions={{
          style: {
            background: 'var(--surface-glass-strong)',
            border: '1px solid var(--border-glass)',
            backdropFilter: 'blur(20px)',
            fontFamily: "'Space Grotesk', sans-serif",
          },
        }}
      />

      {/* ─── Header ─── */}
      <header className="glass-header sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-3 animate-fade-in">
              <div className="relative p-2.5 rounded-xl bg-gradient-to-br from-violet-600 to-indigo-600 shadow-lg shadow-violet-600/20">
                <Cpu className="w-5 h-5 text-white" />
                <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-violet-600 to-indigo-600 animate-glow opacity-50 blur-sm -z-10" />
              </div>
              <div>
                <h1 className="text-lg font-bold tracking-tight text-primary">
                  <span className="bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent">
                    ELDER
                  </span>
                  <span className="text-xs font-normal ml-2 text-muted">
                    Architect Agent
                  </span>
                </h1>
                <p className="text-[10px] tracking-widest uppercase text-muted">
                  System Design Engine
                </p>
              </div>
            </div>

            {/* Desktop Tabs */}
            <div className="hidden md:flex items-center gap-1.5">
              <div className="flex items-center gap-1 p-1 rounded-xl glass">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                      activeTab === tab.id
                        ? 'tab-active text-white'
                        : 'text-secondary'
                    }`}
                  >
                    <span className="mr-1.5 text-xs opacity-60">{tab.icon}</span>
                    {tab.label}
                  </button>
                ))}
              </div>

              <div className="w-px h-6 mx-2 border-r border-glass" />

              <button
                onClick={() => setIsDarkMode(!isDarkMode)}
                className="p-2.5 rounded-xl glass transition-all hover:scale-105 text-secondary"
                aria-label="Toggle theme"
              >
                {isDarkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
              </button>
            </div>

            {/* Mobile Controls */}
            <div className="flex md:hidden items-center gap-2">
              <button
                onClick={() => setIsDarkMode(!isDarkMode)}
                className="p-2 rounded-lg glass text-secondary"
                aria-label="Toggle theme"
              >
                {isDarkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
              </button>
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="p-2 rounded-lg glass text-secondary"
                aria-label="Toggle menu"
              >
                {isMobileMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* Mobile Menu */}
          <div className={`md:hidden mt-3 pb-2 ${isMobileMenuOpen ? 'animate-slide-down' : 'hidden'}`}>
            <div className="flex flex-col gap-1.5 p-2 glass rounded-xl">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => {
                    setActiveTab(tab.id)
                    setIsMobileMenuOpen(false)
                  }}
                  className={`px-4 py-3 rounded-lg text-sm font-medium transition-all text-left ${
                    activeTab === tab.id ? 'tab-active text-white' : 'text-secondary'
                  }`}
                >
                  <span className="mr-2 opacity-60">{tab.icon}</span>
                  {tab.label}
                </button>
              ))}
            </div>
          </div>
        </div>
        <div className="glow-line" />
      </header>

      {/* ─── Main Content ─── */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column */}
          <div className="lg:col-span-1 space-y-6">
            <div className="animate-slide-up stagger-1">
              <RequirementInput onSessionUpdate={setSession} />
            </div>
            <div className="animate-slide-up stagger-2">
              <FailureModesPanel session={session} />
            </div>
          </div>

          {/* Right (Main) Column */}
          <div className="lg:col-span-2 space-y-6">
            {activeTab === 'architecture' && (
              <>
                <div className="animate-scale-in">
                  <ArchitectureViewer session={session} />
                </div>
                <div className="animate-scale-in stagger-1">
                  <ADRPanel session={session} onSessionUpdate={setSession} />
                </div>
              </>
            )}
            {activeTab === 'phases' && (
              <div className="animate-scale-in">
                <PhaseBoard session={session} onSessionUpdate={setSession} />
              </div>
            )}
            {activeTab === 'dispatch' && (
              <div className="animate-scale-in">
                <DispatchPanel session={session} onSessionUpdate={setSession} />
              </div>
            )}
          </div>
        </div>
      </main>

      {/* ─── Footer ─── */}
      <footer className="mt-12 py-6 border-t border-glass">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-muted">
          <div className="flex items-center gap-6">
            <span className="flex items-center gap-2">
              <Layers className="w-3.5 h-3.5" />
              ELDER v1.0.0
            </span>
            <span className="hidden sm:flex items-center gap-2">
              <Database className="w-3.5 h-3.5" />
              {session?.memory?.length ?? 0} memories
            </span>
          </div>
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5">
              <Zap className="w-3.5 h-3.5 text-amber-500" />
              {session?.tokens?.total ?? 0} tokens
            </span>
          </div>
        </div>
      </footer>
    </div>
  )
}
