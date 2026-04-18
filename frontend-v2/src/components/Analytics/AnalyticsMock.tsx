import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const categoryData = [
  { name: 'Network', count: 42, color: '#22d3ee' },
  { name: 'Security', count: 38, color: '#818cf8' },
  { name: 'Infra', count: 25, color: '#a855f7' },
  { name: 'Access', count: 18, color: '#f472b6' },
  { name: 'App', count: 12, color: '#fbbf24' },
];

const AnalyticsMock: React.FC = () => {
  return (
    <div className="glass rounded-3xl p-6 h-full flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold tracking-tight text-white/90">Intelligence Analytics</h2>
        <div className="px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[10px] font-bold text-zinc-400 uppercase tracking-widest">
          Last 30 Days
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/5">
          <span className="text-[10px] text-zinc-500 uppercase font-bold tracking-widest">Auto-Resolve Rate</span>
          <div className="flex items-end gap-2 mt-1">
            <span className="text-2xl font-mono font-bold text-emerald-400">74%</span>
            <span className="text-[10px] text-emerald-500 font-bold mb-1">+12% ↑</span>
          </div>
        </div>
        <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/5">
          <span className="text-[10px] text-zinc-500 uppercase font-bold tracking-widest">Avg Confidence</span>
          <div className="flex items-end gap-2 mt-1">
            <span className="text-2xl font-mono font-bold text-cyan-400">86.2%</span>
            <span className="text-[10px] text-cyan-500 font-bold mb-1">+2.4% ↑</span>
          </div>
        </div>
      </div>

      <div className="flex-1 min-h-[200px]">
        <span className="text-[10px] text-zinc-500 uppercase font-bold tracking-widest block mb-4">Volume by Category</span>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={categoryData} layout="vertical" margin={{ left: -20 }}>
            <XAxis type="number" hide />
            <YAxis 
              dataKey="name" 
              type="category" 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#94a3b8', fontSize: 10, fontWeight: 600 }} 
              width={70}
            />
            <Tooltip 
              cursor={{ fill: 'rgba(255,255,255,0.02)' }}
              contentStyle={{ 
                backgroundColor: 'rgba(9, 9, 11, 0.8)', 
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '12px',
                backdropFilter: 'blur(8px)'
              }}
            />
            <Bar dataKey="count" radius={[0, 4, 4, 0]} barSize={12}>
              {categoryData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} fillOpacity={0.6} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="pt-4 border-t border-white/5 flex items-center justify-between text-xs">
        <span className="text-zinc-500">Processing Node: <span className="text-zinc-300 font-mono">US-EAST-1</span></span>
        <span className="text-zinc-500">Latency: <span className="text-emerald-400 font-mono">14ms</span></span>
      </div>
    </div>
  );
};

export default AnalyticsMock;
