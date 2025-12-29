import { AnalysisRequest, AnalysisResponse, Agent } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function getAgents(): Promise<Agent[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/agents`);
    if (!response.ok) {
      throw new Error("Failed to fetch agents");
    }
    return response.json();
  } catch (error) {
    console.error("Error fetching agents:", error);
    // Return default agents if API fails for UI dev purposes
    return [
      { id: "quant", name: "Quant Analyst", role: "Quantitative Analysis", description: "Technical patterns and indicators" },
      { id: "sentiment", name: "Sentiment Scout", role: "Sentiment Analysis", description: "Market sentiment and news" },
      { id: "macro", name: "Macro Strategist", role: "Macro Economics", description: "Global economic context" },
      { id: "risk", name: "Risk Manager", role: "Risk Management", description: "Position sizing and downside" },
      { id: "portfolio", name: "Portfolio Chief", role: "Strategy", description: "Final decision maker" },
    ];
  }
}

export async function startAnalysis(ticker: string, context?: string): Promise<AnalysisResponse> {
  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ticker, context }),
  });

  if (!response.ok) {
    throw new Error("Failed to start analysis");
  }

  return response.json();
}
