"""
⚡ Nexus AI Ticket Intelligence Platform — v3.0
Streamlit Dashboard with 5-Tab Progressive Disclosure UI (Refined)

Tab 1: 🎫 Submit Ticket — pipeline control center
Tab 2: 🧠 Classification — cascade result, confidence, novelty flag
Tab 3: 🔍 RAG Evidence — ranked chunks with multi-hop results and scores
Tab 4: 🤖 Agent Decisions — triage routing, automation discovery
Tab 5: ⚖️ Resolution + Judge — resolution steps, rubric scores, safety gate
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

# ── Premium Visualization Palette ──────────────────────────────
PLOTLY_THEME = {
    "background": "rgba(0,0,0,0)",
    "text": "#94a3b8",
    "accent_indigo": "#6366f1",
    "accent_cyan": "#22d3ee",
    "accent_purple": "#a855f7",
    "accent_green": "#4ade80",
    "accent_amber": "#fbbf24",
    "accent_red": "#f87171",
    "grid": "rgba(255,255,255,0.05)",
    "palette": ["#6366f1", "#22d3ee", "#a855f7", "#4ade80", "#fbbf24", "#f87171"]
}

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Nexus AI — Ticket Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Premium Glassmorphism CSS System ─────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', -apple-system, sans-serif; }
    
    /* ═══════════════════════════════════════════════════════════
       SECTION 1: AURORA DYNAMIC ENVIRONMENT (Task 7.1.1)
       ═══════════════════════════════════════════════════════════ */
    @keyframes auroraBreathing {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: linear-gradient(-45deg, #0d0e17, #111222, #1a1c2c, #0d0e17);
        background-size: 400% 400%;
        animation: auroraBreathing 20s ease infinite;
        color: #e2e8f0;
    }
    
    /* ── Header Overrides & Theme fix ── */
    [data-testid="stHeader"] { display: none !important; height: 0 !important; }
    .stApp > header { display: none !important; }
    .block-container { padding-top: 5rem !important; padding-bottom: 2rem; max-width: 1300px; }
    
    /* ═══════════════════════════════════════════════════════════
       SECTION 2: CORE GLASSMORPHISM MATERIAL (Task 7.1.2)
       ═══════════════════════════════════════════════════════════ */
    .glass {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px; padding: 20px;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .glass:hover {
        border-color: rgba(129, 140, 248, 0.3);
        box-shadow: 0 15px 40px -10px rgba(99, 102, 241, 0.2), inset 0 1px 0 rgba(255,255,255,0.15);
        transform: translateY(-4px) scale(1.02);
    }
    .glass-accent {
        background: rgba(99, 102, 241, 0.04);
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 16px; padding: 24px;
        box-shadow: 0 10px 30px -10px rgba(99,102,241,0.1), inset 0 1px 0 rgba(255,255,255,0.08);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .glass-accent:hover {
        border-color: rgba(129, 140, 248, 0.4);
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 20px 40px -10px rgba(99, 102, 241, 0.3);
    }
    
    /* ── Form & Status Box — Frosted Glass ── */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1) !important;
        transition: transform 0.3s ease, border-color 0.3s ease !important;
    }
    [data-testid="stStatusWidget"] {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(99,102,241,0.15) !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 12px rgba(99,102,241,0.08) !important;
        padding: 8px 16px !important;
        margin-bottom: 16px !important;
    }

    /* ═══════════════════════════════════════════════════════════
       SECTION 3: ELITE FLOATING PILL NAVBAR (The "Glide" Edition)
       Ported from React/Tailwind — High-fidelity floating glass
       ═══════════════════════════════════════════════════════════ */
    
    /* ── 3A: The Global "Floating Pill" Container ── */
    div[data-testid="stTabs"] {
        position: fixed !important;
        top: 20px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: auto !important;
        max-width: 95% !important;
        z-index: 99998 !important;
        padding: 0 !important;
    }
    
    [data-baseweb="tab-list"] {
        background: rgba(13, 14, 23, 0.5) !important;
        backdrop-filter: blur(24px) saturate(150%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(150%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 9999px !important; /* Full Pill */
        padding: 6px 10px !important;
        gap: 6px !important;
        box-shadow: 
            0 10px 15px -3px rgba(0, 0, 0, 0.1),
            0 4px 6px -2px rgba(0, 0, 0, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        border-bottom: none !important;
        display: flex !important;
        align-items: center !important;
        position: relative !important;
    }
    
    /* ── 3B: Branding Injection (The Logo) ── */
    [data-baseweb="tab-list"]::before {
        content: "Nexus AI" !important;
        color: #f8fafc !important;
        font-weight: 800 !important;
        font-size: 0.9rem !important;
        letter-spacing: -0.02em !important;
        margin-right: 24px !important;
        margin-left: 12px !important;
        flex-shrink: 0 !important;
        background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* ── 3C: Utility Injection (The "Status" Action) ── */
    [data-baseweb="tab-list"]::after {
        content: "Status: Online" !important;
        color: #818cf8 !important;
        font-weight: 600 !important;
        font-size: 0.72rem !important;
        margin-left: 20px !important;
        margin-right: 10px !important;
        padding: 6px 14px !important;
        border-radius: 9999px !important;
        background: #090a10 !important;
        position: relative !important;
        display: inline-flex !important;
        align-items: center !important;
        cursor: pointer !important;
        border: 1px solid transparent !important;
        /* Holographic Border Hack */
        background-image: linear-gradient(#090a10, #090a10),
                           linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        background-origin: border-box !important;
        background-clip: padding-box, border-box !important;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.2) !important;
        white-space: nowrap !important;
        transition: all 0.3s ease !important;
    }
    
    /* ── 3D: Navigation Items ("The Grip") ── */
    [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        border-radius: 9999px !important;
        padding: 8px 20px !important;
        margin: 0 !important;
        color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 500 !important;
        font-size: 0.82rem !important;
        transition: all 0.3s ease-in-out !important;
        white-space: nowrap !important;
        height: auto !important;
    }
    
    /* Inactive Hover */
    [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #fff !important;
    }
    
    /* ── 3E: Active Tab ("The Glide") ── */
    [data-baseweb="tab"][aria-selected="true"] {
        background: rgba(59, 130, 246, 0.1) !important;
        color: #3b82f6 !important;
        font-weight: 600 !important;
        box-shadow: inset 0 0 10px rgba(59, 130, 246, 0.2) !important;
        letter-spacing: 0.01em !important;
    }
    
    /* ── 3F: Cleaning the DOM (Removing Streamlit Defaults) ── */
    [data-baseweb="tab-highlight"] {
        display: none !important;
        height: 0px !important;
        border: none !important;
    }
    [data-baseweb="tab-border"] {
        display: none !important;
        height: 0px !important;
    }
    
    /* ── 3G: Content Offset ── */
    [data-baseweb="tab-panel"] {
        padding-top: 15px !important;
        animation: fadeIn 0.5s ease-out forwards;
    }
    
    /* ── 3H: Mobile Responsiveness Fix ── */
    @media (max-width: 768px) {
        div[data-testid="stTabs"] {
            position: relative !important;
            top: 0 !important;
            left: 0 !important;
            transform: none !important;
            width: 100% !important;
            max-width: 100% !important;
            margin-bottom: 20px !important;
        }
        [data-baseweb="tab-list"] {
            border-radius: 12px !important;
            flex-wrap: wrap !important;
            justify-content: center !important;
        }
        [data-baseweb="tab-list"]::before,
        [data-baseweb="tab-list"]::after {
            display: none !important;
        }
    }

    /* ═══════════════════════════════════════════════════════════
       SECTION 4: SIDEBAR RECOVERY PROTOCOL (Task 7.1.4)
       ═══════════════════════════════════════════════════════════ */
    [data-testid="collapsedControl"] {
        z-index: 99999 !important;
        position: fixed !important;
        top: 20px !important;
        left: 20px !important;
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        border: 1px solid rgba(168, 85, 247, 0.4) !important;
        border-radius: 50% !important;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="collapsedControl"]:hover {
        box-shadow: 0 0 25px rgba(168, 85, 247, 0.6) !important;
        transform: scale(1.1) !important;
    }
    
    section[data-testid="stSidebar"] {
        background: rgba(10, 14, 26, 0.6) !important;
        backdrop-filter: blur(30px) !important;
        -webkit-backdrop-filter: blur(30px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 24px !important;
        margin: 20px !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h4 {
        color: #94a3b8 !important; font-size: 0.75rem !important;
        text-transform: uppercase !important; letter-spacing: 0.1em !important;
        font-weight: 600 !important;
    }

    /* ═══════════════════════════════════════════════════════════
       SECTION 5: INPUTS & BUTTONS (Task 7.1.5)
       ═══════════════════════════════════════════════════════════ */
    .stTextInput input, .stTextArea textarea {
        background: #090a10 !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2) !important;
        background: #0c0d14 !important;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #475569 !important;
    }
    
    /* ── Form Submit Button ── */
    [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        height: 3.5rem !important;
        letter-spacing: 0.5px !important;
        transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease !important;
    }
    [data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 25px -5px rgba(168, 85, 247, 0.5) !important;
    }
    
    /* ── Primary Button (general) ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%) !important;
        color: white !important; font-weight: 600 !important; font-size: 0.9rem !important;
        border: none !important; border-radius: 10px !important;
        padding: 12px 24px !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 12px rgba(99,102,241,0.25) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(99,102,241,0.4) !important;
    }

    /* ═══════════════════════════════════════════════════════════
       SECTION 6: UX & DEEP GLASSMORPHISM (Task 7.2 & 7.3)
       ═══════════════════════════════════════════════════════════ */
    
    /* ── Floating Action Button (FAB) ── */
    .fab-glass {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        z-index: 9999;
        font-size: 1.5rem;
    }
    .fab-glass:hover {
        transform: scale(1.1) rotate(10deg);
        background: rgba(99, 102, 241, 0.4);
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
    }

    /* ── Command Palette Pill ── */
    .cmd-palette {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 9999px !important;
        padding: 4px 12px !important;
        transition: all 0.3s ease !important;
    }
    .cmd-palette:focus-within {
        border-color: #818cf8 !important;
        box-shadow: 0 0 15px rgba(129, 140, 248, 0.3) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }

    /* ── Keyboard Shortcut Tooltip ── */
    .shortcut-badge {
        position: fixed;
        bottom: 30px;
        left: 30px;
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 8px 12px;
        font-size: 0.7rem;
        color: #64748b;
        cursor: help;
        transition: all 0.3s ease;
        z-index: 999;
    }
    .shortcut-badge:hover {
        color: #e2e8f0;
        background: rgba(0, 0, 0, 0.6);
    }

    /* ── Dynamic Status Processing ── */
    .status-processing {
        animation: pulseGlow 2s infinite !important;
        color: #fbbf24 !important;
        background: rgba(251, 191, 36, 0.1) !important;
    }

    /* ── Frosted Modal Overlay ── */
    .frosted-modal {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        z-index: 10000;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.3s ease forwards;
    }

    /* ── Animations ── */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 15px rgba(99, 102, 241, 0.15); }
        50% { box-shadow: 0 0 30px rgba(99, 102, 241, 0.35); }
    }
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes borderPulse {
        0%, 100% { border-color: rgba(99, 102, 241, 0.2); }
        50% { border-color: rgba(99, 102, 241, 0.5); }
    }
    
    .animate-in { animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    .fade-in { animation: fadeIn 0.4s ease forwards; }
    
    /* Staggered Entrance Delays */
    .delay-1 { animation-delay: 0.1s; }
    .delay-2 { animation-delay: 0.2s; }
    .delay-3 { animation-delay: 0.3s; }
    .delay-4 { animation-delay: 0.4s; }
    .delay-5 { animation-delay: 0.5s; }
    
    /* ── Prevent overflow ── */
    .stMarkdown p, .stMarkdown div {
        word-wrap: break-word; overflow-wrap: break-word;
    }

    /* ── Section Headers ── */
    .section-title {
        font-size: 1.1rem; font-weight: 600; color: #e2e8f0;
        letter-spacing: -0.02em; margin-bottom: 16px;
        padding-bottom: 10px; border-bottom: 1px solid rgba(148,163,184,0.1);
    }
    .section-icon { margin-right: 8px; }
    
    /* ── Metric Cards ── */
    .metric-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px; padding: 20px 24px; text-align: center;
        transition: all 0.3s ease;
        position: relative; overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, rgba(129,140,248,0.5), transparent);
        opacity: 0; transition: opacity 0.3s ease;
    }
    .metric-card:hover { 
        transform: translateY(-4px);
        border-color: rgba(129, 140, 248, 0.2);
    }
    .metric-card:hover::before { opacity: 1; }
    .metric-val { color: #f8fafc; margin: 0; font-size: 1.8rem; font-weight: 700; letter-spacing: -0.02em; }
    .metric-label { color: #64748b; margin: 4px 0 0; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; }
    
    /* ── KV Row (Key-Value) ── */
    .kv {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 0; border-bottom: 1px solid rgba(148,163,184,0.06);
    }
    .kv:last-child { border-bottom: none; }
    .kv-key { color: #64748b; font-size: 0.85rem; font-weight: 500; }
    .kv-val { font-weight: 600; font-size: 0.9rem; }

    /* ── Badges ── */
    .pill {
        padding: 5px 14px; border-radius: 100px; font-size: 0.78rem; font-weight: 600;
        display: inline-flex; align-items: center; gap: 5px;
        letter-spacing: 0.02em;
    }
    .pill-green { background: rgba(34,197,94,0.12); color: #4ade80; border: 1px solid rgba(34,197,94,0.2); }
    .pill-amber { background: rgba(245,158,11,0.12); color: #fbbf24; border: 1px solid rgba(245,158,11,0.2); }
    .pill-red { background: rgba(239,68,68,0.12); color: #f87171; border: 1px solid rgba(239,68,68,0.2); }
    .pill-purple { background: rgba(168,85,247,0.12); color: #c084fc; border: 1px solid rgba(168,85,247,0.2); }
    .pill-blue { background: rgba(59,130,246,0.12); color: #60a5fa; border: 1px solid rgba(59,130,246,0.2); }
    .pill-indigo { background: rgba(99,102,241,0.12); color: #818cf8; border: 1px solid rgba(99,102,241,0.2); }

    /* ── Priority Badges ── */
    .pri { padding: 3px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; }
    .pri-p1 { background: rgba(220,38,38,0.15); color: #fca5a5; }
    .pri-p2 { background: rgba(249,115,22,0.15); color: #fdba74; }
    .pri-p3 { background: rgba(59,130,246,0.15); color: #93c5fd; }
    .pri-p4 { background: rgba(34,197,94,0.15); color: #86efac; }

    /* ── Banners ── */
    .banner-danger {
        background: linear-gradient(135deg, rgba(127,29,29,0.5), rgba(153,27,27,0.2));
        border: 1px solid rgba(239,68,68,0.2); border-radius: 12px;
        padding: 16px 20px; animation: borderPulse 3s infinite;
    }
    .banner-info {
        background: linear-gradient(135deg, rgba(30,58,138,0.4), rgba(30,64,175,0.2));
        border: 1px solid rgba(59,130,246,0.2); border-radius: 12px;
        padding: 16px 20px;
    }
    .banner-success {
        background: linear-gradient(135deg, rgba(21,128,61,0.3), rgba(22,163,74,0.15));
        border: 1px solid rgba(34,197,94,0.2); border-radius: 12px;
        padding: 16px 20px;
    }
    
    /* ── Expander ── */
    .streamlit-expanderHeader { font-size: 0.85rem !important; font-weight: 500 !important; }
    
    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.2); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.3); }

    /* ── Pipeline Step Indicator ── */
    .step-flow {
        display: flex; align-items: center; gap: 4px;
        padding: 8px 0; flex-wrap: wrap;
    }
    .step {
        padding: 4px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 600;
        letter-spacing: 0.03em;
    }
    .step-done { background: rgba(34,197,94,0.1); color: #4ade80; }
    .step-active { background: rgba(99,102,241,0.15); color: #818cf8; animation: borderPulse 2s infinite; border: 1px solid rgba(99,102,241,0.3); }
    .step-pending { background: rgba(51,65,85,0.3); color: #475569; }
    .step-arrow { color: #334155; font-size: 0.7rem; }
    
    /* ── Score Ring ── */
    .score-ring {
        width: 80px; height: 80px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem; font-weight: 700; margin: 0 auto 8px;
    }
</style>
""", unsafe_allow_html=True)


# ── Cached Model Loading ─────────────────────────────────────
@st.cache_resource(show_spinner="Initializing classification engine...")
def load_classifier():
    from core.classifier import TicketClassifier
    return TicketClassifier()

@st.cache_resource(show_spinner="Loading RAG retrieval engine...")
def load_rag_engine():
    from core.rag import ResolutionEngine
    return ResolutionEngine()

@st.cache_resource(show_spinner="Spawning agent workers...")
def load_agents():
    from core.agent import AgenticLayer, TriageAgent, ResolutionAgent, AutomationDiscoveryAgent
    return AgenticLayer(), TriageAgent(), ResolutionAgent(), AutomationDiscoveryAgent()

@st.cache_resource(show_spinner="Initializing quality judge...")
def load_judge():
    from core.judge import ResolutionJudge
    return ResolutionJudge()

@st.cache_data(show_spinner=False)
def load_ticket_data():
    for fname in ["synthetic_tickets_merged.csv", "synthetic_tickets.csv"]:
        csv_path = os.path.join(os.path.dirname(__file__), "data", fname)
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path)
    return pd.DataFrame()


# ── Session State ────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False


# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 16px;">
        <div style="font-size: 1.6rem; font-weight: 800; letter-spacing: -0.03em;
                    background: linear-gradient(135deg, #818cf8, #c084fc, #f472b6);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Nexus AI
        </div>
        <div style="color: #475569; font-size: 0.8rem; font-weight: 500; margin-top: 2px;">
            Ticket Intelligence Platform · v3.0
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("#### Pipeline Controls")
    generate_resolution = st.toggle("Enable Full Resolution", value=True,
        help="Run Resolution Agent + LLM-as-Judge quality evaluation"
    )
    
    st.divider()
    
    st.markdown("#### System Info")
    llm_label = f"Groq · {config.GROQ_MODEL}" if config.USE_GROQ else f"Ollama · {config.OLLAMA_MODEL}"
    st.markdown(f"""
    <div style="font-size: 0.78rem; color: #475569; line-height: 1.8;">
        <div><span style="color:#64748b;">LLM</span> <span style="color:#818cf8; font-weight:500;">{llm_label}</span></div>
        <div><span style="color:#64748b;">Embed</span> <span style="color:#c084fc; font-weight:500;">{config.EMBEDDING_MODEL_NAME}</span></div>
        <div><span style="color:#64748b;">Vector DB</span> <span style="color:#4ade80; font-weight:500;">ChromaDB Local</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Session stats
    session_count = len(st.session_state.history)
    if session_count > 0:
        escalated = sum(1 for h in st.session_state.history if h.get("escalated"))
        st.markdown(f"""
        <div style="font-size: 0.78rem; color: #475569; line-height: 1.8;">
            <div>Tickets analyzed: <span style="color:#e2e8f0; font-weight:600;">{session_count}</span></div>
            <div>Escalations: <span style="color:#f87171; font-weight:600;">{escalated}</span></div>
        </div>
        """, unsafe_allow_html=True)


# ── Helper Functions ─────────────────────────────────────────
def priority_pill(priority: str) -> str:
    p = priority.lower()
    if "p1" in p or "critical" in p: return f'<span class="pri pri-p1">P1 Critical</span>'
    if "p2" in p or "high" in p:     return f'<span class="pri pri-p2">P2 High</span>'
    if "p3" in p or "medium" in p:   return f'<span class="pri pri-p3">P3 Medium</span>'
    return f'<span class="pri pri-p4">P4 Low</span>'

def conf_color(c: float) -> str:
    if c >= 0.8: return "#4ade80"
    if c >= 0.6: return "#fbbf24"
    return "#f87171"

def score_color(s) -> str:
    s = float(s) if s else 0
    if s >= 4: return "#4ade80"
    if s >= 3: return "#fbbf24"
    return "#f87171"

def cascade_pill(method: str) -> str:
    pills = {
        "centroid": ("FAST PATH", "pill-green"),
        "llm_judge": ("LLM JUDGE", "pill-amber"),
        "escalated": ("ESCALATED", "pill-red"),
        "novel_ticket": ("NOVEL", "pill-purple"),
        "similarity_search": ("SIMILARITY", "pill-blue"),
    }
    text, cls = pills.get(method, ("UNKNOWN", "pill-blue"))
    return f'<span class="pill {cls}">{text}</span>'

def decision_pill(decision: str) -> str:
    pills = {
        "AUTO_ROUTE": "pill-green",
        "ROUTE_WITH_LLM_ASSIST": "pill-amber",
        "ESCALATE_LOW_CONFIDENCE": "pill-red",
        "ESCALATE_NOVEL": "pill-purple",
    }
    cls = pills.get(decision, "pill-blue")
    return f'<span class="pill {cls}">{decision}</span>'

def render_rubric_bar(label: str, score, max_s: int = 5) -> str:
    s = int(score) if score else 0
    pct = (s / max_s) * 100
    color = score_color(s)
    return f"""
    <div style="margin-bottom: 14px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
            <span style="color:#94a3b8; font-size:0.82rem; font-weight:500;">{label}</span>
            <span style="color:{color}; font-weight:700; font-size:0.85rem; font-family:'JetBrains Mono';">{s}/{max_s}</span>
        </div>
        <div style="background:rgba(51,65,85,0.4); border-radius:6px; overflow:hidden; height:6px;">
            <div style="width:{pct}%; height:100%; background:linear-gradient(90deg, {color}, {color}88);
                        border-radius:6px; transition: width 0.5s ease;"></div>
        </div>
    </div>
    """


# ── Full Pipeline ────────────────────────────────────────────
def run_full_pipeline(title: str, desc: str, enable_rag: bool):
    st.session_state.is_processing = True
    result = {}
    
    with st.status("Running intelligence pipeline...", expanded=True) as status:
        st.write("⬡ Extracting semantic embeddings...")
        clf = load_classifier()
        classification = clf.classify(title, desc)
        result["classification"] = classification
        time.sleep(0.2)
        
        st.write("⬡ Triage agent routing...")
        _, triage_agent, res_agent, auto_agent = load_agents()
        ticket = {"title": title, "description": desc}
        triage_result = triage_agent.run(ticket, classification)
        result["triage"] = triage_result
        time.sleep(0.15)
        
        st.write("⬡ Retrieving & ranking historical evidence...")
        rag = load_rag_engine()
        rag_result = rag.suggest_resolution(title, desc)
        result["rag"] = rag_result
        query_embedding = rag.embedding_model.encode(f"{title} {desc}").tolist()
        raw_results = rag.collection.query(
            query_embeddings=[query_embedding], n_results=6,
            include=["documents", "metadatas", "distances"]
        )
        ranked_chunks = rag._rank_retrieved_chunks(raw_results)[:3]
        result["ranked_chunks"] = ranked_chunks
        time.sleep(0.15)
        
        if enable_rag:
            st.write("⬡ Resolution agent generating fix...")
            res_result = res_agent.run(ticket, ranked_chunks)
            result["resolution"] = res_result
            time.sleep(0.15)
            
            st.write("⬡ Quality judge evaluating resolution...")
            judge = load_judge()
            resolution_text = "\n".join(res_result.get("resolution_steps", []))
            judge_result = judge.judge(
                {"title": title, "description": desc, "category": classification.get("category", "Unknown")},
                resolution_text
            )
            result["judge"] = judge_result
            time.sleep(0.15)
            
            st.write("⬡ Scanning for automation patterns...")
            auto_result = auto_agent.run({
                "title": title, "description": desc,
                "category": classification.get("category", "Unknown"),
                "resolution": resolution_text,
            })
            result["automation"] = auto_result
        else:
            result["resolution"] = None
            result["judge"] = None
            auto_result = auto_agent.run({
                "title": title, "description": desc,
                "category": classification.get("category", "Unknown"),
                "resolution": "",
            })
            result["automation"] = auto_result
        
        status.update(label="Pipeline complete", state="complete", expanded=False)
    
    st.session_state.is_processing = False
    result["title"] = title
    result["description"] = desc
    return result


# ── 5-Tab Layout ─────────────────────────────────────────────
tab_submit, tab_classify, tab_rag, tab_agent, tab_judge = st.tabs([
    "Submit Ticket", "Classification", "RAG Evidence",
    "Agent Decisions", "Resolution + Judge"
])


# ━━━ TAB 1: SUBMIT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_submit:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_input, col_result = st.columns([1.3, 1], gap="large")
    
    with col_input:
        with st.form("ticket_form", clear_on_submit=False):
            st.markdown('<div class="section-title" style="margin-top:-10px;"><span class="section-icon">📝</span>New Ticket</div>', unsafe_allow_html=True)
            ticket_title = st.text_input(
                "Subject",
                placeholder="VPN connection drops after 5 minutes with error 619"
            )
            ticket_desc = st.text_area(
                "Description",
                placeholder="Provide full context: error messages, affected users, timestamps, recent changes...",
                height=265
            )
            submitted = st.form_submit_button("Launch Intelligence Pipeline", use_container_width=True, type="primary")
    
    with col_result:
        if submitted and ticket_title and ticket_desc:
            result = run_full_pipeline(ticket_title, ticket_desc, generate_resolution)
            st.session_state.pipeline_result = result
            
            clf = result["classification"]
            judge = result.get("judge", {})
            triage = result.get("triage", {})
            
            # Pipeline summary card
            gate = judge.get("safety_gate", "N/A") if judge else "N/A"
            gate_color = "#4ade80" if gate == "PASS" else ("#f87171" if gate == "BLOCKED" else "#64748b")
            
            st.markdown(f"""
            <div class="glass-accent animate-in delay-1" style="margin-bottom: 16px;">
                <div class="section-title" style="margin-bottom: 14px; border: none; padding: 0;">
                    <span class="section-icon">⚡</span>Pipeline Result
                </div>
                <div class="kv">
                    <span class="kv-key">Category</span>
                    <span class="kv-val" style="color:#c084fc;">{clf.get('category', 'N/A')}</span>
                </div>
                <div class="kv">
                    <span class="kv-key">Confidence</span>
                    <span class="kv-val" style="color:{conf_color(clf.get('confidence', 0))}; font-family:'JetBrains Mono';">
                        {clf.get('confidence', 0):.1%}
                    </span>
                </div>
                <div class="kv">
                    <span class="kv-key">Route To</span>
                    <span class="kv-val" style="color:#e2e8f0;">{clf.get('department', 'N/A')}</span>
                </div>
                <div class="kv">
                    <span class="kv-key">Cascade</span>
                    {cascade_pill(clf.get('method', 'centroid'))}
                </div>
                <div class="kv">
                    <span class="kv-key">Triage</span>
                    {decision_pill(triage.get('decision', 'N/A'))}
                </div>
                <div class="kv">
                    <span class="kv-key">Safety Gate</span>
                    <span class="kv-val" style="color:{gate_color}; font-weight:700;">{gate}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Pipeline step indicator
            steps_html = ""
            stages = ["Classify", "Triage", "RAG", "Resolve", "Judge", "Auto"]
            for i, s in enumerate(stages):
                steps_html += f'<span class="step step-done">{s}</span>'
                if i < len(stages) - 1:
                    steps_html += '<span class="step-arrow">→</span>'
            
            st.markdown(f'<div class="step-flow" style="margin-top:8px;">{steps_html}</div>', unsafe_allow_html=True)
            
            st.markdown('<p style="color:#475569; font-size:0.8rem; margin-top:12px;">Navigate tabs to inspect each stage →</p>', unsafe_allow_html=True)
            
            # Save to history
            st.session_state.history.append({
                "title": ticket_title,
                "category": clf.get("category"),
                "department": clf.get("department"),
                "confidence": clf.get("confidence"),
                "priority": clf.get("priority_suggestion", "P3 Medium"),
                "method": clf.get("method"),
                "safety_gate": gate,
                "escalated": triage.get("escalate", False),
            })
            st.toast("Pipeline complete", icon="✅")
            
        elif submitted:
            st.error("Please provide both a subject and description.")
        
        elif st.session_state.pipeline_result is None:
            st.markdown("""
            <div class="glass" style="text-align:center; padding: 48px 24px;">
                <div style="font-size: 2.5rem; margin-bottom: 12px; opacity: 0.4;">⚡</div>
                <p style="color:#64748b; font-size: 0.9rem; font-weight: 500; margin: 0;">
                    Submit a ticket to engage the pipeline
                </p>
                <p style="color:#334155; font-size: 0.78rem; margin-top: 8px;">
                    Classify → Triage → RAG → Resolve → Judge → Automate
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Show previous result
            clf = st.session_state.pipeline_result["classification"]
            judge = st.session_state.pipeline_result.get("judge", {})
            triage = st.session_state.pipeline_result.get("triage", {})
            gate = judge.get("safety_gate", "N/A") if judge else "N/A"
            gate_color = "#4ade80" if gate == "PASS" else ("#f87171" if gate == "BLOCKED" else "#64748b")
            
            st.markdown(f"""
            <div class="glass-accent animate-in delay-1">
                <div class="section-title" style="margin-bottom: 14px; border: none; padding: 0;">
                    <span class="section-icon">⚡</span>Last Pipeline Result
                </div>
                <div class="kv">
                    <span class="kv-key">Category</span>
                    <span class="kv-val" style="color:#c084fc;">{clf.get('category', 'N/A')}</span>
                </div>
                <div class="kv">
                    <span class="kv-key">Confidence</span>
                    <span class="kv-val" style="color:{conf_color(clf.get('confidence', 0))}; font-family:'JetBrains Mono';">{clf.get('confidence', 0):.1%}</span>
                </div>
                <div class="kv">
                    <span class="kv-key">Safety Gate</span>
                    <span class="kv-val" style="color:{gate_color}; font-weight:700;">{gate}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ━━━ TAB 2: CLASSIFICATION ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_classify:
    st.markdown("<br>", unsafe_allow_html=True)
    pr = st.session_state.pipeline_result
    
    if pr is None:
        st.info("Submit a ticket first to see classification results.")
    else:
        clf = pr["classification"]
        conf = clf.get("confidence", 0)
        cat = clf.get("category", "Unknown")
        method = clf.get("method", "centroid")
        is_novel = clf.get("is_novel", False)
        
        # Top cascade badge
        st.markdown(f'<div style="text-align:center; margin-bottom:20px;">{cascade_pill(method)}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown(f"""
            <div class="glass animate-in delay-1">
                <div class="section-title"><span class="section-icon">🎯</span>Classification Result</div>
                <div class="kv">
                    <span class="kv-key">Category</span>
                    <span class="kv-val" style="color:#c084fc;">{cat}</span>
                </div>
                <div class="kv">
                    <span class="kv-key">Department</span>
                    <span class="kv-val" style="color:#e2e8f0;">{clf.get('department', 'N/A')}</span>
                </div>
                <div class="kv">
                    <span class="kv-key">Confidence</span>
                    <span class="kv-val" style="color:{conf_color(conf)}; font-family:'JetBrains Mono';">{conf:.1%}</span>
                </div>
                <div class="kv">
                    <span class="kv-key">Cascade Path</span>
                    {cascade_pill(method)}
                </div>
                <div class="kv">
                    <span class="kv-key">Novel Ticket</span>
                    <span class="kv-val" style="color:{'#c084fc' if is_novel else '#4ade80'};">{'Yes' if is_novel else 'No'}</span>
                </div>
                <div class="kv">
                    <span class="kv-key">Priority</span>
                    {priority_pill(clf.get('priority_suggestion', 'P3 Medium'))}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Sankey Flow Visualization ──
            st.markdown('<div class="glass animate-in delay-3"><div class="section-title"><span class="section-icon">🌊</span>Intelligence Flow</div>', unsafe_allow_html=True)
            
            # Define nodes
            nodes = ["Ticket", "Classifier", "Agent", "Resolution"]
            node_colors = [PLOTLY_THEME["accent_cyan"], PLOTLY_THEME["accent_purple"], PLOTLY_THEME["accent_indigo"], PLOTLY_THEME["accent_green"]]
            
            # Define links
            links = [
                {"source": 0, "target": 1, "value": 1, "label": "Input"},
                {"source": 1, "target": 2, "value": 1, "label": "Triage"},
                {"source": 2, "target": 3, "value": 1, "label": "Solve"}
            ]
            
            sankey_fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=15, thickness=20, line=dict(color="black", width=0.5),
                    label=nodes, color=node_colors
                ),
                link=dict(
                    source=[l["source"] for l in links],
                    target=[l["target"] for l in links],
                    value=[l["value"] for l in links],
                    color="rgba(99, 102, 241, 0.2)"
                )
            )])
            
            sankey_fig.update_layout(
                height=200, margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor=PLOTLY_THEME["background"],
                font=dict(color=PLOTLY_THEME["text"], size=10)
            )
            st.plotly_chart(sankey_fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
            
            llm_rationale = clf.get("llm_rationale")
            if llm_rationale:
                st.markdown(f"""
                <div style="background:rgba(245,158,11,0.06); border:1px solid rgba(245,158,11,0.12);
                            border-radius:10px; padding:14px 16px; margin-top:12px;
                            color:#fde68a; font-size:0.84rem; line-height:1.6;">
                    <strong style="color:#fbbf24;">LLM Judge Rationale</strong><br>
                    <span style="color:#cbd5e1;">{llm_rationale}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            scores = clf.get("all_scores", {})
            if scores:
                sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1]))
                
                fig = go.Figure(go.Bar(
                    x=list(sorted_scores.values()),
                    y=list(sorted_scores.keys()),
                    orientation='h',
                    marker=dict(
                        color=[PLOTLY_THEME["accent_purple"] if k == cat else 'rgba(51,65,85,0.5)' for k in sorted_scores.keys()],
                        line=dict(width=0)
                    ),
                    text=[f"{v:.0%}" for v in sorted_scores.values()],
                    textposition='outside',
                    textfont=dict(color=PLOTLY_THEME["text"], size=12, family="JetBrains Mono")
                ))
                fig.update_layout(
                    height=260, margin=dict(l=0, r=50, t=8, b=0),
                    paper_bgcolor=PLOTLY_THEME["background"], plot_bgcolor=PLOTLY_THEME["background"],
                    font=dict(color=PLOTLY_THEME["text"], size=12, family="Inter"),
                    xaxis=dict(showgrid=False, range=[0, 1], visible=False),
                    yaxis=dict(showgrid=False, tickfont=dict(size=13, family="Inter"))
                )
                st.markdown('<div class="glass animate-in delay-2"><div class="section-title"><span class="section-icon">📊</span>Confidence Scores</div>', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                st.markdown('</div>', unsafe_allow_html=True)


# ━━━ TAB 3: RAG EVIDENCE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_rag:
    st.markdown("<br>", unsafe_allow_html=True)
    pr = st.session_state.pipeline_result
    
    if pr is None:
        st.info("Submit a ticket first to see RAG evidence.")
    else:
        ranked_chunks = pr.get("ranked_chunks", [])
        
        if not ranked_chunks:
            st.warning("No similar tickets found in the vector store.")
        else:
            st.markdown('<div class="section-title"><span class="section-icon">🏆</span>Ranked Evidence — Hop 1</div>', unsafe_allow_html=True)
            st.markdown('<p style="color:#475569; font-size:0.78rem; margin-top:-10px; margin-bottom:16px;">Scoring: Semantic (60%) · Recency (20%) · Outcome (20%)</p>', unsafe_allow_html=True)
            
            for i, chunk in enumerate(ranked_chunks):
                sem = chunk.get("semantic", 0)
                rec = chunk.get("recency", 0)
                out = chunk.get("outcome", 0)
                final = chunk.get("final_score", 0)
                meta = chunk.get("metadata", {})
                
                sc = score_color(final * 5)  # normalize 0-1 to 0-5 scale for color
                
                st.markdown(f"""
                <div class="glass animate-in delay-{(i+1)%5 + 1}" style="margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <span style="color:#e2e8f0; font-weight:600; font-size:0.9rem;">
                            #{i+1} · {chunk.get('id', 'N/A')}
                        </span>
                        <span class="pill pill-indigo" style="font-family:'JetBrains Mono';">
                            {final:.2f}
                        </span>
                    </div>
                    <div style="display:flex; gap:16px; margin-bottom:14px;">
                        <div style="flex:1; text-align:center; padding:8px; background:rgba(168,85,247,0.1); border-radius:8px; border: 1px solid rgba(168,85,247,0.2);">
                            <div style="color:#94a3b8; font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">Semantic</div>
                            <div style="color:#c084fc; font-size:1rem; font-weight:700; font-family:'JetBrains Mono';">{sem:.2f}</div>
                        </div>
                        <div style="flex:1; text-align:center; padding:8px; background:rgba(251,191,36,0.1); border-radius:8px; border: 1px solid rgba(251,191,36,0.2);">
                            <div style="color:#94a3b8; font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">Recency</div>
                            <div style="color:#fbbf24; font-size:1rem; font-weight:700; font-family:'JetBrains Mono';">{rec:.2f}</div>
                        </div>
                        <div style="flex:1; text-align:center; padding:8px; background:rgba(74,222,128,0.1); border-radius:8px; border: 1px solid rgba(74,222,128,0.2);">
                            <div style="color:#94a3b8; font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">Outcome</div>
                            <div style="color:#4ade80; font-size:1rem; font-weight:700; font-family:'JetBrains Mono';">{out:.2f}</div>
                        </div>
                    </div>
                    <div style="color:#cbd5e1; font-size:0.84rem; line-height:1.6; margin-bottom:10px;">
                        {chunk.get('document', '')[:280]}
                    </div>
                    <div style="color:#64748b; font-size:0.8rem; border-top:1px solid rgba(148,163,184,0.06); padding-top:10px;">
                        <span style="color:#94a3b8; font-weight:500;">Past fix:</span> {meta.get('resolution', 'N/A')[:250]}
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ━━━ TAB 4: AGENT DECISIONS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_agent:
    st.markdown("<br>", unsafe_allow_html=True)
    pr = st.session_state.pipeline_result
    
    if pr is None:
        st.info("Submit a ticket first to see agent decisions.")
    else:
        triage = pr.get("triage", {})
        auto = pr.get("automation", {})
        
        col_t, col_a = st.columns([1, 1], gap="large")
        
        with col_t:
            decision = triage.get("decision", "N/A")
            escalate = triage.get("escalate", False)
            urgency = triage.get("urgency_boost", False)
            
            st.markdown(f"""
            <div class="glass">
                <div class="section-title"><span class="section-icon">🏥</span>TriageAgent</div>
                <div class="kv">
                    <span class="kv-key">Decision</span>
                    {decision_pill(decision)}
                </div>
                <div class="kv">
                    <span class="kv-key">Route To</span>
                    <span class="kv-val" style="color:#e2e8f0;">{triage.get('route_to', 'N/A')}</span>
                </div>
                <div class="kv">
                    <span class="kv-key">Escalate</span>
                    <span class="kv-val" style="color:{'#f87171' if escalate else '#4ade80'};">{'Yes' if escalate else 'No'}</span>
                </div>
                <div class="kv">
                    <span class="kv-key">Urgency Boost</span>
                    <span class="kv-val" style="color:{'#fbbf24' if urgency else '#4ade80'};">{'Yes' if urgency else 'No'}</span>
                </div>
                <div style="margin-top:12px; padding-top:12px; border-top:1px solid rgba(148,163,184,0.06);">
                    <div style="color:#64748b; font-size:0.78rem; font-weight:500; margin-bottom:4px;">Rationale</div>
                    <div style="color:#cbd5e1; font-size:0.84rem; line-height:1.6;">{triage.get('rationale', 'N/A')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if escalate:
                st.markdown(f"""
                <div class="banner-danger" style="margin-top:12px;">
                    <div style="color:#fca5a5; font-weight:700; font-size:0.85rem; margin-bottom:4px;">🚨 Escalation Triggered</div>
                    <div style="color:#fecaca; font-size:0.82rem;">{triage.get('rationale', '')}</div>
                </div>
                """, unsafe_allow_html=True)
            
            if urgency:
                keywords = triage.get("urgency_keywords", [])
                st.markdown(f"""
                <div style="background:rgba(245,158,11,0.06); border:1px solid rgba(245,158,11,0.12);
                            border-radius:10px; padding:12px; margin-top:10px;">
                    <span style="color:#fbbf24; font-size:0.8rem; font-weight:600;">⚡ Urgency keywords:</span>
                    <span style="color:#fde68a; font-size:0.8rem;"> {', '.join(keywords)}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col_a:
            should_auto = auto.get("should_automate", False)
            pattern_count = auto.get("pattern_count", 0)
            
            st.markdown(f"""
            <div class="glass">
                <div class="section-title"><span class="section-icon">🤖</span>AutomationDiscovery</div>
                <div class="kv">
                    <span class="kv-key">Pattern Match</span>
                    <span class="pill {'pill-blue' if should_auto else 'pill-green'}">
                        {'AUTOMATE' if should_auto else 'NO PATTERN'}
                    </span>
                </div>
                <div class="kv">
                    <span class="kv-key">Similar Tickets</span>
                    <span class="kv-val" style="color:#e2e8f0; font-family:'JetBrains Mono';">{pattern_count}</span>
                </div>
                <div class="kv">
                    <span class="kv-key">Threshold</span>
                    <span class="kv-val" style="color:#64748b; font-family:'JetBrains Mono';">{config.REPEAT_THRESHOLD}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if should_auto:
                st.markdown(f"""
                <div class="banner-info" style="margin-top:12px;">
                    <div style="color:#93c5fd; font-weight:700; font-size:0.85rem; margin-bottom:6px;">🤖 Runbook Suggested</div>
                    <div style="color:#bfdbfe; font-size:0.82rem; line-height:1.6;">{auto.get('suggested_runbook', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="padding: 24px; text-align: center; margin-top: 12px;">
                    <div style="color:#334155; font-size:2rem; margin-bottom:8px;">✓</div>
                    <p style="color:#475569; font-size:0.82rem;">No recurring pattern detected. This appears to be a unique or low-frequency issue.</p>
                </div>
                """, unsafe_allow_html=True)


# ━━━ TAB 5: RESOLUTION + JUDGE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_judge:
    st.markdown("<br>", unsafe_allow_html=True)
    pr = st.session_state.pipeline_result
    
    if pr is None:
        st.info("Submit a ticket first to see resolution and judge results.")
    elif pr.get("resolution") is None:
        st.warning("Enable **Full Resolution** in the sidebar and resubmit.")
    else:
        res = pr["resolution"]
        judge = pr.get("judge", {})
        
        col_res, col_jdg = st.columns([1.2, 1], gap="large")
        
        with col_res:
            steps = res.get("resolution_steps", [])
            res_conf = res.get("confidence", 0)
            
            st.markdown(f"""
            <div class="glass">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                    <div class="section-title" style="margin:0; border:none; padding:0;">
                        <span class="section-icon">🔧</span>Resolution Steps
                    </div>
                    <span style="color:{conf_color(res_conf)}; font-weight:600; font-size:0.82rem; font-family:'JetBrains Mono';">
                        {res_conf:.0%} conf
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            for i, step in enumerate(steps):
                st.markdown(f"""
                <div style="display:flex; gap:12px; margin-bottom:10px; align-items:flex-start;">
                    <div style="min-width:24px; height:24px; border-radius:6px; background:rgba(99,102,241,0.12);
                                color:#818cf8; font-size:0.75rem; font-weight:700; display:flex; align-items:center;
                                justify-content:center; margin-top:2px;">{i+1}</div>
                    <div style="color:#cbd5e1; font-size:0.85rem; line-height:1.65; flex:1;">{step}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            source_ids = res.get("source_ids", [])
            if source_ids:
                st.markdown(f'<p style="color:#475569; font-size:0.75rem; margin-top:8px;">Sources: {", ".join(source_ids)}</p>', unsafe_allow_html=True)
        
        with col_jdg:
            if not judge:
                st.warning("Judge results unavailable.")
            else:
                gate = judge.get("safety_gate", "PASS")
                overall = float(judge.get("overall", 0))
                
                # Safety gate banner
                if gate == "PASS":
                    st.markdown("""
                    <div class="banner-success" style="margin-bottom: 16px;">
                        <div style="display:flex; align-items:center; gap:8px;">
                            <span style="font-size:1.2rem;">🛡️</span>
                            <div>
                                <div style="color:#4ade80; font-weight:700; font-size:0.85rem;">SAFETY GATE: PASS</div>
                                <div style="color:#86efac; font-size:0.78rem;">Safe for auto-deployment</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="banner-danger" style="margin-bottom: 16px;">
                        <div style="display:flex; align-items:center; gap:8px;">
                            <span style="font-size:1.2rem;">🚫</span>
                            <div>
                                <div style="color:#f87171; font-weight:700; font-size:0.85rem;">SAFETY GATE: BLOCKED</div>
                                <div style="color:#fca5a5; font-size:0.78rem;">Requires human review</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Overall score ring
                ring_color = score_color(overall)
                st.markdown(f"""
                <div class="glass" style="text-align:center; padding:20px; margin-bottom:16px;">
                    <div class="score-ring" style="border: 3px solid {ring_color}; color:{ring_color};">
                        {overall:.1f}
                    </div>
                    <div style="color:#64748b; font-size:0.75rem; font-weight:600; text-transform:uppercase; letter-spacing:0.08em;">
                        Overall Score
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Rubric bars
                st.markdown(f"""
                <div class="glass">
                    <div class="section-title" style="margin-bottom:12px;"><span class="section-icon">📊</span>Quality Rubric</div>
                    {render_rubric_bar("Correctness", judge.get("correctness", 0))}
                    {render_rubric_bar("Completeness", judge.get("completeness", 0))}
                    {render_rubric_bar("Safety", judge.get("safety", 0))}
                    {render_rubric_bar("Clarity", judge.get("clarity", 0))}
                </div>
                """, unsafe_allow_html=True)
                
                # Critique
                critique = judge.get("critique", "")
                if critique:
                    st.markdown(f"""
                    <div style="background:rgba(245,158,11,0.04); border:1px solid rgba(245,158,11,0.1);
                                border-radius:10px; padding:14px; margin-top:12px;">
                        <div style="color:#fbbf24; font-size:0.78rem; font-weight:600; margin-bottom:6px;">Judge Critique</div>
                        <div style="color:#94a3b8; font-size:0.82rem; line-height:1.6;">{critique}</div>
                    </div>
                    """, unsafe_allow_html=True)
