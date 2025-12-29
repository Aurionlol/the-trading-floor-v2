import { AgentState } from '@/types';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';
import Image from 'next/image';

interface AgentPanelProps {
  agentStates: Record<string, AgentState['status']>;
}

const agents = [
  { id: 'quant', name: 'Quant Analyst', icon: '/icons/quant_analyst.webp' },
  { id: 'sentiment', name: 'Sentiment Scout', icon: '/icons/sentiment_scout.webp' },
  { id: 'macro', name: 'Macro Strategist', icon: '/icons/macro_strategiest.webp' },
  { id: 'risk', name: 'Risk Manager', icon: '/icons/risk_manager.webp' },
  { id: 'portfolio', name: 'Portfolio Chief', icon: '/icons/portfolio_chief.webp' },
];

export default function AgentPanel({ agentStates }: AgentPanelProps) {
  return (
    <div className="flex flex-col flex-1 overflow-y-auto custom-scrollbar">
      {agents.map((agent) => {
        const status = agentStates[agent.id] || 'idle';
        const isThinking = status === 'thinking';
        const isActive = status !== 'idle';

        return (
          <motion.div
            key={agent.id}
            initial={false}
            animate={{
              borderColor: isThinking ? "var(--gold-primary)" : "transparent",
              backgroundColor: isThinking ? "rgba(212, 175, 55, 0.05)" : "transparent"
            }}
            className={cn(
              "group flex items-center gap-4 p-4 border-l-2 transition-all duration-300 relative overflow-hidden",
              isActive ? "border-gold-primary" : "border-transparent opacity-60 hover:opacity-100"
            )}
          >
            {/* Active Background Slide */}
            <div className={cn(
              "absolute inset-0 bg-gold-primary/5 transform transition-transform duration-500 origin-left",
              isThinking ? "scale-x-100" : "scale-x-0"
            )} />

            {/* Avatar Container */}
            <div className={cn(
              "relative z-10 w-14 h-14 border border-gold-muted/30 sharp-corners transition-colors duration-300 overflow-hidden",
              isThinking ? "border-gold-primary" : "group-hover:border-gold-muted/50"
            )}>
              <Image
                src={agent.icon}
                alt={agent.name}
                fill
                className="object-cover"
              />
              {isThinking && (
                <div className="absolute inset-0 animate-pulse-amber shadow-[0_0_10px_var(--gold-primary)] opacity-50" />
              )}
            </div>
            
            <div className="flex flex-col relative z-10 flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <span className={cn(
                  "font-serif text-lg tracking-wide transition-colors",
                  isThinking ? "text-gold-primary" : "text-text-primary"
                )}>
                  {agent.name}
                </span>
                {/* Status Dot */}
                {isThinking && (
                  <div className="w-2 h-2 rounded-full bg-gold-bright animate-pulse shadow-[0_0_5px_var(--gold-bright)]" />
                )}
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono text-gold-muted uppercase tracking-wider">
                  {status === 'thinking' ? 'ANALYZING MARKET DATA...' : 
                   status === 'done' ? 'ANALYSIS COMPLETE' : 'STANDING BY'}
                </span>
              </div>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
