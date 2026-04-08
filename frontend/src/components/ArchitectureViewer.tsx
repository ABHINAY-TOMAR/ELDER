import { useEffect, useRef, useState } from 'react'
import { Maximize2, Minimize2, Copy, Check, ZoomIn, ZoomOut, Download } from 'lucide-react'
import mermaid from 'mermaid'
import type { SessionState } from '../lib/types'

const darkThemeConfig = {
  startOnLoad: false,
  theme: 'dark',
  themeVariables: {
    primaryColor: '#6366f1',
    primaryTextColor: '#e2e8f0',
    primaryBorderColor: '#4f46e5',
    lineColor: '#64748b',
    secondaryColor: '#1e1b4b',
    tertiaryColor: '#312e81',
    background: '#0f172a',
    mainBkg: '#1e293b',
    nodeBorder: '#4f46e5',
    clusterBkg: '#1e293b',
    clusterBorder: '#334155',
    titleColor: '#e2e8f0',
    edgeLabelBackground: '#1e293b',
  },
}

const lightThemeConfig = {
  startOnLoad: false,
  theme: 'base' as const,
  themeVariables: {
    primaryColor: '#6366f1',
    primaryTextColor: '#1e293b',
    primaryBorderColor: '#4f46e5',
    lineColor: '#64748b',
    secondaryColor: '#e0e7ff',
    tertiaryColor: '#c7d2fe',
    background: '#f8fafc',
    mainBkg: '#f1f5f9',
    nodeBorder: '#4f46e5',
    clusterBkg: '#f1f5f9',
    clusterBorder: '#e2e8f0',
    titleColor: '#1e293b',
    edgeLabelBackground: '#f1f5f9',
  },
}

mermaid.initialize(darkThemeConfig)

interface ArchitectureViewerProps {
  session: SessionState | null
}

export default function ArchitectureViewer({ session }: ArchitectureViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [fullscreen, setFullscreen] = useState(false)
  const [copied, setCopied] = useState(false)
  const [scale, setScale] = useState(1)
  const [error, setError] = useState<string | null>(null)
  const [isDark, setIsDark] = useState(true)

  useEffect(() => {
    const isDarkMode = !document.documentElement.classList.contains('light')
    setIsDark(isDarkMode)
    mermaid.initialize(isDarkMode ? darkThemeConfig : lightThemeConfig)
  }, [])

  useEffect(() => {
    if (!containerRef.current || !session?.mermaid_diagram) return

    const renderDiagram = async () => {
      try {
        setError(null)
        const id = `mermaid-${Date.now()}`
        const { svg } = await mermaid.render(id, session.mermaid_diagram)
        if (containerRef.current) {
          containerRef.current.innerHTML = svg
          containerRef.current.classList.add('animate-fade-in')
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to render diagram')
      }
    }

    renderDiagram()
  }, [session?.mermaid_diagram, isDark])

  useEffect(() => {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.attributeName === 'class') {
          const isDarkMode = !document.documentElement.classList.contains('light')
          setIsDark(isDarkMode)
          mermaid.initialize(isDarkMode ? darkThemeConfig : lightThemeConfig)
        }
      })
    })
    observer.observe(document.documentElement, { attributes: true })
    return () => observer.disconnect()
  }, [])

  const copyMermaid = () => {
    if (session?.mermaid_diagram) {
      navigator.clipboard.writeText(session.mermaid_diagram)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      containerRef.current?.parentElement?.requestFullscreen()
      setFullscreen(true)
    } else {
      document.exitFullscreen()
      setFullscreen(false)
    }
  }

  const downloadDiagram = () => {
    if (!containerRef.current) return
    const svg = containerRef.current.querySelector('svg')
    if (!svg) return
    const svgData = new XMLSerializer().serializeToString(svg)
    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')
    const img = new Image()
    img.onload = () => {
      canvas.width = img.width * 2
      canvas.height = img.height * 2
      ctx?.scale(2, 2)
      ctx?.drawImage(img, 0, 0)
      const pngFile = canvas.toDataURL('image/png')
      const downloadLink = document.createElement('a')
      downloadLink.download = 'architecture-diagram.png'
      downloadLink.href = pngFile
      downloadLink.click()
    }
    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)))
  }

  if (!session) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center">
        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-slate-800 flex items-center justify-center">
          <svg className="w-8 h-8 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-slate-400 mb-2">No Architecture Yet</h3>
        <p className="text-sm text-slate-500">Enter your requirements to generate an architecture diagram</p>
      </div>
    )
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800">
        <h3 className="text-sm font-medium text-slate-300">Architecture Diagram</h3>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setScale((s) => Math.max(0.5, s - 0.1))}
            className="p-1.5 hover:bg-slate-800 text-slate-400 hover:text-slate-300 rounded transition-colors"
            title="Zoom out"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <span className="text-xs text-slate-500 w-12 text-center">{Math.round(scale * 100)}%</span>
          <button
            onClick={() => setScale((s) => Math.min(2, s + 0.1))}
            className="p-1.5 hover:bg-slate-800 text-slate-400 hover:text-slate-300 rounded transition-colors"
            title="Zoom in"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <div className="w-px h-4 bg-slate-700 mx-1" />
          <button
            onClick={copyMermaid}
            className="p-1.5 hover:bg-slate-800 text-slate-400 hover:text-slate-300 rounded transition-colors"
            title="Copy Mermaid code"
          >
            {copied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
          </button>
          <button
            onClick={toggleFullscreen}
            className="p-1.5 hover:bg-slate-800 text-slate-400 hover:text-slate-300 rounded transition-colors"
            title="Toggle fullscreen"
          >
            {fullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
          <button
            onClick={downloadDiagram}
            className="p-1.5 hover:bg-slate-800 text-slate-400 hover:text-slate-300 rounded transition-colors"
            title="Download PNG"
          >
            <Download className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="p-6 overflow-auto" style={{ maxHeight: fullscreen ? 'calc(100vh - 100px)' : '500px' }}>
        {error ? (
          <div className="text-center text-red-400">
            <p>Failed to render diagram</p>
            <p className="text-sm text-slate-500 mt-1">{error}</p>
          </div>
        ) : (
          <div
            ref={containerRef}
            className="flex justify-center transition-transform origin-center"
            style={{ transform: `scale(${scale})` }}
          />
        )}
      </div>

      {session.components && session.components.length > 0 && (
        <div className="px-4 py-3 border-t border-slate-800 bg-slate-900/50">
          <p className="text-xs text-slate-500">
            {session.components.length} components identified
          </p>
        </div>
      )}
    </div>
  )
}
