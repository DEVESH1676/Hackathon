import MainLayout from './layouts/MainLayout'
import IntelligenceFeed from './components/Pipeline/IntelligenceFeed'
import { usePipeline } from './hooks/usePipeline'

function App() {
  const { state } = usePipeline();

  return (
    <MainLayout>
      <div className="space-y-12">
        {/* Intelligence Feed Header */}
        <div className="flex flex-col gap-4">
          <h2 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-white to-white/40 bg-clip-text text-transparent">
            Intelligence Feed
          </h2>
          <p className="text-zinc-500 text-lg max-w-2xl leading-relaxed text-pretty">
            Real-time autonomous ticket processing. Watch the agentic pipeline classify, retrieve, and resolve complex IT issues.
          </p>
        </div>

        {/* Pipeline Stages Placeholder */}
        <div id="classify" className="space-y-8">
          {state.stage === 'idle' ? (
            <div className="min-h-[550px] rounded-[3.5rem] border-2 border-dashed border-white/10 flex flex-col items-center justify-center group hover:border-cyan-500/30 transition-all duration-1000 bg-white/[0.01] relative overflow-hidden">
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
    </MainLayout>
  )
}

export default App
