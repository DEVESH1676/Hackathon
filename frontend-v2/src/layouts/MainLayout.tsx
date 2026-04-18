import React from "react";
import PillNavbar from "../components/Navigation/PillNavbar";
import HealthPulse from "../components/Pulse/HealthPulse";
import HistoryMock from "../components/History/HistoryMock";
import AnalyticsMock from "../components/Analytics/AnalyticsMock";

const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="min-h-screen bg-[#020617] text-white font-sans selection:bg-cyan-500/30 overflow-x-hidden">
      {/* Background Aurora Effect */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] rounded-full bg-cyan-500/10 blur-[140px] animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] rounded-full bg-purple-600/10 blur-[140px] animate-pulse delay-1000" />
        <div className="absolute top-[20%] right-[10%] w-[30%] h-[30%] rounded-full bg-indigo-500/5 blur-[120px] animate-pulse delay-700" />
      </div>

      <PillNavbar />

      <main className="relative z-10 pt-32 pb-20 px-6 max-w-[1600px] mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Left Panel: Command Center (4 Cols) */}
          <div className="lg:col-span-4 space-y-8 sticky top-32">
            <div className="glass rounded-[2rem] p-8 border-cyan-500/20 shadow-2xl shadow-cyan-500/5">
              <div className="flex items-center gap-3 mb-6">
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
              
              {/* TicketForm Placeholder will be injected here in Wave 3 */}
              <div className="p-12 border-2 border-dashed border-white/5 rounded-3xl text-center">
                <span className="text-zinc-600 text-xs font-medium uppercase tracking-widest">Ticket Interface Stub</span>
              </div>
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
        <div className="max-w-[1600px] mx-auto flex flex-col md:row justify-between items-center gap-6">
          <div className="flex items-center gap-3 opacity-40 grayscale hover:opacity-100 hover:grayscale-0 transition-all cursor-default">
            <span className="text-xs font-black tracking-[0.3em] uppercase">Nexus Intelligence Platform</span>
          </div>
          <div className="flex gap-8 text-[10px] font-bold text-zinc-600 uppercase tracking-widest">
            <a href="#" className="hover:text-cyan-500 transition-colors">Documentation</a>
            <a href="#" className="hover:text-cyan-500 transition-colors">API Status</a>
            <a href="#" className="hover:text-cyan-500 transition-colors">Security Audit</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default MainLayout;
