import MainLayout from './layouts/MainLayout'

function App() {
  return (
    <MainLayout>
      <div className="space-y-12">
        {/* Intelligence Feed Header */}
        <div className="flex flex-col gap-4">
          <h2 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-white to-white/40 bg-clip-text text-transparent">
            Intelligence Feed
          </h2>
          <p className="text-zinc-500 text-lg max-w-2xl leading-relaxed">
            Real-time autonomous ticket processing. Watch the agentic pipeline classify, retrieve, and resolve complex IT issues.
          </p>
        </div>

        {/* Wave 3: IntelligenceFeed will be implemented here */}
        <div id="classify" className="min-h-[400px] rounded-[2rem] border-2 border-dashed border-white/5 flex items-center justify-center group hover:border-cyan-500/20 transition-all duration-500">
          <div className="flex flex-col items-center gap-4 opacity-20 group-hover:opacity-100 transition-opacity duration-500">
            <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 flex items-center justify-center text-cyan-400">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <span className="text-xs font-bold uppercase tracking-widest text-zinc-500 group-hover:text-cyan-400">Waiting for Pipeline Ignition</span>
          </div>
        </div>
      </div>
    </MainLayout>
  )
}

export default App
