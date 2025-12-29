"""Pydantic schemas for agent outputs and API contracts."""

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Recommendation(str, Enum):
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    HOLD = "hold"
    SELL = "sell"
    STRONG_SELL = "strong_sell"


class AgentOutput(BaseModel):
    """Base output schema for all specialist agents."""

    score: int = Field(..., ge=0, le=100, description="Numerical score (0-100 scale)")
    confidence: ConfidenceLevel = Field(
        ..., description="Confidence level of the analysis"
    )
    evidence: list[str] = Field(
        ..., description="Key supporting evidence (specific data points)"
    )
    concerns: list[str] = Field(
        default_factory=list, description="Primary concerns or caveats"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class QuantAnalystOutput(AgentOutput):
    """Output from the Quant Analyst agent."""

    agent_type: Literal["quant_analyst"] = "quant_analyst"
    rsi: float | None = Field(None, description="Relative Strength Index value")
    macd_signal: str | None = Field(None, description="MACD signal interpretation")
    moving_averages: dict[str, float] | None = Field(
        None, description="Key moving average values"
    )
    patterns_identified: list[str] = Field(
        default_factory=list, description="Chart patterns found"
    )
    support_levels: list[float] = Field(
        default_factory=list, description="Key support levels"
    )
    resistance_levels: list[float] = Field(
        default_factory=list, description="Key resistance levels"
    )


class SentimentScoutOutput(AgentOutput):
    """Output from the Sentiment Scout agent."""

    agent_type: Literal["sentiment_scout"] = "sentiment_scout"
    narrative_summary: str = Field(
        ..., description="Summary of current market narrative"
    )
    news_sentiment: str | None = Field(None, description="Overall news sentiment")
    volume_analysis: str | None = Field(None, description="Volume anomaly observations")
    contrarian_signals: list[str] = Field(
        default_factory=list, description="Potential contrarian indicators"
    )


class MacroStrategistOutput(AgentOutput):
    """Output from the Macro Strategist agent."""

    agent_type: Literal["macro_strategist"] = "macro_strategist"
    sector_outlook: str = Field(..., description="Sector performance assessment")
    macro_alignment: str = Field(
        ..., description="How well the asset aligns with macro trends"
    )
    intermarket_signals: list[str] = Field(
        default_factory=list, description="Related market signals"
    )
    regime_assessment: str | None = Field(
        None, description="Current market regime classification"
    )


class RiskManagerOutput(AgentOutput):
    """Output from the Risk Manager agent."""

    agent_type: Literal["risk_manager"] = "risk_manager"
    position_size_pct: float = Field(
        ..., ge=0, le=100, description="Recommended position size as % of portfolio"
    )
    max_drawdown_pct: float | None = Field(
        None, description="Historical max drawdown percentage"
    )
    volatility_assessment: str = Field(..., description="Volatility analysis summary")
    correlation_risks: list[str] = Field(
        default_factory=list, description="Correlation risk factors"
    )
    stop_loss_level: float | None = Field(None, description="Suggested stop loss price")
    invalidation_criteria: list[str] = Field(
        default_factory=list, description="Conditions that invalidate the thesis"
    )


class AgentScore(BaseModel):
    """Individual agent score for the consensus report."""

    agent_name: str
    score: int = Field(..., ge=0, le=100)
    rationale: str


class ConsensusReport(BaseModel):
    """Final consensus report from the Portfolio Chief."""

    ticker: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    recommendation: Recommendation
    confidence: ConfidenceLevel
    agent_scores: list[AgentScore]
    key_agreements: list[str] = Field(..., description="Points where agents agree")
    key_disagreements: list[str] = Field(
        default_factory=list, description="Points of contention"
    )
    disagreement_resolution: str | None = Field(
        None, description="How disagreements were resolved"
    )
    position_size_pct: float = Field(..., ge=0, le=100)
    risk_factors: list[str]
    invalidation_criteria: list[str]
    executive_summary: str


# API Contracts


class AnalysisRequest(BaseModel):
    """Request to analyze a ticker."""

    ticker: str = Field(
        ..., min_length=1, max_length=10, description="Stock ticker symbol"
    )
    context: str | None = Field(
        None, description="Optional analysis context or focus areas"
    )


class AnalysisResponse(BaseModel):
    """Response containing analysis ID for streaming."""

    analysis_id: str
    stream_url: str
    status: str = "started"


class AgentMessageType(str, Enum):
    THINKING = "thinking"
    ANALYSIS = "analysis"
    DEBATE = "debate"
    CONCLUSION = "conclusion"
    ERROR = "error"


class AgentMessage(BaseModel):
    """A message from an agent during deliberation (for SSE streaming)."""

    analysis_id: str
    agent_id: str
    agent_name: str
    message_type: AgentMessageType
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict | None = None


class AgentInfo(BaseModel):
    """Information about an available agent."""

    id: str
    name: str
    role: str
    description: str
    focus_areas: list[str]


class AnalysisHistoryItem(BaseModel):
    """A past analysis record."""

    analysis_id: str
    ticker: str
    recommendation: Recommendation
    confidence: ConfidenceLevel
    timestamp: datetime
