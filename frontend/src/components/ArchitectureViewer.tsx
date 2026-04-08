import { useEffect, useRef, useState, useCallback } from 'react'
import { Maximize2, Minimize2, Copy, Check, ZoomIn, ZoomOut, Download, Share2, Eye, GitBranch, Layers, AlertTriangle, Info } from 'lucide-react'
import mermaid from 'mermaid'
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

const TECHNOLOGY_COLORS: Record<string, string> = {
  fastapi: '#009688',
  django: '#092e20',
  flask: '#000000',
  express: '#339933',
  nodejs: '#339933',
  react: '#61dafb',
  vue: '#42b883',
  angular: '#dd0031',
  postgresql: '#336791',
  mongodb: '#47a248',
  redis: '#dc382d',
  kafka: '#231f20',
  kubernetes: '#326ce5',
  docker: '#2496ed',
  aws: '#ff9900',
  gcp: '#4285f4',
  azure: '#0078d4',
  python: '#3776ab',
  typescript: '#3178c6',
  golang: '#00add8',
  rust: '#ce422b',
  java: '#b07219',
  graphql: '#e10098',
  grpc: '#244c5a',
}

const SEVERITY_COLORS = {
  critical: '#ef4444',
  high: '#f97316',
  medium: '#eab308',
  low: '#22c55e',
}

const DOMAIN_COLORS = {
  microservices: '#6366f1',
  ai_native: '#8b5cf6',
  data_pipeline: '#06b6d4',
}

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

function getNodeStyle(nodeId: string, components: Component[], colorMode: ColorMode): string {
  const component = components.find(c => 
    c.name.toLowerCase().replace(/\s+/g, '_') === nodeId.toLowerCase() ||
    c.name.toLowerCase() === nodeId.toLowerCase()
  )
  
  if (!component) return ''
  
  let color = '#6366f1'
  
  if (colorMode === 'technology') {
    color = getTechColor(component.technology || component.name)
  } else if (colorMode === 'domain') {
    color = DOMAIN_COLORS[session?.domain || 'microservices'] || '#6366f1'
  }
  
  return `style=&quot;fill:${color};stroke:${color};stroke-width:2px;&quot;`
}

function generateServiceMapDiagram(session: SessionState, colorMode: ColorMode): string {
  if (!session.components || session.components.length === 0) {
    return 'graph TD\n  A[No Components]'
  }
  
  let diagram = 'graph TD\n'
  
  const components = session.components
  const connections = session.connections || []
  
  for (const comp of components) {
    const nodeId = comp.name.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '')
    const tech = comp.technology || 'Service'
    const color = colorMode === 'technology' ? getTechColor(tech) : 
                  colorMode === 'domain' ? (DOMAIN_COLORS[session?.domain || 'microservices'] || '#6366f1') : '#6366f1'
    
    const shape = comp.type === 'gateway' ? `[${comp.name}]` :
                  comp.type === 'database' ? `[(${comp.name})]` :
                  `([${comp.name}])`
    
    diagram += `  ${nodeId}${shape}\n`
    diagram += `  style ${nodeId} fill:${color},stroke:${color},stroke-width:2px,rx:10,ry:10\n`
  }
  
  for (const conn of connections) {
    const fromId = conn.from.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '')
    const toId = conn.to.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '')
    const protocol = conn.protocol || 'HTTP'
    diagram += `  ${fromId} -->|${protocol}| ${toId}\n`
  }
  
  return diagram
}

function generateDataFlowDiagram(session: SessionState): string {
  if (!session.components || session.components.length === 0) {
    return 'graph LR\n  A[No Data Flow]'
  }
  
  let diagram = 'graph LR\n'
  
  diagram += '  subgraph &quot;External&quot;\n'
  diagram += '    Client[Client App]\n'
  diagram += '  end\n'
  
  diagram += '  subgraph &quot;Services&quot;\n'
  for (const comp of session.components) {
    const nodeId = comp.name.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '')
    const tech = comp.technology || 'Service'
    diagram += `    ${nodeId}[${comp.name}]:::${tech.replace(/\s+/g, '')}\n`
  }
  diagram += '  end\n'
  
  diagram += '  subgraph &quot;Data Stores&quot;\n'
  diagram += '    DB[(Database)]\n'
  diagram += '    Cache[(Cache)]\n'
  diagram += '  end\n'
  
  for (const comp of session.components) {
    const nodeId = comp.name.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '')
    diagram += `  Client --> ${nodeId}\n`
    diagram += `  ${nodeId} <--> DB\n`
  }
  
  for (const tech of Object.keys(TECHNOLOGY_COLORS)) {
    const techClass = tech.replace(/\s+/g, '')
    diagram += `  classDef ${techClass} fill:#${TECHNOLOGY_COLORS[tech].slice(1)},stroke:#${TECHNOLOGY_COLORS[tech].slice(1)}\n`
  }
  
  return diagram
}

function generateTechnologyDiagram(session: SessionState): string {
  if (!session.components || session.components.length === 0) {
    return 'graph TD\n  A[No Technologies]'
  }
  
  let diagram = 'graph TB\n'
  
  const techGroups: Record<string, string[]> = {}
  
  for (const comp of session.components) {
    const tech = comp.technology || 'Other'
    if (!techGroups[tech]) techGroups[tech] = []
    const nodeId = comp.name.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '')
    techGroups[tech].push(nodeId)
    
    const color = getTechColor(tech)
    diagram += `  ${nodeId}((${comp.name}))\n`
    diagram += `  style ${nodeId} fill:${color},stroke:#fff,stroke-width:1px\n`
  }
  
  for (const [tech, nodes] of Object.entries(techGroups)) {
    if (nodes.length > 1) {
      diagram += `  subgraph &quot;${tech}&quot;\n`
      for (const node of nodes) {
        diagram += `    ${node}\n`
      }
      diagram += '  end\n'
    }
  }
  
  return diagram
}

function generateSeverityDiagram(session: SessionState): string {
  if (!session.failure_modes || session.failure_modes.length === 0) {
    return 'graph TD\n  A[No Failure Modes]'
  }
  
  let diagram = 'graph TD\n'
  
  for (const failure of session.failure_modes) {
    const nodeId = `FM_${failure.component.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '')}`
    const color = SEVERITY_COLORS[failure.impact as keyof typeof SEVERITY_COLORS] || '#6366f1'
    
    diagram += `  ${nodeId}{${failure.component}}\n`
    diagram += `  style ${nodeId} fill:${color},stroke:#fff,stroke-width:2px\n`
    
    const mitNodeId = `${nodeId}_mit`
    diagram += `  ${nodeId} --> ${mitNodeId}[${failure.mitigation?.slice(0, 30) || 'Mitigation'}]\n`
  }
  
  return diagram
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

  const getDiagram = useCallback(() => {
    if (!session) return 'graph TD\n  A[No Data]'
    
    switch (viewMode) {
      case 'service':
        return generateServiceMapDiagram(session, colorMode)
      case 'dataflow':
        return generateDataFlowDiagram(session)
      case 'technology':
        return generateTechnologyDiagram(session)
      case 'severity':
        return generateSeverityDiagram(session)
      default:
        return session.mermaid_diagram || 'graph TD\n  A[No Diagram]'
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
        setError(null)
        const diagram = getDiagram()
        const id = `mermaid-${Date.now()}`
        const { svg } = await mermaid.render(id, diagram)
        if (containerRef.current) {
          containerRef.current.innerHTML = svg
          containerRef.current.classList.add('animate-fade-in')
          
          const svgEl = containerRef.current.querySelector('svg')
          if (svgEl) {
            svgEl.style.maxWidth = '100%'
            svgEl.style.height = 'auto'
          }
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to render diagram')
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
    const diagram = getDiagram()
    navigator.clipboard.writeText(diagram)
    setCopied(true)
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
    }
    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)))
  }

  const downloadSVG = () => {
    if (!containerRef.current) return
    const svg = containerRef.current.querySelector('svg')
    if (!svg) return
    const svgData = new XMLSerializer().serializeToString(svg)
    const blob = new Blob([svgData], { type: 'image/svg+xml' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.download = `architecture-${viewMode}.svg`
    link.href = url
    link.click()
    URL.revokeObjectURL(url)
  }

  const shareArchitecture = async () => {
    const diagram = getDiagram()
    const data = {
      diagram,
      viewMode,
      colorMode,
      timestamp: new Date().toISOString(),
    }
    const jsonStr = JSON.stringify(data)
    const base64 = btoa(unescape(encodeURIComponent(jsonStr)))
    const shareUrl = `${window.location.origin}?arch=${base64}`
    
    if (navigator.share) {
      await navigator.share({
        title: 'Architecture Diagram',
        text: 'Check out this architecture design',
        url: shareUrl,
      })
    } else {
      await navigator.clipboard.writeText(shareUrl)
      alert('Share URL copied to clipboard!')
    }
  }

  if (!session) {
    return (
      <div className="bg-slate-900 dark:bg-slate-900 border border-slate-800 dark:border-slate-800 rounded-xl p-8 text-center">
        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-slate-800 dark:bg-slate-800 flex items-center justify-center">
          <svg className="w-8 h-8 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-slate-400 dark:text-slate-400 mb-2">No Architecture Yet</h3>
        <p className="text-sm text-slate-500 dark:text-slate-500">Enter your requirements to generate an architecture diagram</p>
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
    <div className="bg-slate-900 dark:bg-slate-900 border border-slate-800 dark:border-slate-800 rounded-xl overflow-hidden">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between px-4 py-3 border-b border-slate-800 dark:border-slate-800 gap-3">
        <div className="flex items-center gap-2">
          <h3 className="text-sm font-medium text-slate-300 dark:text-slate-300">Architecture Diagram</h3>
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="p-1 hover:bg-slate-800 dark:hover:bg-slate-800 text-slate-400 hover:text-slate-300 rounded transition-colors"
            title="Toggle details"
          >
            <Info className="w-4 h-4" />
          </button>
        </div>
        
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex bg-slate-800 dark:bg-slate-800 rounded-lg p-1">
            {viewModes.map((mode) => (
              <button
                key={mode.id}
                onClick={() => setViewMode(mode.id)}
                className={`flex items-center gap-1.5 px-2 py-1 rounded text-xs font-medium transition-all ${
                  viewMode === mode.id
                    ? 'bg-violet-600 text-white'
                    : 'text-slate-400 hover:text-white'
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
              className="px-2 py-1 bg-slate-800 dark:bg-slate-800 border border-slate-700 dark:border-slate-700 rounded text-xs text-slate-300 focus:outline-none focus:ring-2 focus:ring-violet-500"
            >
              {colorModes.map((mode) => (
                <option key={mode.id} value={mode.id}>{mode.label}</option>
              ))}
            </select>
          )}
        </div>

        <div className="hidden md:flex items-center gap-1">
          <button
            onClick={() => setScale((s) => Math.max(0.5, s - 0.1))}
            className="p-1.5 hover:bg-slate-800 dark:hover:bg-slate-800 text-slate-400 hover:text-slate-300 rounded transition-colors"
            title="Zoom out"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <span className="text-xs text-slate-500 w-12 text-center">{Math.round(scale * 100)}%</span>
          <button
            onClick={() => setScale((s) => Math.min(2, s + 0.1))}
            className="p-1.5 hover:bg-slate-800 dark:hover:bg-slate-800 text-slate-400 hover:text-slate-300 rounded transition-colors"
            title="Zoom in"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <div className="w-px h-4 bg-slate-700 mx-1" />
          <button
            onClick={copyMermaid}
            className="p-1.5 hover:bg-slate-800 dark:hover:bg-slate-800 text-slate-400 hover:text-slate-300 rounded transition-colors"
            title="Copy Mermaid code"
          >
            {copied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
          </button>
          <button
            onClick={downloadSVG}
            className="p-1.5 hover:bg-slate-800 dark:hover:bg-slate-800 text-slate-400 hover:text-slate-300 rounded transition-colors"
            title="Download SVG"
          >
            <Download className="w-4 h-4" />
          </button>
          <button
            onClick={downloadPNG}
            className="p-1.5 hover:bg-slate-800 dark:hover:bg-slate-800 text-slate-400 hover:text-slate-300 rounded transition-colors"
            title="Download PNG"
          >
            <Download className="w-4 h-4" />
          </button>
          <button
            onClick={shareArchitecture}
            className="p-1.5 hover:bg-slate-800 dark:hover:bg-slate-800 text-slate-400 hover:text-slate-300 rounded transition-colors"
            title="Share"
          >
            <Share2 className="w-4 h-4" />
          </button>
          <button
            onClick={toggleFullscreen}
            className="p-1.5 hover:bg-slate-800 dark:hover:bg-slate-800 text-slate-400 hover:text-slate-300 rounded transition-colors"
            title="Toggle fullscreen"
          >
            {fullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row">
        <div 
          className="flex-1 p-4 overflow-auto" 
          style={{ maxHeight: fullscreen ? 'calc(100vh - 100px)' : '500px' }}
        >
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

        {showDetails && session.components && session.components.length > 0 && (
          <div className="w-full lg:w-80 border-t lg:border-t-0 lg:border-l border-slate-800 dark:border-slate-800 p-4 overflow-auto max-h-64 lg:max-h-96">
            <h4 className="text-sm font-medium text-slate-300 dark:text-slate-300 mb-3">Components ({session.components.length})</h4>
            <div className="space-y-2">
              {session.components.map((comp, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedComponent(comp)}
                  className={`w-full text-left p-2 rounded-lg transition-colors ${
                    selectedComponent === comp
                      ? 'bg-violet-600/20 border border-violet-500'
                      : 'bg-slate-800/50 hover:bg-slate-800 border border-transparent'
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: getTechColor(comp.technology || comp.name) }}
                    />
                    <span className="text-sm font-medium text-slate-200 truncate">{comp.name}</span>
                  </div>
                  {comp.technology && (
                    <p className="text-xs text-slate-500 mt-1 ml-5">{comp.technology}</p>
                  )}
                </button>
              ))}
            </div>

            {selectedComponent && (
              <div className="mt-4 p-3 bg-slate-800/50 rounded-lg border border-slate-700">
                <h5 className="text-sm font-medium text-slate-200">{selectedComponent.name}</h5>
                {selectedComponent.technology && (
                  <p className="text-xs text-slate-400 mt-1">Technology: {selectedComponent.technology}</p>
                )}
                {selectedComponent.type && (
                  <p className="text-xs text-slate-400">Type: {selectedComponent.type}</p>
                )}
                {selectedComponent.responsibilities && selectedComponent.responsibilities.length > 0 && (
                  <div className="mt-2">
                    <p className="text-xs text-slate-500">Responsibilities:</p>
                    <ul className="text-xs text-slate-400 mt-1 list-disc list-inside">
                      {selectedComponent.responsibilities.map((r, i) => (
                        <li key={i}>{r}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      <div className="px-4 py-3 border-t border-slate-800 dark:border-t-slate-800 bg-slate-900/50 dark:bg-slate-900/50">
        <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-slate-500">
          <div className="flex items-center gap-4">
            <span>{session.components?.length || 0} components</span>
            <span>{session.connections?.length || 0} connections</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="capitalize">{viewMode.replace(/([A-Z])/g, ' $1').trim()}</span>
            <span>•</span>
            <span className="capitalize">{colorMode}</span>
          </div>
        </div>
      </div>
    </div>
  )
}
