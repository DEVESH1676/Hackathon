import React from "react";

const mockHistory = [
  { id: "T-1001", subject: "VPN connection drops", category: "Network", confidence: 0.89, status: "Resolved", date: "2 mins ago" },
  { id: "T-1002", subject: "Access denied to database", category: "Security", confidence: 0.94, status: "Auto-Resolved", date: "15 mins ago" },
  { id: "T-1003", subject: "Slow application response", category: "Infrastructure", confidence: 0.42, status: "Escalated", date: "1 hour ago" },
  { id: "T-1004", subject: "Password reset request", category: "Access", confidence: 0.98, status: "Resolved", date: "2 hours ago" },
];

const HistoryMock: React.FC = () => {
  return (
    <div className="glass rounded-3xl p-6 overflow-hidden">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold tracking-tight text-white/90">Recent Run History</h2>
        <button className="text-xs font-semibold text-cyan-400 hover:text-cyan-300 transition-colors">
          View Full Archive →
        </button>
      </div>

      <div className="space-y-4">
        {mockHistory.map((item) => (
          <div key={item.id} className="flex items-center gap-5 p-5 rounded-2xl bg-white/[0.03] border border-white/5 hover:bg-white/[0.05] transition-all group cursor-pointer shadow-xl">
            <div className="w-14 h-14 rounded-2xl bg-cyan-500/10 flex items-center justify-center text-cyan-400 font-mono text-sm border border-cyan-500/20 group-hover:scale-105 transition-transform shrink-0">
              {item.id.split('-')[1]}
            </div>
            <div className="flex-1 min-w-0">
              <h4 className="text-base font-bold text-white/90 truncate">{item.subject}</h4>
              <div className="flex items-center gap-4 mt-2">
                <span className="text-[11px] font-black text-cyan-500/80 uppercase tracking-widest">{item.category}</span>
                <span className="w-1 h-1 rounded-full bg-zinc-600" />
                <span className="text-xs text-zinc-400 font-bold">{item.date}</span>
              </div>
            </div>
            <div className="text-right flex flex-col items-end gap-2 shrink-0">
              <span className={`text-[10px] font-black px-3 py-1 rounded-lg border tracking-widest ${
                item.status === 'Escalated' 
                  ? 'bg-red-500/20 text-red-300 border-red-500/40 shadow-[0_0_10px_rgba(239,68,68,0.1)]' 
                  : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40 shadow-[0_0_10px_rgba(16,185,129,0.1)]'
              }`}>
                {item.status.toUpperCase()}
              </span>
              <span className="text-[11px] font-mono font-bold text-zinc-400">
                {(item.confidence * 100).toFixed(0)}% CONF
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HistoryMock;
