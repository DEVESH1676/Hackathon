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
                
                <TicketForm 
                  onSubmit={startPipeline} 
                  isLoading={state.stage !== 'idle' && state.stage !== 'complete' && state.stage !== 'error'} 
                />

                <GlowingProgressBar progress={state.progress} stage={state.stage} />
              </div>

              <div className="h-[320px]">
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
      <footer className="relative z-10 py-16 px-8 border-t border-white/5 bg-black/40 mt-24">
        <div className="max-w-[1600px] mx-auto flex flex-col md:flex-row justify-between items-center gap-8 text-pretty">
          <div className="flex items-center gap-4 opacity-80 transition-all cursor-default">
            <div className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center shadow-2xl">
              <span className="text-[12px] font-black text-white">N</span>
            </div>
            <span className="text-[11px] font-black tracking-[0.5em] uppercase text-white">Nexus Intelligence Platform</span>
          </div>
          <div className="flex gap-12 text-[11px] font-black text-zinc-500 uppercase tracking-widest">
            <a href="#" className="hover:text-cyan-400 transition-colors duration-300">Documentation</a>
            <a href="#" className="hover:text-cyan-400 transition-colors duration-300">API Status</a>
            <a href="#" className="hover:text-cyan-400 transition-colors duration-300">Security Audit</a>
          </div>
        </div>
        <div className="max-w-[1600px] mx-auto mt-12 pt-8 border-t border-white/[0.02] flex justify-center">
          <p className="text-[10px] font-bold text-zinc-700 uppercase tracking-[0.4em]">© 2026 NEXUS AI CORE • GLOBAL ARCHITECTURE</p>
        </div>
      </footer>

      </div>
    </AuroraBackground>
  );
};

export default MainLayout;
