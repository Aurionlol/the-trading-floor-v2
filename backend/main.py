"""Main entry point for the Trading Floor backend."""

import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Trading Floor API",
    description="Multi-agent market analysis council - A team of AI specialists analyzing financial instruments",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root() -> dict:
    """Root endpoint with API info."""
    return {
        "name": "Trading Floor API",
        "version": "0.1.0",
        "description": "Multi-agent market analysis council",
        "docs": "/docs",
        "endpoints": {
            "agents": "/api/agents",
            "analyze": "/api/analyze",
            "stream": "/api/stream/{analysis_id}",
            "history": "/api/history",
        },
    }


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


def main() -> None:
    """Run the server."""
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("RELOAD", "true").lower() == "true"

    uvicorn.run(
        "backend.main:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    main()
