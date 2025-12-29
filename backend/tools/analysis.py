"""Analysis tools for risk and correlation calculations."""

from typing import Type

import numpy as np
import pandas as pd
import yfinance as yf
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class CorrelationInput(BaseModel):
    """Input schema for correlation tool."""

    ticker: str = Field(..., description="Primary stock ticker symbol")
    compare_tickers: str = Field(
        default="SPY,QQQ,TLT,GLD",
        description="Comma-separated list of tickers to compare correlation against",
    )
    period: str = Field(default="1y", description="Period for correlation calculation")


class CorrelationTool(BaseTool):
    """Computes correlation between assets."""

    name: str = "Correlation Calculator"
    description: str = (
        "Calculates correlation coefficients between a stock and other assets. "
        "Use this to identify diversification opportunities and understand "
        "how the stock moves relative to indices, bonds, and commodities."
    )
    args_schema: Type[BaseModel] = CorrelationInput

    def _run(
        self, ticker: str, compare_tickers: str = "SPY,QQQ,TLT,GLD", period: str = "1y"
    ) -> str:
        """Calculate correlations between ticker and comparison assets."""
        try:
            tickers_list = [t.strip().upper() for t in compare_tickers.split(",")]
            all_tickers = [ticker.upper()] + tickers_list

            # Download all data
            data = yf.download(
                all_tickers, period=period, interval="1d", progress=False
            )["Close"]

            if data.empty:
                return f"No data found for the specified tickers."

            # Calculate daily returns
            returns = data.pct_change().dropna()

            if returns.empty or len(returns) < 20:
                return "Insufficient data to calculate meaningful correlations."

            # Calculate correlation matrix
            corr_matrix = returns.corr()

            # Get correlations with the target ticker
            target_corr = corr_matrix[ticker.upper()].drop(ticker.upper())

            result = f"Correlation Analysis for {ticker.upper()}\n"
            result += f"Period: {period} ({len(returns)} trading days)\n"
            result += "=" * 50 + "\n\n"

            result += "CORRELATIONS WITH TARGET STOCK\n"
            result += "-" * 40 + "\n"

            # Sort by absolute correlation
            sorted_corr = target_corr.sort_values(key=abs, ascending=False)

            for comp_ticker, corr_value in sorted_corr.items():
                if corr_value > 0.7:
                    strength = "STRONG POSITIVE"
                elif corr_value > 0.3:
                    strength = "MODERATE POSITIVE"
                elif corr_value > -0.3:
                    strength = "LOW/NONE"
                elif corr_value > -0.7:
                    strength = "MODERATE NEGATIVE"
                else:
                    strength = "STRONG NEGATIVE"

                result += f"{comp_ticker}: {corr_value:.3f} ({strength})\n"

            result += "\nINTERPRETATION\n"
            result += "-" * 40 + "\n"

            # SPY correlation interpretation
            if "SPY" in sorted_corr.index:
                spy_corr = sorted_corr["SPY"]
                if spy_corr > 0.8:
                    result += (
                        "- Highly correlated with market (systematic risk dominant)\n"
                    )
                elif spy_corr > 0.5:
                    result += "- Moderately correlated with market\n"
                else:
                    result += "- Low market correlation (potential diversifier)\n"

            # Bond correlation
            if "TLT" in sorted_corr.index:
                tlt_corr = sorted_corr["TLT"]
                if tlt_corr < -0.3:
                    result += "- Negative bond correlation (typical equity behavior)\n"
                elif tlt_corr > 0.3:
                    result += "- Positive bond correlation (unusual, investigate)\n"

            # Gold correlation
            if "GLD" in sorted_corr.index:
                gld_corr = sorted_corr["GLD"]
                if gld_corr < 0:
                    result += "- Negative gold correlation (risk-on behavior)\n"
                elif gld_corr > 0.3:
                    result += (
                        "- Positive gold correlation (defensive characteristics)\n"
                    )

            return result

        except Exception as e:
            return f"Error calculating correlations: {str(e)}"


class VolatilityInput(BaseModel):
    """Input schema for volatility tool."""

    ticker: str = Field(..., description="Stock ticker symbol")
    period: str = Field(default="1y", description="Period for volatility calculation")


class VolatilityTool(BaseTool):
    """Calculates historical volatility metrics."""

    name: str = "Volatility Analyzer"
    description: str = (
        "Calculates volatility metrics including historical volatility, "
        "average true range (ATR), and volatility comparison to benchmarks. "
        "Use this to assess risk and determine appropriate position sizing."
    )
    args_schema: Type[BaseModel] = VolatilityInput

    def _run(self, ticker: str, period: str = "1y") -> str:
        """Calculate volatility metrics for the given ticker."""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period, interval="1d")

            if hist.empty or len(hist) < 20:
                return f"Insufficient data to calculate volatility for {ticker}."

            close = hist["Close"]
            high = hist["High"]
            low = hist["Low"]

            # Daily returns
            returns = close.pct_change().dropna()

            # Historical volatility (annualized)
            daily_vol = returns.std()
            annual_vol = daily_vol * np.sqrt(252)

            # Rolling volatility (20-day)
            rolling_vol_20 = returns.rolling(window=20).std() * np.sqrt(252)
            current_rolling_vol = rolling_vol_20.iloc[-1]

            # Average True Range (14-period)
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr_14 = true_range.rolling(window=14).mean().iloc[-1]
            atr_pct = (atr_14 / close.iloc[-1]) * 100

            # Volatility regime comparison
            vol_percentile = (
                (rolling_vol_20 <= current_rolling_vol).sum()
                / len(rolling_vol_20)
                * 100
            )

            # Compare to SPY
            spy = yf.Ticker("SPY")
            spy_hist = spy.history(period=period, interval="1d")
            spy_returns = spy_hist["Close"].pct_change().dropna()
            spy_vol = spy_returns.std() * np.sqrt(252)

            beta = (
                returns.cov(spy_returns) / spy_returns.var()
                if len(spy_returns) > 0
                else None
            )

            result = f"Volatility Analysis for {ticker.upper()}\n"
            result += f"Period: {period} ({len(returns)} trading days)\n"
            result += "=" * 50 + "\n\n"

            result += "HISTORICAL VOLATILITY\n"
            result += "-" * 40 + "\n"
            result += f"Annualized Volatility: {annual_vol * 100:.1f}%\n"
            result += f"Daily Volatility: {daily_vol * 100:.2f}%\n"
            result += f"Current 20-Day Vol: {current_rolling_vol * 100:.1f}%\n"
            result += f"Volatility Percentile: {vol_percentile:.0f}%\n"

            if vol_percentile > 80:
                result += "Status: HIGH VOLATILITY REGIME\n"
            elif vol_percentile < 20:
                result += "Status: LOW VOLATILITY REGIME\n"
            else:
                result += "Status: NORMAL VOLATILITY\n"

            result += "\nAVERAGE TRUE RANGE\n"
            result += "-" * 40 + "\n"
            result += f"ATR (14-period): ${atr_14:.2f}\n"
            result += f"ATR as % of Price: {atr_pct:.2f}%\n"

            result += "\nMARKET COMPARISON\n"
            result += "-" * 40 + "\n"
            result += f"SPY Annualized Vol: {spy_vol * 100:.1f}%\n"
            result += f"Relative Volatility: {(annual_vol / spy_vol):.2f}x SPY\n"
            if beta is not None:
                result += f"Beta: {beta:.2f}\n"
                if beta > 1.2:
                    result += "Interpretation: High beta, amplifies market moves\n"
                elif beta < 0.8:
                    result += "Interpretation: Low beta, defensive characteristics\n"
                else:
                    result += "Interpretation: Market-like beta\n"

            result += "\nRISK METRICS\n"
            result += "-" * 40 + "\n"
            # Value at Risk (95% confidence, 1-day)
            var_95 = np.percentile(returns, 5)
            result += f"1-Day VaR (95%): {var_95 * 100:.2f}%\n"
            result += f"Expected Daily Range: ${close.iloc[-1] * daily_vol:.2f}\n"

            # Worst days
            worst_days = returns.nsmallest(5)
            result += "\nWorst 5 Days:\n"
            for date, ret in worst_days.items():
                result += f"  {date.strftime('%Y-%m-%d')}: {ret * 100:.2f}%\n"

            return result

        except Exception as e:
            return f"Error calculating volatility for {ticker}: {str(e)}"


class DrawdownInput(BaseModel):
    """Input schema for drawdown tool."""

    ticker: str = Field(..., description="Stock ticker symbol")
    period: str = Field(default="2y", description="Period for drawdown analysis")


class DrawdownTool(BaseTool):
    """Identifies historical drawdown periods and recovery times."""

    name: str = "Drawdown Analyzer"
    description: str = (
        "Analyzes historical drawdowns including maximum drawdown, current drawdown, "
        "average recovery time, and drawdown distribution. Use this to understand "
        "downside risk and historical stress periods."
    )
    args_schema: Type[BaseModel] = DrawdownInput

    def _run(self, ticker: str, period: str = "2y") -> str:
        """Analyze drawdowns for the given ticker."""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period, interval="1d")

            if hist.empty or len(hist) < 50:
                return f"Insufficient data to analyze drawdowns for {ticker}."

            close = hist["Close"]

            # Calculate running maximum
            running_max = close.cummax()

            # Calculate drawdown series
            drawdown = (close - running_max) / running_max

            # Current drawdown
            current_dd = drawdown.iloc[-1]

            # Maximum drawdown
            max_dd = drawdown.min()
            max_dd_date = drawdown.idxmin()

            # Find peak before max drawdown
            peak_before_max_dd = close.loc[:max_dd_date].idxmax()
            peak_value = close.loc[peak_before_max_dd]
            trough_value = close.loc[max_dd_date]

            # Check if recovered from max drawdown
            post_trough = close.loc[max_dd_date:]
            recovered = (post_trough >= peak_value).any()
            if recovered:
                recovery_date = post_trough[post_trough >= peak_value].index[0]
                recovery_days = (recovery_date - max_dd_date).days
            else:
                recovery_days = None

            # Drawdown statistics
            significant_dds = drawdown[drawdown < -0.05]  # >5% drawdowns

            result = f"Drawdown Analysis for {ticker.upper()}\n"
            result += f"Period: {period}\n"
            result += "=" * 50 + "\n\n"

            result += "CURRENT STATUS\n"
            result += "-" * 40 + "\n"
            result += f"Current Drawdown: {current_dd * 100:.1f}%\n"
            if current_dd < -0.1:
                result += "Status: SIGNIFICANT DRAWDOWN (>10%)\n"
            elif current_dd < -0.05:
                result += "Status: MODERATE DRAWDOWN (5-10%)\n"
            elif current_dd < -0.02:
                result += "Status: MINOR PULLBACK (2-5%)\n"
            else:
                result += "Status: NEAR ALL-TIME HIGH\n"

            result += "\nMAXIMUM DRAWDOWN\n"
            result += "-" * 40 + "\n"
            result += f"Max Drawdown: {max_dd * 100:.1f}%\n"
            result += f"Peak Date: {peak_before_max_dd.strftime('%Y-%m-%d')}\n"
            result += f"Peak Value: ${peak_value:.2f}\n"
            result += f"Trough Date: {max_dd_date.strftime('%Y-%m-%d')}\n"
            result += f"Trough Value: ${trough_value:.2f}\n"

            if recovery_days is not None:
                result += f"Recovery Time: {recovery_days} days\n"
                result += f"Recovery Date: {recovery_date.strftime('%Y-%m-%d')}\n"
            else:
                days_since_trough = (close.index[-1] - max_dd_date).days
                result += f"NOT YET RECOVERED ({days_since_trough} days since trough)\n"

            result += "\nDRAWDOWN DISTRIBUTION\n"
            result += "-" * 40 + "\n"
            result += f"Average Drawdown: {drawdown.mean() * 100:.1f}%\n"
            result += f"Median Drawdown: {drawdown.median() * 100:.1f}%\n"
            result += f"Time in Drawdown >5%: {(drawdown < -0.05).sum() / len(drawdown) * 100:.0f}%\n"
            result += f"Time in Drawdown >10%: {(drawdown < -0.10).sum() / len(drawdown) * 100:.0f}%\n"
            result += f"Time in Drawdown >20%: {(drawdown < -0.20).sum() / len(drawdown) * 100:.0f}%\n"

            # List significant drawdowns
            result += "\nSIGNIFICANT DRAWDOWNS (>10%)\n"
            result += "-" * 40 + "\n"

            # Find distinct drawdown periods
            in_drawdown = False
            drawdown_periods = []
            current_period_start = None
            current_period_min = 0

            for date, dd in drawdown.items():
                if dd < -0.10 and not in_drawdown:
                    in_drawdown = True
                    current_period_start = date
                    current_period_min = dd
                elif dd < -0.10 and in_drawdown:
                    current_period_min = min(current_period_min, dd)
                elif dd >= -0.05 and in_drawdown:
                    in_drawdown = False
                    drawdown_periods.append(
                        (current_period_start, date, current_period_min)
                    )

            if in_drawdown:
                drawdown_periods.append(
                    (current_period_start, close.index[-1], current_period_min)
                )

            if drawdown_periods:
                for start, end, min_dd in drawdown_periods[-5:]:  # Last 5
                    duration = (end - start).days
                    result += f"  {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}: {min_dd * 100:.1f}% ({duration} days)\n"
            else:
                result += "  No drawdowns >10% in this period\n"

            return result

        except Exception as e:
            return f"Error analyzing drawdowns for {ticker}: {str(e)}"
