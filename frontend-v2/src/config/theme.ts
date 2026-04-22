/**
 * Nexus AI — Global Theme Configuration
 * Edit these values to change the entire application's aesthetic in one go.
 */

export const THEME = {
  // Brand Colors (Refined Saturation)
  primary: "#2dd4bf",    // Molten Teal (Sharper, more precise)
  secondary: "#6366f1",  // Electric Indigo
  accent: "#a855f7",     // Tech Purple

  // Neutral / Backgrounds (Deep Slate for maximum contrast)
  background: "#020617", // Slate-950 (Professional Deep Navy/Black)
  surface: "#0f172a",    // Slate-900 (Elevated Cards)

  // Status Colors (2026 Semantic Standards)
  success: "#00ffc2",    // Carbon Mint (The 2026 "Success" trend)
  warning: "#fbbf24",    // Amber
  danger: "#ff4757",     // Vibrant Coral-Red

  // Glassmorphism (Fluent Design 2.0 specs)
  glass: {
    bg: "rgba(15, 23, 42, 0.4)", // Slate-based transparency
    border: "rgba(255, 255, 255, 0.08)",
    glow: "rgba(45, 212, 191, 0.15)", // Subtle primary glow
  },

  // Typography
  text: {
    base: "#f1f5f9",     // Slate-100 (Slightly softer than pure Slate-50)
    muted: "#94a3b8",    // Slate-400
    dim: "#475569",      // Slate-600
  },

  aurora: ["#0ea5e9", "#2dd4bf", "#6366f1", "#a855f7", "#0ea5e9"]
};
