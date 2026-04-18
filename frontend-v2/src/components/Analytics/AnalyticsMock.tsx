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
    <div className="glass rounded-3xl p-8 h-full flex flex-col gap-10">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold tracking-tight text-white/90">Analytics</h2>
        <div className="px-4 py-1.5 rounded-full bg-white/5 border border-white/10 text-[10px] font-black text-zinc-400 uppercase tracking-widest shadow-inner">
          30D Overview
        </div>
      </div>

      <div className="space-y-6">
        <div className="p-6 rounded-2xl bg-white/[0.03] border border-white/5 shadow-xl">
          <span className="text-[10px] text-zinc-500 uppercase font-black tracking-[0.2em]">Auto-Resolve Rate</span>
          <div className="flex items-end gap-3 mt-2">
            <span className="text-3xl font-mono font-bold text-emerald-400">74%</span>
            <span className="text-xs text-emerald-500 font-black mb-1.5">+12% ↑</span>
          </div>
        </div>
        <div className="p-6 rounded-2xl bg-white/[0.03] border border-white/5 shadow-xl">
          <span className="text-[10px] text-zinc-500 uppercase font-black tracking-[0.2em]">Avg Confidence</span>
          <div className="flex items-end gap-3 mt-2">
            <span className="text-3xl font-mono font-bold text-cyan-400">86.2%</span>
            <span className="text-xs text-cyan-500 font-black mb-1.5">+2.4% ↑</span>
          </div>
        </div>
      </div>

      <div className="flex-1 min-h-[180px]">
        <span className="text-[10px] text-zinc-500 uppercase font-black tracking-[0.2em] block mb-6">Volume by Category</span>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={categoryData} layout="vertical" margin={{ left: -10, right: 20 }}>
            <XAxis type="number" hide />
            <YAxis 
              dataKey="name" 
              type="category" 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#94a3b8', fontSize: 11, fontWeight: 700 }} 
              width={80}
            />
            <Tooltip 
              cursor={{ fill: 'rgba(255,255,255,0.03)' }}
              contentStyle={{ 
                backgroundColor: 'rgba(9, 9, 11, 0.95)', 
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '16px',
                backdropFilter: 'blur(12px)',
                boxShadow: '0 20px 50px rgba(0,0,0,0.5)'
              }}
            />
            <Bar dataKey="count" radius={[0, 6, 6, 0]} barSize={16}>
              {categoryData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} fillOpacity={0.7} />
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
