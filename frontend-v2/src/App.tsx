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
        {/* Pipeline Stages Placeholder */}
        <div id="classify" className="space-y-8">
          {state.stage === 'idle' ? (
            <div className="min-h-[500px] rounded-[3rem] border-2 border-dashed border-white/5 flex flex-col items-center justify-center group hover:border-cyan-500/20 transition-all duration-700 bg-white/[0.01]">
              <div className="flex flex-col items-center gap-8 max-w-sm text-center">
                <div className="relative">
                  <div className="w-20 h-20 rounded-[2.5rem] bg-cyan-500/10 flex items-center justify-center text-cyan-400 group-hover:scale-110 transition-transform duration-500">
                    <svg className="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <div className="absolute -inset-4 bg-cyan-500/20 blur-2xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
                </div>
                <div className="space-y-3 relative z-10 px-6">
                  <h3 className="text-xl font-bold text-white/90">Awaiting Pipeline Ignition</h3>
                  <p className="text-sm text-zinc-500 leading-relaxed font-medium">
                    Submit a technical ticket via the <span className="text-cyan-400 font-bold">Command Center</span> to start the autonomous reasoning process.
                  </p>
                </div>
                <div className="flex items-center gap-2 text-zinc-600">
                   <div className="w-1.5 h-1.5 rounded-full bg-zinc-800" />
                   <span className="text-[10px] font-black uppercase tracking-widest">Neural Link Offline</span>
                </div>
              </div>
            </div>
          ) : (

          <IntelligenceFeed />
        )}
      </div>
    </MainLayout>
  )
}

export default App
