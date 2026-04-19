import React, { useState, useEffect, useMemo } from "react";
import { motion } from "framer-motion";
import { cn } from "../../lib/utils";

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
  const [isScrolled, setIsScrolled] = useState(false);

  const observerEntries = useMemo(() => sections.map(s => ({ id: s.id })), []);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
      
      if (activeSection === "blueprint") return;

      const scrollY = window.scrollY;
      const offset = window.innerHeight * 0.35;

      let current = "classify";

      for (const entry of observerEntries) {
        if (entry.id === "blueprint") continue;
        const el = document.getElementById(entry.id);
        if (!el) continue;
        
        const rect = el.getBoundingClientRect();
        const top = rect.top + scrollY;
        
        if (top - offset <= scrollY) {
          current = entry.id;
        }
      }

      if (current) setActiveSection(current);
    };

    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, [activeSection, observerEntries]);

  const handleNavClick = (sectionId: string, e: React.MouseEvent) => {
    e.preventDefault();
    if (sectionId === "blueprint") {
      onViewChange?.("architecture");
    } else {
      onViewChange?.("operations");
      setTimeout(() => {
        document.getElementById(sectionId)?.scrollIntoView({ behavior: "smooth" });
      }, 10);
    }
    setActiveSection(sectionId);
  };

  return (
    <header
      className={cn(
        "fixed z-[100] transition-all duration-500 ease-in-out",
        "inset-x-0 top-0 border-b border-white/10 bg-black/50 backdrop-blur-2xl backdrop-saturate-150 md:border-none md:bg-transparent md:backdrop-filter-none",
        "md:inset-x-auto md:left-1/2 md:-translate-x-1/2 md:w-auto md:max-w-[95%] xl:max-w-7xl",
        isScrolled ? "md:top-4" : "md:top-8"
      )}
    >
      <div
        className={cn(
          "flex items-center justify-between px-4 lg:px-6 transition-all duration-500 ease-in-out",
          "md:rounded-full md:border",
          isScrolled
            ? "py-2 md:bg-black/70 md:backdrop-blur-xl md:backdrop-saturate-150 md:shadow-2xl md:shadow-cyan-500/10 md:border-white/10"
            : "py-3 md:bg-transparent md:backdrop-blur-none md:shadow-none md:border-transparent"
        )}
      >
        {/* LOGO (Animated) */}
        <motion.a
          href="#classify"
          initial={{ letterSpacing: "0.2em" }}
          whileHover={{
            letterSpacing: "0.3em",
            textShadow: "0 0 20px rgba(34,211,238, 0.5)"
          }}
          transition={{ duration: 0.3 }}
          onClick={(e) => handleNavClick("classify", e)}
          className="font-black text-[11px] tracking-[0.2em] uppercase md:ml-4 md:mr-6 whitespace-nowrap cursor-pointer text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500"
        >
          Nexus AI
        </motion.a>

        {/* DESKTOP NAV (Framer Motion Pill) */}
        <nav className="hidden md:flex items-center gap-1 p-1">
          {sections.map((section) => (
            <a
              key={section.id}
              href={`#${section.id}`}
              onClick={(e) => handleNavClick(section.id, e)}
              className={cn(
                "relative group px-4 lg:px-6 py-2 text-[10px] uppercase tracking-[0.15em] font-black transition-colors duration-300 rounded-full cursor-pointer",
                activeSection === section.id
                  ? "text-cyan-400"
                  : "text-zinc-500 hover:text-zinc-200"
              )}
            >
              {activeSection === section.id && (
                <motion.div
                  layoutId="navbar-pill"
                  className="absolute inset-0 bg-cyan-500/10 rounded-full -z-10 shadow-[inset_0_0_12px_rgba(34,211,238,0.2)] border border-cyan-500/20"
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                />
              )}
              <motion.span
                initial={{ letterSpacing: "0.15em" }}
                animate={{ letterSpacing: activeSection === section.id ? "0.25em" : "0.15em" }}
                transition={{ duration: 0.3, ease: "easeOut" }}
                className="inline-block whitespace-nowrap"
              >
                {section.label}
              </motion.span>
            </a>
          ))}
        </nav>

        {/* ACTIONS (Right) */}
        <div className="ml-2 pl-5 pr-4 border-l border-white/10 hidden lg:flex items-center gap-3">
          <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.5)]" />
          <span className="text-[9px] font-black text-zinc-500 uppercase tracking-widest">System Ready</span>
        </div>

      </div>
    </header>
  );
};

export default PillNavbar;
