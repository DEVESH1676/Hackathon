import React from "react";
import PillNavbar from "../components/Navigation/PillNavbar";
import HealthPulse from "../components/Pulse/HealthPulse";
import HistoryMock from "../components/History/HistoryMock";
import AnalyticsMock from "../components/Analytics/AnalyticsMock";
import TicketForm from "../components/Command/TicketForm";
import GlowingProgressBar from "../components/Command/GlowingProgressBar";
import TerminalLogs from "../components/Visuals/TerminalLogs";
import { AuroraBackground } from "../components/Visuals/AuroraBackground";
import { usePipeline } from "../hooks/usePipeline";

const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { state, startPipeline } = usePipeline();

  return (
    <AuroraBackground className="z-0">
      <div className="min-h-screen text-white font-sans selection:bg-cyan-500/30 overflow-x-hidden text-balance w-full">
        <PillNavbar />

        <main className="relative z-10 pt-32 pb-20 px-6 max-w-[1600px] mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            
            {/* Left Panel: Command Center (4 Cols) */}
            <div className="lg:col-span-4 space-y-8 lg:sticky lg:top-32">
              <div className="glass rounded-[2rem] p-8 border-cyan-500/20 shadow-2xl shadow-cyan-500/5">
                <div className="flex items-center gap-3 mb-8 text-pretty">
                  <div className="w-10 h-10 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                  </div>
                  <div>
                    <h1 className="text-xl font-bold tracking-tight">Command Center</h1>
                    <p className="text-[10px] text-zinc-500 font-bold uppercase tracking-widest">Active Intelligence Session</p>
                  </div>
                </div>
                
                <TicketForm 
                  onSubmit={startPipeline} 
                  isLoading={state.stage !== 'idle' && state.stage !== 'complete' && state.stage !== 'error'} 
                />

                <GlowingProgressBar progress={state.progress} stage={state.stage} />
              </div>

              <div className="h-[300px]">
                <TerminalLogs />
              </div>

              <HealthPulse />
            </div>

            {/* Right Panel: Intelligence Feed (8 Cols) */}
            <div className="lg:col-span-8 space-y-12">
              <section id="feed-root" className="min-h-[600px]">
                {children}
              </section>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <section id="history">
                  <HistoryMock />
                </section>
                <section id="analytics">
                  <AnalyticsMock />
                </section>
              </div>
            </div>

          </div>
        </main>

        {/* Footer Branding */}
        <footer className="relative z-10 py-12 px-6 border-t border-white/5">
          <div className="max-w-[1600px] mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="flex items-center gap-3 opacity-40 grayscale hover:opacity-100 hover:grayscale-0 transition-all cursor-default text-pretty">
              <span className="text-xs font-black tracking-[0.3em] uppercase text-white">Nexus Intelligence Platform</span>
            </div>
            <div className="flex gap-8 text-[10px] font-bold text-zinc-600 uppercase tracking-widest">
              <a href="#" className="hover:text-cyan-500 transition-colors text-zinc-500">Documentation</a>
              <a href="#" className="hover:text-cyan-500 transition-colors text-zinc-500">API Status</a>
              <a href="#" className="hover:text-cyan-500 transition-colors text-zinc-500">Security Audit</a>
            </div>
          </div>
        </footer>
      </div>
    </AuroraBackground>
  );
};

export default MainLayout;
