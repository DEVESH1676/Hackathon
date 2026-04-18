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
            <div className="lg:col-span-4 space-y-6 lg:sticky lg:top-32">
              <div className="glass rounded-[2rem] p-6 lg:p-10 border-white/5 shadow-2xl shadow-cyan-500/5">
                <div className="flex items-center gap-4 mb-10 text-pretty">
                  <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400 shrink-0">
                    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                  </div>
                  <div>
                    <h1 className="text-2xl font-bold tracking-tight text-white/90">Command Center</h1>
                    <p className="text-[10px] text-zinc-400 font-bold uppercase tracking-widest leading-relaxed">Active Intelligence Session</p>
                  </div>
                </div>
                
                <TicketForm 
                  onSubmit={startPipeline} 
                  isLoading={state.stage !== 'idle' && state.stage !== 'complete' && state.stage !== 'error'} 
                />

                <GlowingProgressBar progress={state.progress} stage={state.stage} />
              </div>

              <div className="h-[280px]">
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
        <footer className="relative z-10 py-8 px-6 border-t border-white/5 bg-black/20 mt-12">
          <div className="max-w-[1600px] mx-auto flex flex-col md:flex-row justify-between items-center gap-4 text-pretty">
            <div className="flex items-center gap-3 opacity-60 grayscale hover:opacity-100 hover:grayscale-0 transition-all cursor-default">
              <span className="text-[10px] font-black tracking-[0.4em] uppercase text-white/80">Nexus Intelligence Platform</span>
            </div>
            <div className="flex gap-10 text-[10px] font-bold text-zinc-500 uppercase tracking-widest">
              <a href="#" className="hover:text-cyan-400 transition-colors">Documentation</a>
              <a href="#" className="hover:text-cyan-400 transition-colors">API Status</a>
              <a href="#" className="hover:text-cyan-400 transition-colors">Security Audit</a>
            </div>
          </div>
        </footer>

      </div>
    </AuroraBackground>
  );
};

export default MainLayout;
