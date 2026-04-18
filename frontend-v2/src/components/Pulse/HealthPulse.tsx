import React from "react";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { time: '10:00', load: 40, latency: 240 },
  { time: '11:00', load: 30, latency: 138 },
  { time: '12:00', load: 20, latency: 980 },
  { time: '13:00', load: 27, latency: 390 },
  { time: '14:00', load: 18, latency: 480 },
  { time: '15:00', load: 23, latency: 380 },
  { time: '16:00', load: 34, latency: 430 },
];

const HealthPulse: React.FC = () => {
  return (
    <div className="p-6 h-full glass rounded-3xl flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold tracking-tight text-white/90 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
          System Health Pulse
        </h2>
        <div className="flex gap-4 text-xs font-medium text-zinc-400">
          <span className="flex items-center gap-1">
            <div className="w-2 h-2 rounded-full bg-cyan-500/50" /> API Load
          </span>
          <span className="flex items-center gap-1">
            <div className="w-2 h-2 rounded-full bg-purple-500/50" /> Latency
          </span>
        </div>
      </div>

      <div className="flex-1 min-h-[200px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorLoad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#22d3ee" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorLatency" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#a855f7" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#a855f7" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
            <XAxis 
              dataKey="time" 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#71717a', fontSize: 10 }} 
            />
            <YAxis 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#71717a', fontSize: 10 }} 
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'rgba(9, 9, 11, 0.8)', 
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '12px',
                backdropFilter: 'blur(8px)'
              }}
              itemStyle={{ fontSize: '12px' }}
            />
            <Area 
              type="monotone" 
              dataKey="load" 
              stroke="#22d3ee" 
              fillOpacity={1} 
              fill="url(#colorLoad)" 
              strokeWidth={2}
            />
            <Area 
              type="monotone" 
              dataKey="latency" 
              stroke="#a855f7" 
              fillOpacity={1} 
              fill="url(#colorLatency)" 
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-3 gap-4 pt-2 border-t border-white/5">
        <div className="flex flex-col">
          <span className="text-[10px] text-zinc-500 uppercase font-bold tracking-wider">Models</span>
          <span className="text-sm font-mono text-cyan-400">Online</span>
        </div>
        <div className="flex flex-col">
          <span className="text-[10px] text-zinc-500 uppercase font-bold tracking-wider">Requests</span>
          <span className="text-sm font-mono text-white/90">1.2k</span>
        </div>
        <div className="flex flex-col">
          <span className="text-[10px] text-zinc-500 uppercase font-bold tracking-wider">Uptime</span>
          <span className="text-sm font-mono text-white/90">99.9%</span>
        </div>
      </div>
    </div>
  );
};

export default HealthPulse;
