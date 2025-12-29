"""Trading crew configuration with hierarchical process."""

from crewai import Crew, Process, Task

from backend.agents import (
    get_macro_strategist,
    get_portfolio_chief,
    get_quant_analyst,
    get_risk_manager,
    get_sentiment_scout,
)


def create_trading_crew(ticker: str, context: str | None = None) -> Crew:
    """
    Create a trading analysis crew for the given ticker.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL")
        context: Optional additional context for the analysis

    Returns:
        Configured Crew ready for execution
    """
    # Get agent instances (lazily created)
    quant_analyst = get_quant_analyst()
    sentiment_scout = get_sentiment_scout()
    macro_strategist = get_macro_strategist()
    risk_manager = get_risk_manager()
    portfolio_chief = get_portfolio_chief()

    context_str = f"\nAdditional context: {context}" if context else ""

    # Task 1: Technical Analysis (Quant Analyst)
    technical_analysis_task = Task(
        description=(
            f"Perform comprehensive technical analysis for {ticker}.{context_str}\n\n"
            "Your analysis must include:\n"
            "1. Current price action and trend direction\n"
            "2. Key moving averages (20, 50, 200 SMA) and price position relative to them\n"
            "3. RSI reading and interpretation (overbought/oversold/neutral)\n"
            "4. MACD signal and momentum direction\n"
            "5. Bollinger Band position and volatility assessment\n"
            "6. Key support and resistance levels\n"
            "7. Any chart patterns identified\n"
            "8. Volume analysis and confirmation\n\n"
            "Conclude with a technical score (0-100) and confidence level (low/medium/high)."
        ),
        expected_output=(
            "A detailed technical analysis report containing:\n"
            "- Technical Score (0-100)\n"
            "- Confidence Level (low/medium/high)\n"
            "- Key indicator readings with specific values\n"
            "- Support levels (list of prices)\n"
            "- Resistance levels (list of prices)\n"
            "- Patterns identified\n"
            "- Primary concerns or caveats\n"
            "- Clear bullish/bearish/neutral conclusion with reasoning"
        ),
        agent=quant_analyst,
    )

    # Task 2: Sentiment Analysis (Sentiment Scout)
    sentiment_analysis_task = Task(
        description=(
            f"Analyze market sentiment for {ticker}.{context_str}\n\n"
            "Your analysis must include:\n"
            "1. Volume analysis - are we seeing unusual volume? What does it indicate?\n"
            "2. Recent price action context - panic selling, euphoric buying, or orderly?\n"
            "3. Volatility patterns - is fear elevated or complacency present?\n"
            "4. Any contrarian signals - is the crowd too bullish or too bearish?\n"
            "5. What's the current narrative around this stock?\n"
            "6. Are there signs of capitulation or exhaustion?\n\n"
            "Conclude with a sentiment score (0-100) and confidence level (low/medium/high)."
        ),
        expected_output=(
            "A sentiment analysis report containing:\n"
            "- Sentiment Score (0-100, where 50 is neutral, >50 is bullish)\n"
            "- Confidence Level (low/medium/high)\n"
            "- Narrative summary (2-3 sentences on current market story)\n"
            "- Volume analysis findings\n"
            "- Any contrarian signals identified\n"
            "- Key evidence supporting the sentiment assessment\n"
            "- Primary concerns or caveats"
        ),
        agent=sentiment_scout,
    )

    # Task 3: Macro Analysis (Macro Strategist)
    macro_analysis_task = Task(
        description=(
            f"Analyze macroeconomic context and sector dynamics for {ticker}.{context_str}\n\n"
            "Your analysis must include:\n"
            "1. Company's sector and industry classification\n"
            "2. Sector performance vs. major indices (SPY, QQQ)\n"
            "3. Stock's relative performance vs. sector ETF\n"
            "4. Correlation to major asset classes (stocks, bonds, gold)\n"
            "5. Current market regime (risk-on, risk-off, etc.)\n"
            "6. Any macro tailwinds or headwinds affecting the stock\n"
            "7. Sector rotation signals - is this sector in favor?\n\n"
            "Conclude with a macro alignment score (0-100) and confidence level."
        ),
        expected_output=(
            "A macro analysis report containing:\n"
            "- Macro Alignment Score (0-100)\n"
            "- Confidence Level (low/medium/high)\n"
            "- Sector outlook assessment\n"
            "- Relative performance vs. sector and indices\n"
            "- Intermarket signals identified\n"
            "- Current regime assessment\n"
            "- Key evidence with specific performance numbers\n"
            "- Primary concerns or caveats"
        ),
        agent=macro_strategist,
    )

    # Task 4: Risk Assessment (Risk Manager)
    risk_analysis_task = Task(
        description=(
            f"Perform risk assessment for {ticker}.{context_str}\n\n"
            "Your analysis must include:\n"
            "1. Current and historical volatility metrics\n"
            "2. Maximum drawdown analysis - worst historical losses and recovery times\n"
            "3. Current drawdown status - how far from highs?\n"
            "4. Correlation risks - how correlated to broad market?\n"
            "5. Position sizing recommendation based on volatility\n"
            "6. Suggested stop-loss level with rationale\n"
            "7. Key risks that could cause the investment to fail\n"
            "8. Conditions that would invalidate any bullish thesis\n\n"
            "Conclude with a risk score (0-100, where higher = lower risk) and position size recommendation."
        ),
        expected_output=(
            "A risk assessment report containing:\n"
            "- Risk Score (0-100, higher = lower risk/more favorable)\n"
            "- Confidence Level (low/medium/high)\n"
            "- Position Size Recommendation (as % of portfolio)\n"
            "- Volatility metrics (daily, annualized, vs. SPY)\n"
            "- Maximum drawdown data with dates\n"
            "- Stop-loss level recommendation\n"
            "- Correlation risks identified\n"
            "- Key risk factors (list)\n"
            "- Invalidation criteria (list of conditions that would negate the thesis)"
        ),
        agent=risk_manager,
    )

    # Task 5: Synthesis (Portfolio Chief)
    synthesis_task = Task(
        description=(
            f"Synthesize all specialist analyses for {ticker} and provide final recommendation.{context_str}\n\n"
            "You have received analyses from:\n"
            "1. Quant Analyst - Technical analysis\n"
            "2. Sentiment Scout - Sentiment analysis\n"
            "3. Macro Strategist - Macro and sector analysis\n"
            "4. Risk Manager - Risk assessment\n\n"
            "Your synthesis must:\n"
            "1. Review each specialist's score and key findings\n"
            "2. Identify where specialists agree (strengthens conviction)\n"
            "3. Identify where specialists disagree (requires your judgment)\n"
            "4. Resolve any conflicts with clear reasoning\n"
            "5. Weight the evidence appropriately for current conditions\n"
            "6. Deliver a final recommendation with confidence level\n"
            "7. Specify position size (validate with Risk Manager's input)\n"
            "8. Define what would change your view\n\n"
            "Be decisive but honest about uncertainty. Not every situation is a clear buy or sell."
        ),
        expected_output=(
            "A comprehensive consensus report containing:\n"
            "- Final Recommendation: [strong_buy / buy / hold / sell / strong_sell]\n"
            "- Confidence Level: [low / medium / high]\n"
            "- Agent Scores Summary:\n"
            "  - Quant Analyst: [score] - [one-line rationale]\n"
            "  - Sentiment Scout: [score] - [one-line rationale]\n"
            "  - Macro Strategist: [score] - [one-line rationale]\n"
            "  - Risk Manager: [score] - [one-line rationale]\n"
            "- Key Agreements: [list of points where agents agree]\n"
            "- Key Disagreements: [list of points where agents disagree]\n"
            "- How Disagreements Were Resolved: [explanation]\n"
            "- Position Size: [X]% of portfolio\n"
            "- Key Risk Factors: [list]\n"
            "- Invalidation Criteria: [conditions that would change the view]\n"
            "- Executive Summary: [2-3 paragraph synthesis explaining the recommendation]"
        ),
        agent=portfolio_chief,
        context=[
            technical_analysis_task,
            sentiment_analysis_task,
            macro_analysis_task,
            risk_analysis_task,
        ],
    )

    # Create the crew with sequential process
    crew = Crew(
        agents=[
            portfolio_chief,
            quant_analyst,
            sentiment_scout,
            macro_strategist,
            risk_manager,
        ],
        tasks=[
            technical_analysis_task,
            sentiment_analysis_task,
            macro_analysis_task,
            risk_analysis_task,
            synthesis_task,
        ],
        process=Process.sequential,  # Run specialist tasks first, then synthesis
        verbose=True,
        memory=True,
        planning=True,
    )

    return crew


def run_analysis(ticker: str, context: str | None = None) -> str:
    """
    Run a complete trading analysis for the given ticker.

    Args:
        ticker: Stock ticker symbol
        context: Optional additional analysis context

    Returns:
        The final consensus report as a string
    """
    crew = create_trading_crew(ticker, context)
    result = crew.kickoff(inputs={"ticker": ticker})
    return result.raw
