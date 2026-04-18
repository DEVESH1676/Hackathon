import MainLayout from './layouts/MainLayout'
import IntelligenceFeed from './components/Pipeline/IntelligenceFeed'
import TicketForm from "./components/Command/TicketForm"
import GlowingProgressBar from "./components/Command/GlowingProgressBar"
import TerminalLogs from "./components/Visuals/TerminalLogs"
import HealthPulse from "./components/Pulse/HealthPulse"
import HistoryMock from "./components/History/HistoryMock"
import AnalyticsMock from "./components/Analytics/AnalyticsMock"
import { usePipeline } from './hooks/usePipeline'

function App() {
  const { state, startPipeline } = usePipeline();
  const isPipelineActive = state.stage !== 'idle' && state.stage !== 'complete' && state.stage !== 'error';

  return (
    <MainLayout>
      <div className="space-y-16">
        
        {/* ROW 1: ACTIVE OPERATIONS */}
        <div id="classify" className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* LEFT: Command & Logs */}
          <div className="lg:col-span-4 space-y-6 lg:sticky lg:top-32">
            <div className="glass rounded-[2.5rem] p-8 lg:p-12 border-white/10 shadow-[0_20px_50px_rgba(0,0,0,0.5)] relative overflow-hidden group">
              <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
              
              <div className="flex items-center gap-5 mb-12">
                <div className="w-14 h-14 rounded-3xl bg-cyan-500/5 border border-cyan-500/20 flex items-center justify-center text-cyan-400 shrink-0 shadow-inner">
                  <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                </div>
                <div>
                  <h1 className="text-3xl font-black tracking-tighter text-white/95 leading-none">Command Center</h1>
                  <p className="text-[11px] text-cyan-500/60 font-black uppercase tracking-[0.2em] mt-3">Neural Link Active</p>
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
              <div className="min-h-[750px] h-full rounded-[3.5rem] border-2 border-dashed border-white/10 flex flex-col items-center justify-center group hover:border-cyan-500/30 transition-all duration-1000 bg-white/[0.01] relative overflow-hidden">
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(34,211,238,0.03),transparent_70%)]" />
                
                <div className="flex flex-col items-center gap-10 max-w-md text-center relative z-10 px-12">
                  <div className="relative">
                    <div className="w-24 h-24 rounded-[3rem] bg-cyan-500/5 border border-cyan-500/20 flex items-center justify-center text-cyan-400 group-hover:scale-110 group-hover:rotate-12 transition-all duration-700 shadow-2xl">
                      <svg className="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                    </div>
                    <div className="absolute -inset-8 bg-cyan-500/10 blur-3xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-1000" />
                  </div>
                  <div className="space-y-4">
                    <h3 className="text-2xl font-black text-white/95 tracking-tightest">Awaiting Neural Link</h3>
                    <p className="text-sm text-zinc-400 leading-relaxed font-bold uppercase tracking-wider">
                      Initialize an autonomous intelligence run via the <span className="text-cyan-400">Command Center</span> to generate technical resolutions.
                    </p>
                  </div>
                  <div className="flex flex-col items-center gap-4">
                    <div className="flex items-center gap-3 px-5 py-2 rounded-full bg-white/5 border border-white/10">
                        <div className="w-2 h-2 rounded-full bg-zinc-800" />
                        <span className="text-[10px] font-black uppercase tracking-[0.3em] text-zinc-500">System Standby</span>
                    </div>
                    <p className="text-[10px] font-black text-zinc-600 uppercase tracking-widest animate-pulse">Waiting for telemetry input...</p>
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
            <h2 className="text-3xl font-black tracking-tightest text-white/95 uppercase tracking-widest">Operational Insights</h2>
            <p className="text-zinc-500 text-sm font-bold uppercase tracking-widest">Global Analytics & History Persistence</p>
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
            <div id="analytics" className="xl:col-span-1 h-full">
              <AnalyticsMock />
            </div>
            <div id="history" className="xl:col-span-1 h-full">
              <HistoryMock />
            </div>
            <div className="xl:col-span-1 h-full">
              <HealthPulse />
            </div>
          </div>
        </div>

      </div>
    </MainLayout>
  )
}

export default App
