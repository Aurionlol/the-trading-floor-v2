"""Market data tools wrapping yfinance functionality."""

from typing import Type

import pandas as pd
import yfinance as yf
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class TickerInput(BaseModel):
    """Input schema for single ticker tools."""

    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, MSFT)")


class PriceHistoryInput(BaseModel):
    """Input schema for price history tool."""

    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, MSFT)")
    period: str = Field(
        default="3mo",
        description="Time period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max",
    )
    interval: str = Field(
        default="1d",
        description="Data interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo",
    )


class PriceHistoryTool(BaseTool):
    """Fetches historical OHLCV price data for a ticker."""

    name: str = "Price History"
    description: str = (
        "Retrieves historical Open, High, Low, Close, Volume (OHLCV) data for a stock. "
        "Use this to analyze price trends, identify patterns, and calculate technical indicators. "
        "Returns data as a formatted table with dates and price information."
    )
    args_schema: Type[BaseModel] = PriceHistoryInput

    def _run(self, ticker: str, period: str = "3mo", interval: str = "1d") -> str:
        """Fetch price history for the given ticker."""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period, interval=interval)

            if hist.empty:
                return f"No price data found for {ticker}. Please verify the ticker symbol."

            # Format for readability
            hist = hist.round(2)
            hist.index = hist.index.strftime("%Y-%m-%d")

            summary = (
                f"Price History for {ticker.upper()} ({period}, {interval} intervals)\n"
            )
            summary += "=" * 60 + "\n"
            summary += f"Latest Close: ${hist['Close'].iloc[-1]:.2f}\n"
            summary += f"Period High: ${hist['High'].max():.2f}\n"
            summary += f"Period Low: ${hist['Low'].min():.2f}\n"
            summary += f"Avg Volume: {hist['Volume'].mean():,.0f}\n"
            summary += "=" * 60 + "\n\n"
            summary += "Recent Data (last 10 rows):\n"
            summary += hist.tail(10).to_string()

            return summary

        except Exception as e:
            return f"Error fetching price history for {ticker}: {str(e)}"


class FundamentalsTool(BaseTool):
    """Fetches fundamental financial metrics and ratios."""

    name: str = "Fundamentals"
    description: str = (
        "Retrieves key fundamental data including P/E ratio, market cap, revenue, "
        "earnings, profit margins, and other financial metrics. Use this to assess "
        "the financial health and valuation of a company."
    )
    args_schema: Type[BaseModel] = TickerInput

    def _run(self, ticker: str) -> str:
        """Fetch fundamental data for the given ticker."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            if not info or "regularMarketPrice" not in info:
                return f"No fundamental data found for {ticker}. Please verify the ticker symbol."

            # Extract key metrics
            metrics = {
                "Company Name": info.get("longName", "N/A"),
                "Sector": info.get("sector", "N/A"),
                "Industry": info.get("industry", "N/A"),
                "Market Cap": f"${info.get('marketCap', 0):,.0f}"
                if info.get("marketCap")
                else "N/A",
                "Current Price": f"${info.get('regularMarketPrice', 0):.2f}",
                "52 Week High": f"${info.get('fiftyTwoWeekHigh', 0):.2f}",
                "52 Week Low": f"${info.get('fiftyTwoWeekLow', 0):.2f}",
                "P/E Ratio (Trailing)": f"{info.get('trailingPE', 'N/A'):.2f}"
                if info.get("trailingPE")
                else "N/A",
                "P/E Ratio (Forward)": f"{info.get('forwardPE', 'N/A'):.2f}"
                if info.get("forwardPE")
                else "N/A",
                "PEG Ratio": f"{info.get('pegRatio', 'N/A'):.2f}"
                if info.get("pegRatio")
                else "N/A",
                "Price to Book": f"{info.get('priceToBook', 'N/A'):.2f}"
                if info.get("priceToBook")
                else "N/A",
                "EPS (TTM)": f"${info.get('trailingEps', 'N/A'):.2f}"
                if info.get("trailingEps")
                else "N/A",
                "Revenue (TTM)": f"${info.get('totalRevenue', 0):,.0f}"
                if info.get("totalRevenue")
                else "N/A",
                "Gross Margin": f"{info.get('grossMargins', 0) * 100:.1f}%"
                if info.get("grossMargins")
                else "N/A",
                "Operating Margin": f"{info.get('operatingMargins', 0) * 100:.1f}%"
                if info.get("operatingMargins")
                else "N/A",
                "Profit Margin": f"{info.get('profitMargins', 0) * 100:.1f}%"
                if info.get("profitMargins")
                else "N/A",
                "ROE": f"{info.get('returnOnEquity', 0) * 100:.1f}%"
                if info.get("returnOnEquity")
                else "N/A",
                "Debt to Equity": f"{info.get('debtToEquity', 'N/A'):.2f}"
                if info.get("debtToEquity")
                else "N/A",
                "Dividend Yield": f"{info.get('dividendYield', 0) * 100:.2f}%"
                if info.get("dividendYield")
                else "N/A",
                "Beta": f"{info.get('beta', 'N/A'):.2f}" if info.get("beta") else "N/A",
            }

            result = f"Fundamental Analysis for {ticker.upper()}\n"
            result += "=" * 50 + "\n"
            for key, value in metrics.items():
                result += f"{key}: {value}\n"

            return result

        except Exception as e:
            return f"Error fetching fundamentals for {ticker}: {str(e)}"


class TechnicalIndicatorsTool(BaseTool):
    """Calculates common technical indicators."""

    name: str = "Technical Indicators"
    description: str = (
        "Calculates technical indicators including RSI, MACD, Bollinger Bands, "
        "moving averages (SMA/EMA), and volume analysis. Use this to identify "
        "momentum, trend direction, and potential reversal signals."
    )
    args_schema: Type[BaseModel] = TickerInput

    def _run(self, ticker: str) -> str:
        """Calculate technical indicators for the given ticker."""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="6mo", interval="1d")

            if hist.empty or len(hist) < 50:
                return f"Insufficient data to calculate indicators for {ticker}."

            close = hist["Close"]
            high = hist["High"]
            low = hist["Low"]
            volume = hist["Volume"]

            # Moving Averages
            sma_20 = close.rolling(window=20).mean().iloc[-1]
            sma_50 = close.rolling(window=50).mean().iloc[-1]
            sma_200 = (
                close.rolling(window=200).mean().iloc[-1] if len(close) >= 200 else None
            )
            ema_12 = close.ewm(span=12, adjust=False).mean().iloc[-1]
            ema_26 = close.ewm(span=26, adjust=False).mean().iloc[-1]

            # RSI (14-period)
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs)).iloc[-1]

            # MACD
            macd_line = ema_12 - ema_26
            signal_line = close.ewm(span=9, adjust=False).mean().iloc[-1]
            macd_histogram = macd_line - signal_line

            # Bollinger Bands (20-period, 2 std)
            bb_middle = sma_20
            bb_std = close.rolling(window=20).std().iloc[-1]
            bb_upper = bb_middle + (2 * bb_std)
            bb_lower = bb_middle - (2 * bb_std)

            # Volume analysis
            avg_volume_20 = volume.rolling(window=20).mean().iloc[-1]
            current_volume = volume.iloc[-1]
            volume_ratio = current_volume / avg_volume_20

            # Price position
            current_price = close.iloc[-1]

            result = f"Technical Indicators for {ticker.upper()}\n"
            result += "=" * 50 + "\n\n"

            result += "PRICE & MOVING AVERAGES\n"
            result += "-" * 30 + "\n"
            result += f"Current Price: ${current_price:.2f}\n"
            result += f"SMA 20: ${sma_20:.2f} ({'above' if current_price > sma_20 else 'below'})\n"
            result += f"SMA 50: ${sma_50:.2f} ({'above' if current_price > sma_50 else 'below'})\n"
            if sma_200:
                result += f"SMA 200: ${sma_200:.2f} ({'above' if current_price > sma_200 else 'below'})\n"
            result += f"EMA 12: ${ema_12:.2f}\n"
            result += f"EMA 26: ${ema_26:.2f}\n\n"

            result += "MOMENTUM INDICATORS\n"
            result += "-" * 30 + "\n"
            result += f"RSI (14): {rsi:.1f}"
            if rsi > 70:
                result += " (OVERBOUGHT)\n"
            elif rsi < 30:
                result += " (OVERSOLD)\n"
            else:
                result += " (NEUTRAL)\n"

            result += f"MACD Line: {macd_line:.4f}\n"
            result += f"MACD Histogram: {macd_histogram:.4f}"
            result += f" ({'BULLISH' if macd_histogram > 0 else 'BEARISH'})\n\n"

            result += "BOLLINGER BANDS (20, 2)\n"
            result += "-" * 30 + "\n"
            result += f"Upper Band: ${bb_upper:.2f}\n"
            result += f"Middle Band: ${bb_middle:.2f}\n"
            result += f"Lower Band: ${bb_lower:.2f}\n"
            bb_position = ((current_price - bb_lower) / (bb_upper - bb_lower)) * 100
            result += f"Price Position: {bb_position:.1f}% (0=lower, 100=upper)\n\n"

            result += "VOLUME ANALYSIS\n"
            result += "-" * 30 + "\n"
            result += f"Current Volume: {current_volume:,.0f}\n"
            result += f"20-Day Avg Volume: {avg_volume_20:,.0f}\n"
            result += f"Volume Ratio: {volume_ratio:.2f}x"
            if volume_ratio > 1.5:
                result += " (HIGH)\n"
            elif volume_ratio < 0.5:
                result += " (LOW)\n"
            else:
                result += " (NORMAL)\n"

            return result

        except Exception as e:
            return f"Error calculating indicators for {ticker}: {str(e)}"


class SectorPerformanceInput(BaseModel):
    """Input schema for sector performance tool."""

    ticker: str = Field(
        ..., description="Stock ticker symbol to compare against sectors"
    )
    period: str = Field(
        default="1mo", description="Comparison period: 1d, 5d, 1mo, 3mo, 6mo, 1y"
    )


class SectorPerformanceTool(BaseTool):
    """Compares performance across sectors and major indices."""

    name: str = "Sector Performance"
    description: str = (
        "Compares a stock's performance against its sector, major indices (SPY, QQQ, DIA), "
        "and sector ETFs. Use this to understand relative strength and sector dynamics."
    )
    args_schema: Type[BaseModel] = SectorPerformanceInput

    def _run(self, ticker: str, period: str = "1mo") -> str:
        """Compare sector and index performance."""
        try:
            # Major indices and sector ETFs
            benchmarks = {
                "SPY": "S&P 500",
                "QQQ": "NASDAQ 100",
                "DIA": "Dow Jones",
                "XLK": "Technology",
                "XLF": "Financials",
                "XLE": "Energy",
                "XLV": "Healthcare",
                "XLI": "Industrials",
                "XLC": "Communication",
                "XLY": "Consumer Discretionary",
                "XLP": "Consumer Staples",
                "XLB": "Materials",
                "XLU": "Utilities",
                "XLRE": "Real Estate",
            }

            # Get target stock data
            target_stock = yf.Ticker(ticker)
            target_hist = target_stock.history(period=period)

            if target_hist.empty:
                return f"No data found for {ticker}."

            target_return = (
                (target_hist["Close"].iloc[-1] / target_hist["Close"].iloc[0]) - 1
            ) * 100
            target_info = target_stock.info
            target_sector = target_info.get("sector", "Unknown")

            result = f"Sector & Index Performance Comparison for {ticker.upper()}\n"
            result += f"Period: {period}\n"
            result += f"Sector: {target_sector}\n"
            result += "=" * 60 + "\n\n"

            result += f"{ticker.upper()} Return: {target_return:+.2f}%\n\n"

            result += "MAJOR INDICES\n"
            result += "-" * 40 + "\n"

            performances = []
            for symbol, name in benchmarks.items():
                try:
                    bench = yf.Ticker(symbol)
                    bench_hist = bench.history(period=period)
                    if not bench_hist.empty:
                        bench_return = (
                            (bench_hist["Close"].iloc[-1] / bench_hist["Close"].iloc[0])
                            - 1
                        ) * 100
                        performances.append((symbol, name, bench_return))
                except Exception:
                    continue

            # Sort by performance
            performances.sort(key=lambda x: x[2], reverse=True)

            indices = [p for p in performances if p[0] in ["SPY", "QQQ", "DIA"]]
            sectors = [p for p in performances if p[0] not in ["SPY", "QQQ", "DIA"]]

            for symbol, name, ret in indices:
                relative = target_return - ret
                result += (
                    f"{name} ({symbol}): {ret:+.2f}% | Relative: {relative:+.2f}%\n"
                )

            result += "\nSECTOR ETFs (Ranked by Performance)\n"
            result += "-" * 40 + "\n"

            for symbol, name, ret in sectors:
                relative = target_return - ret
                marker = (
                    " <-- Stock's Sector"
                    if name.lower() in target_sector.lower()
                    else ""
                )
                result += f"{name} ({symbol}): {ret:+.2f}% | Relative: {relative:+.2f}%{marker}\n"

            # Summary
            avg_index_return = (
                sum(p[2] for p in indices) / len(indices) if indices else 0
            )
            result += "\nSUMMARY\n"
            result += "-" * 40 + "\n"
            result += f"Outperforming SPY: {'Yes' if target_return > [p[2] for p in indices if p[0] == 'SPY'][0] else 'No'}\n"
            result += (
                f"Relative to Index Avg: {target_return - avg_index_return:+.2f}%\n"
            )

            return result

        except Exception as e:
            return f"Error comparing sector performance for {ticker}: {str(e)}"
