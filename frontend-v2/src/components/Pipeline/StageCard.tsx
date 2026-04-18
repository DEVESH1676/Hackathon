import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, Circle, Clock, AlertCircle, Search, Cpu, Zap, ShieldCheck, FileText } from 'lucide-react';
import { cn } from '../../lib/utils';

interface StageCardProps {
  stage: string;
  title: string;
  status: 'idle' | 'running' | 'completed' | 'error';
  result?: any;
  index: number;
}

const StageCard: React.FC<StageCardProps> = ({ stage, title, status, result, index }) => {
  const getIcon = () => {
    switch (stage) {
      case 'classify': return <Zap className="w-5 h-5" />;
      case 'triage': return <Cpu className="w-5 h-5" />;
      case 'rag': return <Search className="w-5 h-5" />;
      case 'resolve': return <FileText className="w-5 h-5" />;
      case 'judge': return <ShieldCheck className="w-5 h-5" />;
      default: return <Clock className="w-5 h-5" />;
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'completed': return <CheckCircle2 className="w-5 h-5 text-emerald-400" />;
      case 'running': return <motion.div animate={{ rotate: 360 }} transition={{ duration: 2, repeat: Infinity, ease: "linear" }}><Clock className="w-5 h-5 text-blue-400" /></motion.div>;
      case 'error': return <AlertCircle className="w-5 h-5 text-red-400" />;
      default: return <Circle className="w-5 h-5 text-slate-500" />;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, filter: 'blur(10px)' }}
      animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
      className={cn(
        "relative group overflow-hidden rounded-xl border p-4 transition-all duration-500",
        "bg-white/5 backdrop-blur-md border-white/10",
        status === 'running' && "border-blue-500/50 shadow-[0_0_20px_rgba(59,130,246,0.15)]",
        status === 'completed' && "border-emerald-500/30 bg-emerald-500/[0.02]"
      )}
    >
      {/* Holographic linear-gradient border for active/completed */}
      {(status === 'running' || status === 'completed') && (
        <div className={cn(
          "absolute inset-0 pointer-events-none opacity-50",
          status === 'running' ? "bg-gradient-to-tr from-blue-500/20 via-transparent to-purple-500/20" : "bg-gradient-to-tr from-emerald-500/10 via-transparent to-blue-500/10"
        )} />
      )}

      <div className="flex items-start justify-between gap-4 relative z-10">
        <div className="flex items-center gap-3">
          <div className={cn(
            "p-2 rounded-lg bg-white/5 transition-colors duration-300",
            status === 'completed' ? "text-emerald-400 shadow-[0_0_10px_rgba(52,211,153,0.2)]" : "text-slate-400",
            status === 'running' && "text-blue-400 shadow-[0_0_10px_rgba(59,130,246,0.3)]"
          )}>
            {getIcon()}
          </div>
          <div>
            <div>
              <h3 className={cn(
                "text-[13px] font-black tracking-tight transition-colors duration-300",
                status === 'idle' ? "text-slate-500" : "text-slate-100"
              )}>
                {title.toUpperCase()}
              </h3>
              {status === 'running' && (
                <p className="text-[9px] uppercase tracking-[0.3em] text-blue-400 mt-1.5 font-black animate-pulse">
                  Neural Synthesis Active
                </p>
              )}
            </div>
            ...
            <AnimatePresence>
            {result && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="mt-6 pt-6 border-t border-white/5 relative z-10"
            >
              <div className="bg-black/30 rounded-xl p-5 overflow-hidden border border-white/5 shadow-inner">
                 <pre className="text-[11px] font-mono font-medium text-zinc-400 overflow-x-auto whitespace-pre-wrap leading-relaxed">
                  {typeof result === 'string' ? result : JSON.stringify(result, null, 3)}
                </pre>
              </div>
            </motion.div>
            )}
            </AnimatePresence>

            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default StageCard;
