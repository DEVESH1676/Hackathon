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

        {state.stage === 'idle' ? (
          <div className="min-h-[400px] rounded-[3rem] border-2 border-dashed border-white/5 flex items-center justify-center group hover:border-cyan-500/20 transition-all duration-500">
            <div className="flex flex-col items-center gap-4 opacity-20 group-hover:opacity-100 transition-opacity duration-500">
              <div className="w-16 h-16 rounded-[2rem] bg-cyan-500/10 flex items-center justify-center text-cyan-400">
                <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <span className="text-sm font-bold uppercase tracking-[0.2em] text-zinc-500 group-hover:text-cyan-400">Waiting for Pipeline Ignition</span>
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
