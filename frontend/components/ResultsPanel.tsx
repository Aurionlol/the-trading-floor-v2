import { ConsensusReport, Recommendation } from "@/types";
import { cn } from "@/lib/utils";
import { ArrowDown, ArrowUp, Minus, AlertTriangle, CheckCircle2 } from "lucide-react";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface ResultsPanelProps {
  report: ConsensusReport;
}

const getRecommendationStyle = (rec: Recommendation) => {
  switch (rec) {
    case "strong_buy": return { color: "text-green-banker", label: "STRONG BUY", border: "border-green-banker" };
    case "buy": return { color: "text-green-banker", label: "BUY", border: "border-green-banker" };
    case "sell": return { color: "text-orange-warning", label: "SELL", border: "border-orange-warning" };
    case "strong_sell": return { color: "text-orange-warning", label: "STRONG SELL", border: "border-orange-warning" };
    case "hold": return { color: "text-gold-muted", label: "HOLD", border: "border-gold-muted" };
    default: return { color: "text-text-muted", label: "NEUTRAL", border: "border-text-muted" };
  }
};

export default function ResultsPanel({ report }: ResultsPanelProps) {
    const [expandedScore, setExpandedScore] = useState<string | null>(null);

  if (!report) return null;

  const recStyle = getRecommendationStyle(report.recommendation);

  return (
    <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="mt-8 space-y-6 pb-12"
    >
      {/* Executive Summary Card */}
      <div className="bg-bg-card border-2 border-gold-primary p-1 sharp-corners shadow-[0_0_50px_-10px_rgba(212,175,55,0.1)] relative">
        <div className="border border-gold-muted/50 p-6 sharp-corners bg-bg-primary relative">
            
            {/* Corner Ornaments */}
            <div className="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-gold-primary" />
            <div className="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-gold-primary" />
            <div className="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-gold-primary" />
            <div className="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-gold-primary" />

            <div className="flex flex-col md:flex-row gap-8 mb-8 relative z-10">
                {/* Recommendation Badge */}
                <div className={cn(
                    "flex-none flex flex-col items-center justify-center p-8 border-4 sharp-corners min-w-[200px] bg-bg-elevated",
                    recStyle.border
                )}>
                    <span className={cn("text-4xl font-headline tracking-widest leading-none mb-2", recStyle.color)}>
                        {recStyle.label}
                    </span>
                    <div className="w-full h-[1px] bg-current opacity-30 my-2" />
                    <span className="text-xs font-mono text-gold-muted uppercase tracking-wider">
                        Consensus Verdict
                    </span>
                </div>

                {/* Metrics */}
                <div className="flex-1 grid grid-cols-2 gap-4">
                    <div className="p-4 border border-gold-muted/30 sharp-corners bg-bg-elevated/30">
                        <div className="text-xs font-mono text-gold-muted uppercase tracking-wider mb-1">Confidence</div>
                        <div className="text-2xl font-headline text-gold-primary tracking-wide">{report.confidence.toUpperCase()}</div>
                    </div>
                    <div className="p-4 border border-gold-muted/30 sharp-corners bg-bg-elevated/30">
                        <div className="text-xs font-mono text-gold-muted uppercase tracking-wider mb-1">Position Size</div>
                        <div className="text-2xl font-headline text-gold-primary tracking-wide">{report.position_size_pct}%</div>
                    </div>
                </div>
            </div>

            <div className="relative">
                <h3 className="text-gold-muted font-serif text-xl mb-4 italic">Executive Summary</h3>
                <p className="text-lg leading-relaxed font-mono text-text-primary border-l-2 border-gold-muted/30 pl-6">
                    {report.executive_summary}
                </p>
            </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Agent Scores */}
        <div className="bg-bg-elevated/30 border border-gold-muted/20 p-6 sharp-corners relative">
            <h3 className="text-xl font-headline text-gold-muted tracking-widest mb-6 flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5" />
                VOTING RECORD
            </h3>
            <div className="space-y-4">
                {report.agent_scores.map((agent) => (
                    <div 
                        key={agent.agent_name}
                        className="group border border-gold-muted/10 bg-bg-primary sharp-corners overflow-hidden hover:border-gold-primary/50 transition-colors cursor-pointer"
                        onClick={() => setExpandedScore(expandedScore === agent.agent_name ? null : agent.agent_name)}
                    >
                        <div className="p-4 flex items-center justify-between">
                            <span className="font-serif text-gold-primary/80 group-hover:text-gold-primary transition-colors">{agent.agent_name}</span>
                            <div className="flex items-center gap-4">
                                <div className="w-32 h-1 bg-bg-elevated">
                                    <div 
                                        className="h-full bg-gold-primary transition-all duration-1000 ease-out"
                                        style={{ width: `${agent.score}%` }}
                                    />
                                </div>
                                <span className="font-mono font-bold w-8 text-right text-gold-bright">{agent.score}</span>
                            </div>
                        </div>
                        <AnimatePresence>
                            {expandedScore === agent.agent_name && (
                                <motion.div
                                    initial={{ height: 0 }}
                                    animate={{ height: "auto" }}
                                    exit={{ height: 0 }}
                                    className="overflow-hidden"
                                >
                                    <div className="p-4 pt-0 text-sm font-mono text-text-secondary border-t border-gold-muted/10 bg-bg-card/50">
                                        <div className="pt-2 italic text-gold-muted">Rationale:</div>
                                        {agent.rationale}
                                    </div>
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>
                ))}
            </div>
        </div>

        {/* Risk & Invalidations */}
        <div className="bg-bg-elevated/30 border border-gold-muted/20 p-6 sharp-corners relative">
            <h3 className="text-xl font-headline text-gold-muted tracking-widest mb-6 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-orange-warning" />
                RISK ASSESSMENT
            </h3>
            
            <div className="space-y-8">
                <div>
                    <h4 className="text-xs font-mono font-bold text-orange-warning uppercase tracking-widest mb-4 border-b border-orange-warning/20 pb-2">Primary Risk Factors</h4>
                    <ul className="space-y-2">
                        {report.risk_factors.map((risk, i) => (
                            <li key={i} className="text-sm font-mono text-text-primary flex items-start gap-3">
                                <span className="text-orange-warning mt-0.5 text-xs">▲</span>
                                {risk}
                            </li>
                        ))}
                    </ul>
                </div>

                <div>
                    <h4 className="text-xs font-mono font-bold text-gold-bright uppercase tracking-widest mb-4 border-b border-gold-bright/20 pb-2">Invalidation Criteria</h4>
                    <ul className="space-y-2">
                        {report.invalidation_criteria.map((criteria, i) => (
                            <li key={i} className="text-sm font-mono text-text-primary flex items-start gap-3">
                                <span className="text-gold-bright mt-0.5 text-xs">◆</span>
                                {criteria}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
      </div>
    </motion.div>
  );
}
