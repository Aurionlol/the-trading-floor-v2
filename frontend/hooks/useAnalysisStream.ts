import { useState, useEffect, useRef } from 'react';
import { AgentMessage, AgentState } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function useAnalysisStream(streamUrl: string | null) {
  const [messages, setMessages] = useState<AgentMessage[]>([]);
  const [agentStates, setAgentStates] = useState<Record<string, AgentState['status']>>({});
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!streamUrl) return;

    // Reset state for new analysis
    setMessages([]);
    setAgentStates({});
    setError(null);

    const eventSource = new EventSource(`${API_BASE_URL}${streamUrl}`);
    eventSourceRef.current = eventSource;
    setIsConnected(true);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as AgentMessage;
        
        setMessages((prev) => [...prev, data]);
        
        // Update agent status based on message
        // If message is 'thinking', set that agent to thinking
        // If message is 'analysis' or 'debate', set that agent to done (or active depending on UX)
        // For now: 'thinking' -> thinking, anything else -> done (but 'active' might be better)
        // Let's assume sequential: one starts thinking -> thinking. Then produces analysis -> done.
        
        setAgentStates((prev) => {
             const newStates = { ...prev };
             
             // If this agent is thinking, mark them as thinking
             if (data.message_type === 'thinking') {
                 // Reset others to idle/done if needed, or just set this one
                 newStates[data.agent_id] = 'thinking';
             } else {
                 // They produced content, mark as done
                 newStates[data.agent_id] = 'done';
             }
             return newStates;
        });

        if (data.message_type === 'conclusion') {
            eventSource.close();
            setIsConnected(false);
        }

      } catch (err) {
        console.error('Error parsing SSE message:', err);
      }
    };

    eventSource.onerror = (err) => {
      console.error('SSE Error:', err);
      setError('Connection lost');
      eventSource.close();
      setIsConnected(false);
    };

    return () => {
      eventSource.close();
    };
  }, [streamUrl]);

  return { messages, agentStates, isConnected, error };
}
