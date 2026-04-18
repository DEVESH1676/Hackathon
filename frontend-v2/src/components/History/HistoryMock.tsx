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

      <div className="space-y-3">
        {mockHistory.map((item) => (
          <div key={item.id} className="flex items-center gap-4 p-4 rounded-2xl bg-white/[0.02] border border-white/5 hover:bg-white/[0.04] transition-all group cursor-pointer">
            <div className="w-12 h-12 rounded-xl bg-cyan-500/10 flex items-center justify-center text-cyan-400 font-mono text-xs border border-cyan-500/20 group-hover:scale-110 transition-transform">
              {item.id.split('-')[1]}
            </div>
            <div className="flex-1 min-w-0">
              <h4 className="text-sm font-semibold text-white/80 truncate">{item.subject}</h4>
              <div className="flex items-center gap-3 mt-1">
                <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-tighter">{item.category}</span>
                <span className="w-1 h-1 rounded-full bg-zinc-700" />
                <span className="text-[10px] text-zinc-500 font-medium">{item.date}</span>
              </div>
            </div>
            <div className="text-right flex flex-col items-end gap-1">
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                item.status === 'Escalated' 
                  ? 'bg-red-500/10 text-red-400 border-red-500/20' 
                  : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
              }`}>
                {item.status.toUpperCase()}
              </span>
              <span className="text-[10px] font-mono text-zinc-500">
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
