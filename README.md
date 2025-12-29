# The Trading Floor

A multi-agent market analysis system where specialized AI agents collaborate and debate on financial instruments, simulating a hedge fund research team's decision-making process.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

The Trading Floor creates a visual council of AI agents, each with distinct expertise, that analyze financial instruments and produce consensus-based trading recommendations. Agents engage in structured debate, challenge each other's assumptions, and synthesize diverse perspectives into actionable insights.

### The Council Members

| Agent | Role | Focus |
|-------|------|-------|
| **Quant Analyst** | Technical Analysis | Price patterns, indicators, statistical signals |
| **Sentiment Scout** | Market Sentiment | News flow, crowd psychology, contrarian signals |
| **Macro Strategist** | Macroeconomic Context | Sector dynamics, intermarket relationships |
| **Risk Manager** | Risk Assessment | Position sizing, volatility, downside scenarios |
| **Portfolio Chief** | Final Decision | Synthesis, conflict resolution, recommendations |

## Features

- **Real-time Streaming**: Watch agents deliberate via Server-Sent Events
- **Multi-Agent Debate**: Agents challenge and build upon each other's analyses
- **Structured Output**: Consensus reports with individual scores and dissenting opinions
- **Modern UI**: Animated conversation panels with agent status indicators

## Tech Stack

### Backend
- **[CrewAI](https://www.crewai.com/)** - Agent orchestration
- **[FastAPI](https://fastapi.tiangolo.com/)** - REST API & SSE streaming
- **[yfinance](https://github.com/ranaroussi/yfinance)** - Market data
- **Python 3.11+**

### Frontend
- **[Next.js 14](https://nextjs.org/)** - React framework
- **[Tailwind CSS](https://tailwindcss.com/)** - Styling
- **[Framer Motion](https://www.framer.com/motion/)** - Animations
- **TypeScript**

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- [Bun](https://bun.sh/) (or npm/yarn)
- OpenAI API key (or Anthropic)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/CloudAI-X/the-trading-floor.git
   cd the-trading-floor
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **Install backend dependencies**
   ```bash
   uv sync
   ```

4. **Install frontend dependencies**
   ```bash
   cd frontend
   bun install
   ```

### Running the Application

1. **Start the backend** (from project root)
   ```bash
   uv run trading-floor
   ```
   The API will be available at `http://localhost:8000`

2. **Start the frontend** (in another terminal)
   ```bash
   cd frontend
   bun dev
   ```
   The UI will be available at `http://localhost:3000`

3. **Open your browser** and navigate to `http://localhost:3000`

## Configuration

### Backend Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for agent LLM | Yes* |
| `ANTHROPIC_API_KEY` | Anthropic API key (alternative) | Yes* |
| `HOST` | Backend host | No (default: `0.0.0.0`) |
| `PORT` | Backend port | No (default: `8000`) |
| `RELOAD` | Enable hot reload | No (default: `true`) |

*One of `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` is required.

### Frontend Environment Variables

Create `frontend/.env.local` for frontend configuration:

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | No (default: `http://localhost:8000`) |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/health` | Health check |
| `GET` | `/api/agents` | List all agents |
| `POST` | `/api/analyze` | Start analysis for a ticker |
| `GET` | `/api/stream/{id}` | SSE stream for analysis |
| `GET` | `/api/history` | Past analyses |
| `GET` | `/api/analysis/{id}` | Get analysis result |

### Example: Start Analysis

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'
```

## Project Structure

```
trading-floor/
├── backend/
│   ├── agents/           # Individual agent definitions
│   ├── crews/            # CrewAI crew configurations
│   ├── tools/            # Market data & analysis tools
│   ├── schemas/          # Pydantic models
│   ├── api/              # FastAPI routes
│   └── main.py           # Application entry point
├── frontend/
│   ├── app/              # Next.js app router
│   ├── components/       # React components
│   ├── hooks/            # Custom React hooks
│   ├── lib/              # Utilities & API client
│   └── types/            # TypeScript definitions
├── .env.example          # Environment template
├── pyproject.toml        # Python dependencies
└── README.md
```

## Development

### Backend Development

```bash
# Run with hot reload
uv run trading-floor

# Run tests
uv run pytest

# Type checking (if configured)
uv run mypy backend
```

### Frontend Development

```bash
cd frontend

# Development server
bun dev

# Lint
bun lint

# Build
bun build
```

## How It Works

1. **Input**: User submits a ticker symbol (e.g., "AAPL")
2. **Data Gathering**: Agents fetch relevant market data using yfinance
3. **Individual Analysis**: Each specialist produces their assessment
4. **Debate Phase**: Agents review and challenge each other's analyses
5. **Synthesis**: Portfolio Chief integrates all perspectives
6. **Output**: Structured report with recommendation and confidence level

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CrewAI](https://www.crewai.com/) for the agent orchestration framework
- [yfinance](https://github.com/ranaroussi/yfinance) for market data access
