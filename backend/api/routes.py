"""FastAPI routes for the Trading Floor API."""

import asyncio
import uuid
from collections.abc import AsyncGenerator
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, HTTPException
from sse_starlette.sse import EventSourceResponse

from backend.crews import create_trading_crew
from backend.schemas import (
    AgentInfo,
    AgentMessage,
    AgentMessageType,
    AnalysisHistoryItem,
    AnalysisRequest,
    AnalysisResponse,
)

router = APIRouter()

# In-memory storage for demo purposes
# In production, use Redis or a database
_analyses: dict[str, dict] = {}
_message_queues: dict[str, asyncio.Queue] = {}


@router.get("/agents", response_model=list[AgentInfo])
async def list_agents() -> list[AgentInfo]:
    """List all available agents and their descriptions."""
    return [
        AgentInfo(
            id="quant_analyst",
            name="Quant Analyst",
            role="Quantitative Analyst",
            description="Technical analysis specialist focused on price patterns, indicators, and statistical signals.",
            focus_areas=[
                "Moving averages",
                "RSI & MACD",
                "Bollinger Bands",
                "Chart patterns",
                "Support/Resistance",
                "Volume analysis",
            ],
        ),
        AgentInfo(
            id="sentiment_scout",
            name="Sentiment Scout",
            role="Sentiment Analyst",
            description="Market sentiment and crowd psychology specialist tracking narratives and contrarian signals.",
            focus_areas=[
                "News flow analysis",
                "Volume anomalies",
                "Contrarian signals",
                "Fear/greed indicators",
                "Narrative tracking",
            ],
        ),
        AgentInfo(
            id="macro_strategist",
            name="Macro Strategist",
            role="Macro Strategist",
            description="Top-down analyst connecting individual stocks to sector dynamics and macroeconomic themes.",
            focus_areas=[
                "Sector rotation",
                "Index correlation",
                "Market regime",
                "Relative strength",
                "Cross-asset signals",
            ],
        ),
        AgentInfo(
            id="risk_manager",
            name="Risk Manager",
            role="Risk Manager",
            description="Conservative risk analyst focused on capital preservation, position sizing, and downside scenarios.",
            focus_areas=[
                "Volatility analysis",
                "Drawdown history",
                "Position sizing",
                "Stop-loss levels",
                "Correlation risk",
            ],
        ),
        AgentInfo(
            id="portfolio_chief",
            name="Portfolio Chief",
            role="Portfolio Chief",
            description="Senior decision-maker who synthesizes all analyses and delivers final recommendations.",
            focus_areas=[
                "Evidence synthesis",
                "Conflict resolution",
                "Final recommendation",
                "Risk/reward assessment",
            ],
        ),
    ]


@router.post("/analyze", response_model=AnalysisResponse)
async def start_analysis(
    request: AnalysisRequest, background_tasks: BackgroundTasks
) -> AnalysisResponse:
    """
    Start a new analysis for a ticker.

    Returns an analysis ID that can be used to stream results via SSE.
    """
    analysis_id = str(uuid.uuid4())

    # Initialize storage
    _analyses[analysis_id] = {
        "ticker": request.ticker.upper(),
        "context": request.context,
        "status": "running",
        "started_at": datetime.utcnow(),
        "result": None,
        "error": None,
    }
    _message_queues[analysis_id] = asyncio.Queue()

    # Run analysis in background
    background_tasks.add_task(
        _run_analysis_task,
        analysis_id,
        request.ticker.upper(),
        request.context,
    )

    return AnalysisResponse(
        analysis_id=analysis_id,
        stream_url=f"/api/stream/{analysis_id}",
        status="started",
    )


async def _run_analysis_task(
    analysis_id: str, ticker: str, context: str | None
) -> None:
    """Background task to run the crew analysis."""
    queue = _message_queues.get(analysis_id)
    if not queue:
        return

    try:
        # Send initial message
        await queue.put(
            AgentMessage(
                analysis_id=analysis_id,
                agent_id="system",
                agent_name="System",
                message_type=AgentMessageType.THINKING,
                content=f"Starting analysis for {ticker}...",
            )
        )

        # Create and run the crew
        crew = create_trading_crew(ticker, context)

        # Note: For full streaming, you'd use CrewAI's callback/streaming features
        # This is a simplified version that runs the crew and reports the result
        await queue.put(
            AgentMessage(
                analysis_id=analysis_id,
                agent_id="system",
                agent_name="System",
                message_type=AgentMessageType.THINKING,
                content="Crew assembled. Specialists are analyzing...",
            )
        )

        # Run the crew (blocking in the background task)
        result = crew.kickoff(inputs={"ticker": ticker})

        # Store result
        _analyses[analysis_id]["result"] = result.raw
        _analyses[analysis_id]["status"] = "completed"

        # Send completion message
        await queue.put(
            AgentMessage(
                analysis_id=analysis_id,
                agent_id="portfolio_chief",
                agent_name="Portfolio Chief",
                message_type=AgentMessageType.CONCLUSION,
                content=result.raw,
            )
        )

    except Exception as e:
        _analyses[analysis_id]["error"] = str(e)
        _analyses[analysis_id]["status"] = "failed"

        await queue.put(
            AgentMessage(
                analysis_id=analysis_id,
                agent_id="system",
                agent_name="System",
                message_type=AgentMessageType.ERROR,
                content=f"Analysis failed: {str(e)}",
            )
        )

    finally:
        # Signal end of stream
        await queue.put(None)


@router.get("/stream/{analysis_id}")
async def stream_analysis(analysis_id: str) -> EventSourceResponse:
    """
    Stream analysis messages via Server-Sent Events.

    Each event contains an AgentMessage with the agent's thoughts or conclusions.
    """
    if analysis_id not in _analyses:
        raise HTTPException(status_code=404, detail="Analysis not found")

    async def event_generator() -> AsyncGenerator[dict, None]:
        queue = _message_queues.get(analysis_id)
        if not queue:
            return

        while True:
            try:
                message = await asyncio.wait_for(
                    queue.get(), timeout=300
                )  # 5 min timeout

                if message is None:
                    # End of stream
                    yield {
                        "event": "complete",
                        "data": '{"status": "completed"}',
                    }
                    break

                yield {
                    "event": "message",
                    "data": message.model_dump_json(),
                }

            except asyncio.TimeoutError:
                yield {
                    "event": "timeout",
                    "data": '{"status": "timeout"}',
                }
                break

    return EventSourceResponse(event_generator())


@router.get("/history", response_model=list[AnalysisHistoryItem])
async def get_history() -> list[AnalysisHistoryItem]:
    """Get history of past analyses."""
    # For demo, return completed analyses from memory
    # In production, this would query a database
    history = []
    for analysis_id, data in _analyses.items():
        if data["status"] == "completed":
            history.append(
                AnalysisHistoryItem(
                    analysis_id=analysis_id,
                    ticker=data["ticker"],
                    recommendation="hold",  # Would parse from result
                    confidence="medium",  # Would parse from result
                    timestamp=data["started_at"],
                )
            )
    return history


@router.get("/analysis/{analysis_id}")
async def get_analysis(analysis_id: str) -> dict:
    """Get the status and result of an analysis."""
    if analysis_id not in _analyses:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return _analyses[analysis_id]
