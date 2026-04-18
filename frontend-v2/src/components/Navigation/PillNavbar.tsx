import React, { useState, useEffect } from "react";

const sections = [
  { id: "classify", label: "Classification" },
  { id: "triage", label: "Triage" },
  { id: "rag", label: "RAG Evidence" },
  { id: "resolve", label: "Resolution" },
  { id: "judge", label: "Judge" },
  { id: "history", label: "History" },
  { id: "analytics", label: "Analytics" },
];

const PillNavbar: React.FC = () => {
  const [activeSection, setActiveSection] = useState("classify");

  useEffect(() => {
    const handleScroll = () => {
      const sectionElements = sections.map(s => document.getElementById(s.id));
      const currentSection = sectionElements.find(el => {
        if (!el) return false;
        const rect = el.getBoundingClientRect();
        return rect.top >= 0 && rect.top <= 400;
      });
      if (currentSection) setActiveSection(currentSection.id);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav className="fixed top-8 left-1/2 -translate-x-1/2 z-[100]">
      <div className="bg-black/40 backdrop-blur-2xl border border-white/10 p-1.5 rounded-full flex items-center gap-1 shadow-2xl shadow-cyan-500/10">
        <div className="px-4 py-2 border-r border-white/5 mr-1 hidden md:block">
          <span className="text-[10px] font-black tracking-[0.2em] text-cyan-400 uppercase">Nexus AI</span>
        </div>
        
        {sections.map((section) => (
          <a
            key={section.id}
            href={`#${section.id}`}
            onClick={(e) => {
              e.preventDefault();
              document.getElementById(section.id)?.scrollIntoView({ behavior: "smooth" });
              setActiveSection(section.id);
            }}
            className={`px-4 py-2 rounded-full text-[10px] font-bold uppercase tracking-wider transition-all duration-300 ${
              activeSection === section.id
                ? "bg-cyan-500/10 text-cyan-400 shadow-[inset_0_0_12px_rgba(34,211,238,0.2)]"
                : "text-zinc-500 hover:text-zinc-300"
            }`}
          >
            {section.label}
          </a>
        ))}

        <div className="ml-1 pl-4 pr-3 border-l border-white/5 hidden lg:flex items-center gap-2">
          <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-[9px] font-bold text-zinc-500 uppercase tracking-widest">System Ready</span>
        </div>
      </div>
    </nav>
  );
};

export default PillNavbar;
