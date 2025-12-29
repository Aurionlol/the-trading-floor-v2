import { useRef, useEffect } from 'react';
import { AgentMessage as AgentMessageType } from '@/types';
import AgentMessage from './AgentMessage';

interface ConversationStreamProps {
  messages: AgentMessageType[];
}

export default function ConversationStream({ messages }: ConversationStreamProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto px-8 py-6 custom-scrollbar relative">
      {/* Timeline Line */}
      {messages.length > 0 && (
          <div className="absolute left-8 top-6 bottom-6 w-[1px] bg-gold-muted/20" />
      )}

      {messages.length === 0 ? (
        <div className="h-full flex flex-col items-center justify-center text-gold-muted/30">
          <div className="w-16 h-16 border border-current sharp-corners flex items-center justify-center mb-4">
            <span className="text-4xl font-headline opacity-50">?</span>
          </div>
          <p className="text-xl font-headline tracking-widest">AWAITING MARKET DATA</p>
          <p className="text-xs font-mono uppercase tracking-wider mt-2">Enter Ticker Symbol to Initialize Council</p>
        </div>
      ) : (
        <div className="pl-8">
            {messages.map((msg, index) => (
            <AgentMessage key={`${msg.agent_id}-${index}`} message={msg} />
            ))}
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}
