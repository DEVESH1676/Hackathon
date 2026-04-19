import { useState } from 'react'
import MainLayout from './layouts/MainLayout'
import IntelligenceFeed from './components/Pipeline/IntelligenceFeed'
import TicketForm from "./components/Command/TicketForm"
import GlowingProgressBar from "./components/Command/GlowingProgressBar"
import TerminalLogs from "./components/Visuals/TerminalLogs"
import HealthPulse from "./components/Pulse/HealthPulse"
import HistoryMock from "./components/History/HistoryMock"
import AnalyticsMock from "./components/Analytics/AnalyticsMock"
import { usePipeline } from './hooks/usePipeline'

import Blueprint from './pages/Blueprint'

function App() {
  const { state, startPipeline } = usePipeline();
  const [activeView, setActiveView] = useState<'operations' | 'architecture'>('operations');
  const isPipelineActive = state.stage !== 'idle' && state.stage !== 'complete' && state.stage !== 'error';

  return (
    <MainLayout onViewChange={(view) => setActiveView(view)}>
      {activeView === 'operations' ? (
        <div className="space-y-16">
          
          {/* ROW 1: ACTIVE OPERATIONS */}
          <div id="classify" className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            
            {/* LEFT: Command & Logs */}
            <div className="lg:col-span-4 space-y-6 lg:sticky lg:top-32">
              <div className="glass rounded-2xl p-8 lg:p-10 border-white/10 shadow-[0_20px_50px_rgba(0,0,0,0.4)] relative overflow-hidden group">
                <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-cyan-500/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
                
                <div className="flex items-center gap-4 mb-10">
                  <div className="w-12 h-12 rounded-xl bg-cyan-500/5 border border-cyan-500/20 flex items-center justify-center text-cyan-400 shrink-0 shadow-inner">
                    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                  </div>
                  <div>
                    <h1 className="text-xl font-black tracking-tight text-white/90 leading-none">Command Center</h1>
                    <p className="text-[10px] text-[#94a3b8] font-black uppercase tracking-[0.2em] mt-2">Neural Link Active</p>
                  </div>
                </div>
                
                <TicketForm onSubmit={startPipeline} isLoading={isPipelineActive} />
                <GlowingProgressBar progress={state.progress} stage={state.stage} />
              </div>

              {/* Terminal always visible for active feedback */}
              <div className="h-[300px]">
                <TerminalLogs />
              </div>
            </div>

            {/* RIGHT: Intelligence Feed */}
            <div className="lg:col-span-8">
              {state.stage === 'idle' ? (
                <div className="min-h-[750px] h-full rounded-2xl border border-white/10 flex flex-col items-center justify-center bg-white/[0.01] relative overflow-hidden p-12">
                  <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(34,211,238,0.03),transparent_70%)]" />
                  
                  <div className="w-full max-w-2xl space-y-12 relative z-10">
                    <div className="flex flex-col items-center gap-6 text-center">
                      <div className="relative">
                        <div className="w-20 h-20 rounded-2xl bg-cyan-500/5 border border-cyan-500/20 flex items-center justify-center text-cyan-400 shadow-2xl">
                          <svg className="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M13 10V3L4 14h7v7l9-11h-7z" />
                          </svg>
                        </div>
                        <div className="absolute -inset-4 bg-cyan-500/10 blur-2xl rounded-full animate-pulse" />
                      </div>
                      <div className="space-y-2">
                        <h3 className="text-2xl font-black text-white/95 tracking-tight">System Readiness Report</h3>
                        <p className="text-sm text-[#94a3b8] font-bold uppercase tracking-widest">Autonomous Core: Standby</p>
                      </div>
                    </div>

                    {/* Mocked Readiness Metrics to fill the "void" */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="glass p-6 rounded-xl border-white/5 space-y-4">
                        <div className="flex justify-between items-center text-[10px] font-black uppercase tracking-widest text-[#94a3b8]">
                            <span>Neural Path Integrity</span>
                            <span className="text-emerald-400 text-xs">99.8%</span>
                        </div>
                        <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                            <div className="h-full w-[99.8%] bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.3)]" />
                        </div>
                      </div>
                      <div className="glass p-6 rounded-xl border-white/5 space-y-4">
                        <div className="flex justify-between items-center text-[10px] font-black uppercase tracking-widest text-[#94a3b8]">
                            <span>KB Sync Latency</span>
                            <span className="text-cyan-400 text-xs">14ms</span>
                        </div>
                        <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                            <div className="h-full w-[14%] bg-cyan-500 shadow-[0_0_10px_rgba(34,211,238,0.3)]" />
                        </div>
                      </div>
                    </div>

                    <div className="p-8 glass rounded-xl border-cyan-500/20 bg-cyan-500/[0.02] text-center">
                      <p className="text-xs text-[#94a3b8] leading-relaxed font-bold uppercase tracking-[0.15em]">
                        Awaiting telemetry input from <span className="text-white">Command Center</span> to initiate resolution synthesis.
                      </p>
                    </div>
                  </div>
                </div>
              ) : (
                <IntelligenceFeed />
              )}
            </div>
          </div>

          {/* ROW 2: SYSTEM INSIGHTS */}
          <div className="space-y-12 pt-12 border-t border-white/5">
            <div className="flex flex-col gap-2">
              <h2 className="text-2xl font-black tracking-tight text-white/90 uppercase tracking-widest">Operational Insights</h2>
              <p className="text-[#94a3b8] text-[10px] font-black uppercase tracking-[0.3em]">Global Analytics & System Telemetry</p>
            </div>

            <div className="space-y-8">
              {/* Top Insight Row: Side-by-Side Metrics */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div id="analytics">
                  <AnalyticsMock />
                </div>
                <HealthPulse />
              </div>

              {/* Bottom Insight Row: Full-Width History */}
              <div id="history">
                <HistoryMock />
              </div>
            </div>
          </div>

        </div>
      ) : (
        <Blueprint />
      )}
    </MainLayout>
  )
}

export default App
