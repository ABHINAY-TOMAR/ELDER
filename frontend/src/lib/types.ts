export interface Memory {
  id: string
  category: string
  content: string
  embedding?: number[]
  created_at: string
}

export interface TokenUsage {
  input_tokens: number
  output_tokens: number
  total_tokens: number
  cost_usd: number
  model: string
  timestamp: string
}

export interface Requirement {
  text: string
  domain: string
  constraints: string[]
  stakeholders: string[]
}

export interface Component {
  name: string
  type: 'frontend' | 'backend' | 'database' | 'cache' | 'queue' | 'gateway' | 'service'
  description: string
  technology?: string
  responsibilities: string[]
}

export interface ADR {
  id: string
  title: string
  decision: string
  rationale: string
  consequences: string[]
  status: 'proposed' | 'accepted' | 'deprecated'
}

export interface FailureMode {
  component: string
  failure_type: string
  probability: 'low' | 'medium' | 'high'
  impact: 'low' | 'medium' | 'high'
  mitigation: string
}

export interface Phase {
  id: string
  name: string
  status: 'pending' | 'in_progress' | 'completed' | 'failed'
  tasks: Task[]
  started_at?: string
  completed_at?: string
}

export interface Task {
  id: string
  title: string
  description: string
  status: 'pending' | 'in_progress' | 'completed' | 'failed'
  assignee?: string
  dependencies: string[]
}

export interface AgentDispatch {
  id: string
  agent_name: string
  task: string
  status: 'queued' | 'running' | 'completed' | 'failed'
  started_at?: string
  completed_at?: string
  result?: string
  error?: string
}

export interface SessionState {
  id: string
  requirement: Requirement
  components: Component[]
  adrs: ADR[]
  failure_modes: FailureMode[]
  phases: Phase[]
  dispatches: AgentDispatch[]
  memory: Memory[]
  tokens: {
    total: number
    input: number
    output: number
    cost: number
  }
  mermaid_diagram?: string
  created_at: string
  updated_at: string
}
