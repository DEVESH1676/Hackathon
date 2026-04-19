import React, { useState, useEffect } from "react";

const sections = [
  { id: "classify", label: "Pipeline" },
  { id: "history", label: "History" },
  { id: "analytics", label: "Analytics" },
  { id: "blueprint", label: "Blueprint" },
];

interface PillNavbarProps {
  onViewChange?: (view: "operations" | "architecture") => void;
}

const PillNavbar: React.FC<PillNavbarProps> = ({ onViewChange }) => {
  const [activeSection, setActiveSection] = useState("classify");

  useEffect(() => {
    const handleScroll = () => {
      // Don't update active section via scroll if we're in blueprint view
      if (activeSection === "blueprint") return;

      const sectionElements = sections
        .filter(s => s.id !== "blueprint")
        .map(s => document.getElementById(s.id));
      const currentSection = sectionElements.find(el => {
        if (!el) return false;
        const rect = el.getBoundingClientRect();
        return rect.top >= -100 && rect.top <= 400;
      });
      if (currentSection) setActiveSection(currentSection.id);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [activeSection]);

  return (
    <nav className="fixed top-8 left-1/2 -translate-x-1/2 z-[100] w-full max-w-fit px-4">
      <div className="bg-black/40 backdrop-blur-2xl border border-white/10 p-2 rounded-full flex items-center gap-2 shadow-2xl shadow-cyan-500/10">
        <div className="px-5 py-2 border-r border-white/10 mr-1 hidden sm:block">
          <span className="text-[11px] font-black tracking-[0.3em] text-cyan-400 uppercase">Nexus AI</span>
        </div>
        
        <div className="flex items-center gap-1">
          {sections.map((section) => (
            <a
              key={section.id}
              href={`#${section.id}`}
              onClick={(e) => {
                e.preventDefault();
                if (section.id === "blueprint") {
                  onViewChange?.("architecture");
                } else {
                  onViewChange?.("operations");
                  // Small delay to allow App.tsx to switch view before scrolling
                  setTimeout(() => {
                    document.getElementById(section.id)?.scrollIntoView({ behavior: "smooth" });
                  }, 10);
                }
                setActiveSection(section.id);
              }}
              className={`px-6 py-2.5 rounded-full text-[10px] font-black uppercase tracking-[0.15em] transition-all duration-300 ${
                activeSection === section.id
                  ? "bg-cyan-500/10 text-cyan-400 shadow-[inset_0_0_12px_rgba(34,211,238,0.2)] border border-cyan-500/20"
                  : "text-zinc-500 hover:text-zinc-200 border border-transparent"
              }`}
            >
              {section.label}
            </a>
          ))}
        </div>

        <div className="ml-2 pl-5 pr-4 border-l border-white/10 hidden lg:flex items-center gap-3">
          <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.5)]" />
          <span className="text-[9px] font-black text-zinc-500 uppercase tracking-widest">System Ready</span>
        </div>
      </div>
    </nav>
  );
};

export default PillNavbar;
