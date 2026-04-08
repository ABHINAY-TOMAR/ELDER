import { useEffect, useRef, useState, useCallback } from 'react'
import { Maximize2, Minimize2, Copy, Check, ZoomIn, ZoomOut, Download, Share2, Eye, GitBranch, Layers, AlertTriangle, Info, Network, FileText, Presentation } from 'lucide-react'
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'
import { toast } from 'sonner'
import mermaid from 'mermaid'
import { exportDocs, exportSlides } from '../lib/api'
import type { SessionState, Component } from '../lib/types'

type ViewMode = 'service' | 'dataflow' | 'technology' | 'severity'
type ColorMode = 'technology' | 'severity' | 'domain'

const darkThemeConfig = {
  startOnLoad: false,
  theme: 'dark' as const,
  themeVariables: {
    primaryColor: '#6366f1',
    primaryTextColor: '#e2e8f0',
    primaryBorderColor: '#4f46e5',
    lineColor: '#475569',
    secondaryColor: '#1e1b4b',
    tertiaryColor: '#312e81',
    background: 'transparent',
    mainBkg: 'rgba(30, 41, 59, 0.6)',
    nodeBorder: '#4f46e5',
    clusterBkg: 'rgba(30, 41, 59, 0.4)',
    clusterBorder: 'rgba(99, 102, 241, 0.2)',
    titleColor: '#e2e8f0',
    edgeLabelBackground: 'rgba(30, 41, 59, 0.8)',
  },
}

const lightThemeConfig = {
  startOnLoad: false,
  theme: 'base' as const,
  themeVariables: {
    primaryColor: '#6366f1',
    primaryTextColor: '#1e293b',
    primaryBorderColor: '#4f46e5',
    lineColor: '#94a3b8',
    secondaryColor: '#e0e7ff',
    tertiaryColor: '#c7d2fe',
    background: 'transparent',
    mainBkg: 'rgba(241, 245, 249, 0.7)',
    nodeBorder: '#4f46e5',
    clusterBkg: 'rgba(241, 245, 249, 0.5)',
    clusterBorder: 'rgba(99, 102, 241, 0.2)',
    titleColor: '#1e293b',
    edgeLabelBackground: 'rgba(241, 245, 249, 0.9)',
  },
}

const TECHNOLOGY_COLORS: Record<string, string> = {
  fastapi: '#009688', django: '#092e20', flask: '#000000',
  express: '#339933', nodejs: '#339933', react: '#61dafb',
  vue: '#42b883', angular: '#dd0031', postgresql: '#336791',
  mongodb: '#47a248', redis: '#dc382d', kafka: '#231f20',
  kubernetes: '#326ce5', docker: '#2496ed', aws: '#ff9900',
  gcp: '#4285f4', azure: '#0078d4', python: '#3776ab',
  typescript: '#3178c6', golang: '#00add8', rust: '#ce422b',
  java: '#b07219', graphql: '#e10098', grpc: '#244c5a',
}

const SEVERITY_COLORS = { critical: '#ef4444', high: '#f97316', medium: '#eab308', low: '#22c55e' }
const DOMAIN_COLORS: Record<string, string> = { microservices: '#6366f1', ai_native: '#8b5cf6', data_pipeline: '#06b6d4' }

mermaid.initialize(darkThemeConfig)

interface ArchitectureViewerProps {
  session: SessionState | null
}

function getTechColor(tech: string): string {
  const lower = tech.toLowerCase()
  for (const [key, color] of Object.entries(TECHNOLOGY_COLORS)) {
    if (lower.includes(key)) return color
  }
  return '#6366f1'
}

function generateServiceMapDiagram(session: SessionState, colorMode: ColorMode): string {
  if (!session.components?.length) return 'graph TD\n  A[No Components]'
  let diagram = 'graph TD\n'
  for (const comp of session.components) {
    const nodeId = comp.name.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '')
    const tech = comp.technology || 'Service'
    const color = colorMode === 'technology' ? getTechColor(tech) :
                  colorMode === 'domain' ? (DOMAIN_COLORS[session?.domain || 'microservices'] || '#6366f1') : '#6366f1'
    const shape = comp.type === 'gateway' ? `[${comp.name}]` :
                  comp.type === 'database' ? `[(${comp.name})]` : `([${comp.name}])`
    diagram += `  ${nodeId}${shape}\n`
    diagram += `  style ${nodeId} fill:${color},stroke:${color},stroke-width:2px,rx:10,ry:10\n`
  }
  for (const conn of (session.connections || [])) {
    const fromId = conn.from.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '')
    const toId = conn.to.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '')
    diagram += `  ${fromId} -->|${conn.protocol || 'HTTP'}| ${toId}\n`
  }
  return diagram
}

function generateDataFlowDiagram(session: SessionState): string {
  if (!session.components?.length) return 'graph LR\n  A[No Data Flow]'
  let diagram = 'graph LR\n'
  diagram += '  subgraph &quot;External&quot;\n    Client[Client App]\n  end\n'
  diagram += '  subgraph &quot;Services&quot;\n'
  for (const comp of session.components) {
    const nodeId = comp.name.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '')
    diagram += `    ${nodeId}[${comp.name}]\n`
  }
  diagram += '  end\n'
  diagram += '  subgraph &quot;Data Stores&quot;\n    DB[(Database)]\n    Cache[(Cache)]\n  end\n'
  for (const comp of session.components) {
    const nodeId = comp.name.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '')
    diagram += `  Client --> ${nodeId}\n  ${nodeId} <--> DB\n`
  }
  return diagram
}

function generateTechnologyDiagram(session: SessionState): string {
  if (!session.components?.length) return 'graph TD\n  A[No Technologies]'
  let diagram = 'graph TB\n'
  const techGroups: Record<string, string[]> = {}
  for (const comp of session.components) {
    const tech = comp.technology || 'Other'
    if (!techGroups[tech]) techGroups[tech] = []
    const nodeId = comp.name.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '')
    techGroups[tech].push(nodeId)
    diagram += `  ${nodeId}((${comp.name}))\n`
    diagram += `  style ${nodeId} fill:${getTechColor(tech)},stroke:#fff,stroke-width:1px\n`
  }
  for (const [tech, nodes] of Object.entries(techGroups)) {
    if (nodes.length > 1) {
      diagram += `  subgraph &quot;${tech}&quot;\n`
      for (const node of nodes) diagram += `    ${node}\n`
      diagram += '  end\n'
    }
  }
  return diagram
}

function generateSeverityDiagram(session: SessionState): string {
  if (!session.failure_modes?.length) return 'graph TD\n  A[No Failure Modes]'
  let diagram = 'graph TD\n'
  for (const failure of session.failure_modes) {
    const nodeId = `FM_${failure.component.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '')}`
    const color = SEVERITY_COLORS[failure.impact as keyof typeof SEVERITY_COLORS] || '#6366f1'
    diagram += `  ${nodeId}{${failure.component}}\n`
    diagram += `  style ${nodeId} fill:${color},stroke:#fff,stroke-width:2px\n`
    diagram += `  ${nodeId} --> ${nodeId}_mit[${failure.mitigation?.slice(0, 30) || 'Mitigation'}]\n`
  }
  return diagram
}

function DiagramSkeleton() {
  return (
    <div className="flex flex-col items-center py-12 gap-4">
      <Skeleton circle width={64} height={64} />
      <Skeleton width={200} height={16} />
      <div className="flex gap-8 mt-4">
        <div className="flex flex-col items-center gap-2">
          <Skeleton circle width={48} height={48} />
          <Skeleton width={80} height={10} />
        </div>
        <div className="flex flex-col items-center gap-2">
          <Skeleton circle width={48} height={48} />
          <Skeleton width={80} height={10} />
        </div>
        <div className="flex flex-col items-center gap-2">
          <Skeleton circle width={48} height={48} />
          <Skeleton width={80} height={10} />
        </div>
      </div>
      <Skeleton width={300} height={4} className="mt-4" />
    </div>
  )
}

export default function ArchitectureViewer({ session }: ArchitectureViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [fullscreen, setFullscreen] = useState(false)
  const [copied, setCopied] = useState(false)
  const [scale, setScale] = useState(1)
  const [error, setError] = useState<string | null>(null)
  const [isDark, setIsDark] = useState(true)
  const [viewMode, setViewMode] = useState<ViewMode>('service')
  const [colorMode, setColorMode] = useState<ColorMode>('technology')
  const [selectedComponent, setSelectedComponent] = useState<Component | null>(null)
  const [showDetails, setShowDetails] = useState(false)
  const [isRendering, setIsRendering] = useState(false)

  const getDiagram = useCallback(() => {
    if (!session) return 'graph TD\n  A[No Data]'
    switch (viewMode) {
      case 'service': return generateServiceMapDiagram(session, colorMode)
      case 'dataflow': return generateDataFlowDiagram(session)
      case 'technology': return generateTechnologyDiagram(session)
      case 'severity': return generateSeverityDiagram(session)
      default: return session.mermaid_diagram || 'graph TD\n  A[No Diagram]'
    }
  }, [session, viewMode, colorMode])

  useEffect(() => {
    const isDarkMode = !document.documentElement.classList.contains('light')
    setIsDark(isDarkMode)
    mermaid.initialize(isDarkMode ? darkThemeConfig : lightThemeConfig)
  }, [])

  useEffect(() => {
    if (!containerRef.current) return
    const renderDiagram = async () => {
      try {
        setIsRendering(true)
        setError(null)
        const diagram = getDiagram()
        const id = `mermaid-${Date.now()}`
        const { svg } = await mermaid.render(id, diagram)
        if (containerRef.current) {
          containerRef.current.innerHTML = svg
          containerRef.current.classList.add('animate-fade-in')
          const svgEl = containerRef.current.querySelector('svg')
          if (svgEl) {
            svgEl.classList.add('max-w-full', 'h-auto')
          }
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to render diagram')
      } finally {
        setIsRendering(false)
      }
    }
    renderDiagram()
  }, [session, viewMode, colorMode, isDark, getDiagram])

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
    navigator.clipboard.writeText(getDiagram())
    setCopied(true)
    toast.success('Mermaid code copied!')
    setTimeout(() => setCopied(false), 2000)
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

  const downloadPNG = () => {
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
      downloadLink.download = `architecture-${viewMode}.png`
      downloadLink.href = pngFile
      downloadLink.click()
      toast.success('PNG downloaded!')
    }
    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)))
  }

  const downloadSVG = () => {
    if (!containerRef.current) return
    const svg = containerRef.current.querySelector('svg')
    if (!svg) return
    const blob = new Blob([new XMLSerializer().serializeToString(svg)], { type: 'image/svg+xml' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.download = `architecture-${viewMode}.svg`
    link.href = url
    link.click()
    URL.revokeObjectURL(url)
    toast.success('SVG downloaded!')
  }

  const downloadPDF = async () => {
    if (!session) return
    try {
      toast.info('Generating PDF...', { description: 'This may take a few seconds.' })
      const blob = await exportDocs({
        requirement: session.requirement?.text || 'N/A',
        domain: session.domain || 'Unknown',
        created_at: session.created_at,
        components: session.components,
        adrs: session.adrs,
        failure_modes: session.failure_modes,
        phases: session.phases
      })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `ELDER_Architecture_Report.pdf`
      link.click()
      URL.revokeObjectURL(url)
      toast.success('PDF downloaded!')
    } catch (err) {
      toast.error('Failed to download PDF')
    }
  }

  const downloadPPTX = async () => {
    if (!session) return
    try {
      toast.info('Generating PPTX...', { description: 'Preparing slide deck.' })
      const blob = await exportSlides({
        requirement: session.requirement?.text || 'N/A',
        domain: session.domain || 'Unknown',
        created_at: session.created_at,
        components: session.components,
        adrs: session.adrs,
        failure_modes: session.failure_modes,
        phases: session.phases
      })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `ELDER_Presentation_Deck.pptx`
      link.click()
      URL.revokeObjectURL(url)
      toast.success('PPTX downloaded!')
    } catch (err) {
      toast.error('Failed to download PPTX')
    }
  }

  const shareArchitecture = async () => {
    const data = { diagram: getDiagram(), viewMode, colorMode, timestamp: new Date().toISOString() }
    const base64 = btoa(unescape(encodeURIComponent(JSON.stringify(data))))
    const shareUrl = `${window.location.origin}?arch=${base64}`
    if (navigator.share) {
      await navigator.share({ title: 'Architecture Diagram', text: 'Check out this architecture design', url: shareUrl })
    } else {
      await navigator.clipboard.writeText(shareUrl)
      toast.success('Share URL copied!')
    }
  }

  // Empty state
  if (!session) {
    return (
      <div className="glass-panel text-center py-14">
        <div className="w-16 h-16 mx-auto mb-4 rounded-2xl flex items-center justify-center animate-float bg-indigo-500/10 border border-indigo-500/20">
          <Network className="w-8 h-8 text-violet-400" />
        </div>
        <h3 className="text-base font-medium mb-1.5 text-secondary">
          No Architecture Yet
        </h3>
        <p className="text-sm text-muted">
          Enter your requirements to generate an architecture diagram
        </p>
      </div>
    )
  }

  const viewModes = [
    { id: 'service' as ViewMode, label: 'Service Map', icon: Layers },
    { id: 'dataflow' as ViewMode, label: 'Data Flow', icon: GitBranch },
    { id: 'technology' as ViewMode, label: 'Tech Stack', icon: Eye },
    { id: 'severity' as ViewMode, label: 'Failure Risk', icon: AlertTriangle },
  ]

  const colorModes = [
    { id: 'technology' as ColorMode, label: 'By Technology' },
    { id: 'severity' as ColorMode, label: 'By Severity' },
    { id: 'domain' as ColorMode, label: 'By Domain' },
  ]

  return (
    <div className="glass-panel !p-0 overflow-hidden">
      {/* ─── Toolbar ─── */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between px-5 py-3 gap-3 border-b border-glass">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-gradient-to-br from-violet-500/20 to-indigo-500/20 border border-violet-500/20">
            <Network className="w-4 h-4 text-violet-400" />
          </div>
          <h3 className="text-sm font-semibold text-primary">
            Architecture Diagram
          </h3>
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="p-1.5 rounded-lg glass transition-all text-muted"
            title="Toggle details"
          >
            <Info className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="flex p-1 rounded-xl glass">
            {viewModes.map((mode) => (
              <button
                key={mode.id}
                onClick={() => setViewMode(mode.id)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  viewMode === mode.id ? 'tab-active text-white' : 'text-secondary'
                }`}
                title={mode.label}
              >
                <mode.icon className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">{mode.label}</span>
              </button>
            ))}
          </div>

          {viewMode === 'service' && (
            <select
              value={colorMode}
              onChange={(e) => setColorMode(e.target.value as ColorMode)}
              className="input-glass !px-2 !py-1.5 !rounded-lg text-xs !w-auto cursor-pointer"
              aria-label="Selection coloration mode"
              title="Selection coloration mode"
            >
              {colorModes.map((mode) => (
                <option key={mode.id} value={mode.id} className="bg-slate-900">{mode.label}</option>
              ))}
            </select>
          )}
        </div>

        {/* Toolbar actions */}
        <div className="hidden md:flex items-center gap-1">
          <button onClick={() => setScale((s) => Math.max(0.5, s - 0.1))} className="p-1.5 glass rounded-lg transition-all text-muted" title="Zoom out">
            <ZoomOut className="w-4 h-4" />
          </button>
          <span className="text-xs w-10 text-center font-mono text-muted">
            {Math.round(scale * 100)}%
          </span>
          <button onClick={() => setScale((s) => Math.min(2, s + 0.1))} className="p-1.5 glass rounded-lg transition-all text-muted" title="Zoom in">
            <ZoomIn className="w-4 h-4" />
          </button>
          <div className="w-px h-4 mx-1 border-r border-glass" />
          <button onClick={copyMermaid} className="p-1.5 glass rounded-lg transition-all text-muted" title="Copy Mermaid code">
            {copied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
          </button>
          <button onClick={downloadSVG} className="p-1.5 glass rounded-lg transition-all text-muted" title="Download SVG">
            <Download className="w-4 h-4" />
          </button>
          <button onClick={downloadPNG} className="p-1.5 glass rounded-lg transition-all text-muted" title="Download PNG">
            <Download className="w-4 h-4" />
          </button>
          <div className="w-px h-4 mx-1 border-r border-glass" />
          <button onClick={downloadPDF} className="p-1.5 glass rounded-lg transition-all text-muted" title="Download Architecture Report (PDF)">
            <FileText className="w-4 h-4" />
          </button>
          <button onClick={downloadPPTX} className="p-1.5 glass rounded-lg transition-all text-muted" title="Download Slide Deck (PPTX)">
            <Presentation className="w-4 h-4" />
          </button>
          <button onClick={shareArchitecture} className="p-1.5 glass rounded-lg transition-all text-muted" title="Share">
            <Share2 className="w-4 h-4" />
          </button>
          <button onClick={toggleFullscreen} className="p-1.5 glass rounded-lg transition-all text-muted" title="Fullscreen">
            {fullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* ─── Diagram Area ─── */}
      <div className="flex flex-col lg:flex-row">
        <div
          className={`flex-1 p-6 overflow-auto scrollbar-thin ${fullscreen ? 'max-h-[calc(100vh-100px)]' : 'max-h-[520px]'}`}
        >
          {isRendering ? (
            <DiagramSkeleton />
          ) : error ? (
            <div className="text-center py-12">
              <p className="text-red-400 font-medium">Failed to render diagram</p>
              <p className="text-sm mt-1 text-muted">{error}</p>
            </div>
          ) : (
            <div
              ref={containerRef}
              className="flex justify-center transition-transform origin-center"
              style={{ transform: `scale(${scale})` }}
            />
          )}
        </div>

        {/* ─── Component Details Sidebar ─── */}
        {showDetails && session.components?.length > 0 && (
          <div className="w-full lg:w-80 p-5 overflow-auto max-h-64 lg:max-h-[520px] scrollbar-thin animate-slide-up border-l border-glass">
            <h4 className="text-xs font-medium tracking-widest uppercase mb-3 text-muted">
              Components ({session.components.length})
            </h4>
            <div className="space-y-2">
              {session.components.map((comp, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedComponent(comp)}
                  className={`w-full text-left p-3 rounded-xl transition-all ${
                    selectedComponent === comp ? 'glass-card border-accent' : 'glass'
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: getTechColor(comp.technology || comp.name) }} />
                    <span className="text-sm font-medium truncate text-primary">{comp.name}</span>
                  </div>
                  {comp.technology && (
                    <p className="text-xs mt-1 ml-5" style={{ color: 'var(--text-muted)' }}>{comp.technology}</p>
                  )}
                </button>
              ))}
            </div>

            {selectedComponent && (
              <div className="mt-4 p-4 glass-card animate-slide-up">
                <h5 className="text-sm font-semibold mb-2 text-primary">{selectedComponent.name}</h5>
                {selectedComponent.technology && <p className="text-xs mb-1 text-secondary">Technology: {selectedComponent.technology}</p>}
                {selectedComponent.type && <p className="text-xs mb-2 text-secondary">Type: {selectedComponent.type}</p>}
                {selectedComponent.responsibilities?.length > 0 && (
                  <div>
                    <p className="text-[10px] font-medium tracking-widest uppercase mb-1 text-muted">Responsibilities</p>
                    <ul className="text-xs list-disc list-inside space-y-0.5 text-secondary">
                      {selectedComponent.responsibilities.map((r, i) => <li key={i}>{r}</li>)}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* ─── Footer Stats ─── */}
      <div className="px-5 py-3 border-t border-glass bg-surface-card">
        <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-muted">
          <div className="flex items-center gap-4">
            <span>{session.components?.length || 0} components</span>
            <span>{session.connections?.length || 0} connections</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="capitalize">{viewMode.replace(/([A-Z])/g, ' $1').trim()}</span>
            <span className="opacity-40">•</span>
            <span className="capitalize">{colorMode}</span>
          </div>
        </div>
      </div>
    </div>
  )
}
