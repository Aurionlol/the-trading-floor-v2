import { AgentMessage as AgentMessageType } from '@/types';
import { cn } from '@/lib/utils';
import ReactMarkdown from 'react-markdown';

interface AgentMessageProps {
  message: AgentMessageType;
}

// Reuse avatars here or simplify
const AgentSeal = ({ agentId }: { agentId: string }) => {
    // Return a simplified geometric shape based on ID
    const color = "text-gold-muted";
    switch(agentId) {
        case 'quant': return <svg viewBox="0 0 24 24" className={`w-6 h-6 ${color}`} fill="none" stroke="currentColor"><path d="M12 2L2 7V17L12 22L22 17V7L12 2Z" /></svg>;
        case 'sentiment': return <svg viewBox="0 0 24 24" className={`w-6 h-6 ${color}`} fill="none" stroke="currentColor"><path d="M12 2L2 12L12 22L22 12L12 2Z" /></svg>;
        case 'macro': return <svg viewBox="0 0 24 24" className={`w-6 h-6 ${color}`} fill="none" stroke="currentColor"><circle cx="12" cy="12" r="8" /></svg>;
        case 'risk': return <svg viewBox="0 0 24 24" className={`w-6 h-6 ${color}`} fill="none" stroke="currentColor"><path d="M12 2L2 22H22L12 2Z" /></svg>;
        case 'portfolio': return <svg viewBox="0 0 24 24" className={`w-6 h-6 ${color}`} fill="none" stroke="currentColor"><path d="M12 2L3 7V12C3 17 7 21 12 22C17 21 21 17 21 12V7L12 2Z" /></svg>;
        default: return <svg viewBox="0 0 24 24" className={`w-6 h-6 ${color}`} fill="none" stroke="currentColor"><rect x="2" y="2" width="20" height="20" /></svg>;
    }
}

export default function AgentMessage({ message }: AgentMessageProps) {
  const isThinking = message.message_type === 'thinking';
  
  return (
    <div className={cn(
      "relative mb-6 animate-slide-in group",
      isThinking ? "opacity-70" : "opacity-100"
    )}>
      {/* Connector Line */}
      <div className="absolute left-[-29px] top-6 w-6 h-[1px] bg-gold-muted/30" />
      <div className="absolute left-[-32px] top-5 w-2 h-2 rounded-full border border-gold-muted/50 bg-bg-primary" />

      <div className="border-l-2 border-gold-primary bg-bg-elevated/30 p-1 sharp-corners shadow-lg hover:bg-bg-elevated/50 transition-colors">
        <div className="border border-gold-muted/20 p-4 sharp-corners relative overflow-hidden">
            
            {/* Header */}
            <div className="flex items-center justify-between mb-4 border-b border-gold-muted/10 pb-2">
                <div className="flex items-center gap-3">
                    <div className="p-1 border border-gold-muted/30 bg-bg-primary sharp-corners">
                        <AgentSeal agentId={message.agent_id} />
                    </div>
                    <div>
                        <div className="font-serif text-gold-primary tracking-wide text-lg leading-none">
                            {message.agent_name.toUpperCase()}
                        </div>
                        <div className="font-mono text-[10px] text-gold-muted uppercase tracking-widest mt-1">
                            CLASSIFIED ANALYSIS
                        </div>
                    </div>
                </div>
                <div className="font-mono text-xs text-gold-muted/50 border border-gold-muted/20 px-2 py-0.5">
                    {new Date(message.timestamp).toLocaleTimeString([], { hour12: false })} UTC
                </div>
            </div>

            {/* Content */}
            <div className="font-mono text-sm text-text-primary leading-relaxed">
                {isThinking ? (
                   <div className="flex items-center gap-2 text-gold-muted animate-pulse">
                       <span className="w-2 h-2 bg-gold-primary rounded-full" />
                       <span className="tracking-widest uppercase text-xs">Processing Market Data Stream...</span>
                   </div>
                ) : (
                   <div className="prose prose-invert max-w-none prose-p:my-2 prose-headings:text-gold-muted prose-headings:font-headline prose-headings:tracking-widest prose-strong:text-gold-primary prose-ul:list-square prose-li:marker:text-gold-muted">
                        <ReactMarkdown>{message.content}</ReactMarkdown>
                   </div>
                )}
            </div>

            {/* Corner Decors */}
            <div className="absolute top-0 right-0 w-4 h-4 border-t border-r border-gold-muted/30" />
            <div className="absolute bottom-0 left-0 w-4 h-4 border-b border-l border-gold-muted/30" />
        </div>
      </div>
    </div>
  );
}
