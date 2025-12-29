'use client';

import { useState, useMemo } from 'react';
import { startAnalysis } from '@/lib/api';
import { useAnalysisStream } from '@/hooks/useAnalysisStream';
import TickerInput from '@/components/TickerInput';
import AgentPanel from '@/components/AgentPanel';
import ConversationStream from '@/components/ConversationStream';
import ResultsPanel from '@/components/ResultsPanel';
import { ConsensusReport } from '@/types';
import { Activity } from 'lucide-react';

export default function Home() {
  const [streamUrl, setStreamUrl] = useState<string | null>(null);
  const [isInitializing, setIsInitializing] = useState(false);
  
  const { messages, agentStates, isConnected, error } = useAnalysisStream(streamUrl);

  const handleAnalyze = async (ticker: string) => {
    try {
      setIsInitializing(true);
      const response = await startAnalysis(ticker);
      setStreamUrl(response.stream_url);
    } catch (err) {
      console.error('Failed to start analysis:', err);
      alert('Failed to start analysis. Please check backend connection.');
    } finally {
      setIsInitializing(false);
    }
  };

  const finalReport = useMemo(() => {
    const conclusionMsg = messages.find(m => m.message_type === 'conclusion');
    if (conclusionMsg?.metadata) {
      return conclusionMsg.metadata as ConsensusReport;
    }
    return null;
  }, [messages]);

  return (
    <main className="flex h-screen w-full flex-col overflow-hidden bg-background relative selection:bg-gold-muted selection:text-white">
      
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 border-b border-gold-muted/20 bg-bg-card z-10 shadow-[0_4px_20px_-10px_rgba(0,0,0,0.5)]">
        <div className="flex items-center gap-4">
          <div className="p-2 border border-gold-primary bg-bg-elevated sharp-corners">
            <Activity className="w-6 h-6 text-gold-primary" />
          </div>
          <div>
            <h1 className="text-3xl font-headline tracking-widest text-gold-primary leading-none mb-1">THE TRADING FLOOR</h1>
            <p className="text-xs text-gold-muted font-mono tracking-wider uppercase">Multi-Agent Market Analysis Council</p>
          </div>
        </div>
        <div className="flex items-center gap-6 font-mono text-xs">
          <div className="flex items-center gap-2 px-3 py-1 border border-gold-muted/20 bg-bg-elevated sharp-corners text-gold-muted">
            <div className={`w-1.5 h-1.5 rounded-full ${isConnected ? 'bg-gold-bright animate-pulse' : 'bg-red-900'}`} />
            {isConnected ? 'LIVE FEED ACTIVE' : 'SYSTEM IDLE'}
          </div>
          <div className="text-text-muted">
             {new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }).toUpperCase()}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar - Board of Directors */}
        <div className="w-80 border-r border-gold-muted/20 bg-bg-elevated/50 flex flex-col">
            <div className="p-4 border-b border-gold-muted/10">
                <h2 className="font-headline text-xl text-gold-muted tracking-wider">Board of Directors</h2>
            </div>
            <AgentPanel agentStates={agentStates} />
        </div>

        {/* Center Panel */}
        <div className="flex-1 flex flex-col min-w-0 bg-bg-primary relative">
            
            {/* Ticker Input Bar */}
            <div className="p-6 border-b border-gold-muted/20 bg-bg-card/30">
                <TickerInput onAnalyze={handleAnalyze} isLoading={isInitializing} />
            </div>

            {/* Error Display */}
            {error && (
                <div className="mx-6 mt-4 p-4 sharp-corners bg-red-900/10 border-l-2 border-orange-warning text-orange-warning font-mono text-sm">
                    <span className="font-bold">SYSTEM ERROR:</span> {error}
                </div>
            )}

            {/* Content Area */}
            <div className="flex-1 flex flex-col min-h-0 relative p-6 gap-6">
                
                {/* Stream */}
                <div className="flex-1 overflow-hidden flex flex-col bg-bg-card border border-gold-muted/10 sharp-corners relative">
                    <div className="absolute top-0 right-0 p-2 opacity-20 pointer-events-none">
                        <Activity className="w-32 h-32 text-gold-muted" />
                    </div>
                    <ConversationStream messages={messages} />
                </div>
                
                {/* Results Panel Overlay */}
                {finalReport && (
                    <div className="animate-in slide-in-from-bottom-10 fade-in duration-500 z-20">
                        <ResultsPanel report={finalReport} />
                    </div>
                )}
            </div>
        </div>
      </div>
    </main>
  );
}
