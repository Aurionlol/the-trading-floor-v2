export type AgentMessageType = 'thinking' | 'analysis' | 'debate' | 'conclusion' | 'error';

export interface AgentMessage {
  analysis_id: string;
  agent_id: string;
  agent_name: string;
  message_type: AgentMessageType;
  content: string;
  timestamp: string;
  metadata?: any; // Using any for flexibility, but ideally strictly typed to ConsensusReport
}

export interface AnalysisRequest {
  ticker: string;
  context?: string;
}

export interface AnalysisResponse {
  analysis_id: string;
  stream_url: string;
  status: string;
}

export interface Agent {
    id: string;
    name: string;
    role: string;
    description: string;
}

export interface AgentState {
    id: string;
    name: string;
    status: 'idle' | 'thinking' | 'done';
}

export type Recommendation = "strong_buy" | "buy" | "hold" | "sell" | "strong_sell";
export type ConfidenceLevel = "low" | "medium" | "high";

export interface AgentScore {
    agent_name: string;
    score: number;
    rationale: string;
}

export interface ConsensusReport {
    ticker: string;
    timestamp: string;
    recommendation: Recommendation;
    confidence: ConfidenceLevel;
    agent_scores: AgentScore[];
    key_agreements: string[];
    key_disagreements: string[];
    disagreement_resolution?: string;
    position_size_pct: number;
    risk_factors: string[];
    invalidation_criteria: string[];
    executive_summary: string;
}
