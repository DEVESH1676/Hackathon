/**
 * Nexus AI — Global Theme Configuration
 * Edit these values to change the entire application's aesthetic in one go.
 */

export const THEME = {
  // Brand Colors
  primary: "#22d3ee",    // Cyan (Active Pill, Logo, Glows)
  secondary: "#818cf8",  // Indigo (Accents, Gradients)
  accent: "#c084fc",     // Purple (Aurora, Highlights)
  
  // Neutral / Backgrounds
  background: "#09090b", // Zinc-950 (Deep Base)
  surface: "#18181b",    // Zinc-900 (Cards / Secondary Layers)
  
  // Status Colors
  success: "#10b981",    // Emerald
  warning: "#f59e0b",    // Amber
  danger: "#ef4444",     // Red
  
  // Glassmorphism Settings
  glass: {
    bg: "rgba(255, 255, 255, 0.03)",
    border: "rgba(255, 255, 255, 0.1)",
    glow: "rgba(34, 211, 238, 0.3)", // Glow intensity based on primary
  },
  
  // Typography
  text: {
    base: "#f8fafc",     // Slate-50
    muted: "#94a3b8",    // Slate-400
    dim: "#64748b",      // Slate-500
  },

  // Aurora Gradient Palette
  aurora: [
    "#0ea5e9", // Sky-500
    "#22d3ee", // Cyan-400
    "#818cf8", // Indigo-400
    "#c084fc", // Purple-400
    "#0ea5e9", // Back to Sky
  ]
};
