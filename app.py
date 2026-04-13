"""
⚡ Nexus AI Ticket Intelligence Platform — v3.0
Streamlit Dashboard with 5-Tab Progressive Disclosure UI

Tab 1: 🎫 Submit Ticket — form input for title and description
Tab 2: 🧠 Classification — cascade result, confidence, novelty flag
Tab 3: 🔍 RAG Evidence — ranked chunks with multi-hop results and scores
Tab 4: 🤖 Agent Decisions — which agent fired, decision, rationale
Tab 5: ⚖️ Resolution + Judge — resolution steps, rubric scores, safety gate
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Nexus AI Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom Advanced CSS (Glassmorphism & Animations) ─────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    
    /* ── Background & Layout ── */
    .stApp {
        background-color: #0f172a;
        background-image: radial-gradient(circle at top right, rgba(99, 102, 241, 0.15), transparent 400px),
                          radial-gradient(circle at bottom left, rgba(236, 72, 153, 0.1), transparent 400px);
    }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    
    /* ── Animations ── */
    @keyframes slideUpFade {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 10px rgba(99, 102, 241, 0.2); }
        50% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.5); }
        100% { box-shadow: 0 0 10px rgba(99, 102, 241, 0.2); }
    }

    .animated-content { animation: slideUpFade 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    
    /* Prevent text overflow in markdown */
    .stMarkdown p, .stMarkdown div {
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    /* ── Headers ── */
    .hero-title {
        font-size: 2.5rem; font-weight: 800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem; letter-spacing: -0.5px;
    }
    .hero-sub { color: #94a3b8; font-size: 1.05rem; margin-top: 0; font-weight: 400; }
    
    /* ── Glassmorphism Metric Cards ── */
    .metric-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px; padding: 1.5rem; text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(129, 140, 248, 0.3);
    }
    .metric-card h2 { color: #f8fafc; margin: 0; font-size: 2.2rem; font-weight: 700; }
    .metric-card p  { color: #94a3b8; margin: 0; font-size: 0.9rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; }
    
    /* ── Result & Data Boxes ── */
    .glass-panel {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .glass-panel h4 { color: #f1f5f9; margin-top: 0; border-bottom: 1px solid #334155; padding-bottom: 10px; }
    
    /* ── Badges ── */
    .badge { padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; display: inline-block; }
    .badge-p1 { background: rgba(220, 38, 38, 0.2); color: #fca5a5; border: 1px solid #ef4444; }
    .badge-p2 { background: rgba(249, 115, 22, 0.2); color: #fdba74; border: 1px solid #f97316; }
    .badge-p3 { background: rgba(59, 130, 246, 0.2); color: #93c5fd; border: 1px solid #3b82f6; }
    .badge-p4 { background: rgba(34, 197, 94, 0.2); color: #86efac; border: 1px solid #22c55e; }

    /* ── Escalation Banners ── */
    .escalation-banner {
        background: linear-gradient(90deg, rgba(127, 29, 29, 0.8) 0%, rgba(153, 27, 27, 0.4) 100%);
        border-left: 4px solid #ef4444; border-radius: 8px;
        padding: 1.2rem; color: #fecaca; box-shadow: 0 4px 15px rgba(220, 38, 38, 0.15);
        animation: pulseGlow 3s infinite;
    }
    .automation-banner {
        background: linear-gradient(90deg, rgba(30, 58, 138, 0.8) 0%, rgba(30, 64, 175, 0.4) 100%);
        border-left: 4px solid #3b82f6; border-radius: 8px;
        padding: 1.2rem; color: #bfdbfe; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15);
    }
    .safety-pass {
        background: linear-gradient(90deg, rgba(21, 128, 61, 0.6) 0%, rgba(22, 163, 74, 0.3) 100%);
        border-left: 4px solid #22c55e; border-radius: 8px;
        padding: 1rem; color: #bbf7d0;
    }
    .safety-blocked {
        background: linear-gradient(90deg, rgba(153, 27, 27, 0.8) 0%, rgba(185, 28, 28, 0.4) 100%);
        border-left: 4px solid #ef4444; border-radius: 8px;
        padding: 1rem; color: #fca5a5;
        animation: pulseGlow 2s infinite;
    }
    
    /* ── User Inputs ── */
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid #334155 !important;
        color: #e2e8f0 !important; border-radius: 10px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #818cf8 !important; box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2) !important;
    }
    
    /* ── Primary Button ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important; font-weight: 600 !important;
        border: none !important; border-radius: 10px !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(168, 85, 247, 0.4) !important;
    }
    
    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: none; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 41, 59, 0.5); border-radius: 10px;
        border: 1px solid transparent; color: #94a3b8; padding: 10px 20px; font-weight: 500;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(129, 140, 248, 0.1) !important;
        color: #818cf8 !important; border: 1px solid rgba(129, 140, 248, 0.3);
    }
    
    /* ── Rubric Score Bars ── */
    .rubric-bar {
        height: 8px; border-radius: 4px; margin: 4px 0 12px 0;
    }
    .rubric-label {
        display: flex; justify-content: space-between; color: #cbd5e1; font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


# ── Cached Model Loading ─────────────────────────────────────
@st.cache_resource(show_spinner="Initializing Nexus Core...")
def load_classifier():
    from core.classifier import TicketClassifier
    return TicketClassifier()

@st.cache_resource(show_spinner="Waking RAG engines...")
def load_rag_engine():
    from core.rag import ResolutionEngine
    return ResolutionEngine()

@st.cache_resource(show_spinner="Loading agent reasoning...")
def load_agent():
    from core.agent import AgenticLayer, TriageAgent, ResolutionAgent, AutomationDiscoveryAgent
    return AgenticLayer(), TriageAgent(), ResolutionAgent(), AutomationDiscoveryAgent()

@st.cache_resource(show_spinner="Initializing quality judge...")
def load_judge():
    from core.judge import ResolutionJudge
    return ResolutionJudge()

@st.cache_data(show_spinner=False)
def load_ticket_data():
    # Try merged file first, then fallback
    for fname in ["synthetic_tickets_merged.csv", "synthetic_tickets.csv"]:
        csv_path = os.path.join(os.path.dirname(__file__), "data", fname)
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path)
    return pd.DataFrame()


# ── Session State Init ───────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None


# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="hero-title">Nexus Agent</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">v3.0 — Agentic Intelligence</p>', unsafe_allow_html=True)
    st.divider()
    
    st.markdown("#### 🎛️ Agent Control Panel")
    generate_resolution = st.toggle("🧠 Enable Generative RAG", value=True,
        help="Run the full RAG + Resolution + Judge pipeline on submission."
    )
    
    st.divider()
    st.markdown("#### ⚡ Infrastructure")
    llm_label = f"Groq ({config.GROQ_MODEL})" if config.USE_GROQ else f"Ollama ({config.OLLAMA_MODEL})"
    st.markdown(f'<div style="color:#94a3b8; font-size:0.85rem;">'
                f'<b>LLM:</b> {llm_label}<br>'
                f'<b>Vectors:</b> {config.EMBEDDING_MODEL_NAME}<br>'
                f'<b>Storage:</b> ChromaDB Local</div>', unsafe_allow_html=True)
    
    st.divider()
    st.caption("Nexus AI · v3.0 Milestone · Deployed Local")


# ── Helper Functions ─────────────────────────────────────────
def priority_badge(priority: str) -> str:
    p = priority.lower()
    if "p1" in p or "critical" in p: return f'<span class="badge badge-p1">🔥 {priority}</span>'
    if "p2" in p or "high" in p:     return f'<span class="badge badge-p2">⚡ {priority}</span>'
    if "p3" in p or "medium" in p:   return f'<span class="badge badge-p3">⚠️ {priority}</span>'
    return f'<span class="badge badge-p4">✅ {priority}</span>'

def confidence_color(conf: float) -> str:
    if conf >= 0.8: return "#4ade80"
    if conf >= 0.6: return "#fb923c"
    return "#f87171"

def rubric_color(score: int) -> str:
    if score >= 4: return "#4ade80"
    if score >= 3: return "#fbbf24"
    return "#f87171"

def rubric_bar(label: str, score: int, max_score: int = 5) -> str:
    pct = (score / max_score) * 100
    color = rubric_color(score)
    return f"""
    <div class="rubric-label">
        <span>{label}</span>
        <span style="color:{color}; font-weight:600;">{score}/{max_score}</span>
    </div>
    <div style="background:rgba(51,65,85,0.6); border-radius:4px; overflow:hidden;">
        <div class="rubric-bar" style="width:{pct}%; background:{color};"></div>
    </div>
    """

CASCADE_BADGES = {
    "centroid": ("⚡ FAST PATH", "#22c55e", "rgba(34,197,94,0.15)"),
    "llm_judge": ("🧠 LLM JUDGE", "#f59e0b", "rgba(245,158,11,0.15)"),
    "escalated": ("🚨 ESCALATED", "#ef4444", "rgba(239,68,68,0.15)"),
    "novel_ticket": ("🆕 NOVEL TICKET", "#a855f7", "rgba(168,85,247,0.15)"),
    "similarity_search": ("🔍 SIMILARITY", "#3b82f6", "rgba(59,130,246,0.15)"),
}


# ── FULL PIPELINE EXECUTION ──────────────────────────────────
def run_full_pipeline(title: str, desc: str, enable_rag: bool):
    """Run the complete intelligence pipeline and store results in session."""
    result = {}
    
    with st.status("🔗 Nexus AI initializing analysis...", expanded=True) as status:
        # Stage 1: Classification
        st.write("🔄 Running classification cascade...")
        clf = load_classifier()
        classification = clf.classify(title, desc)
        result["classification"] = classification
        time.sleep(0.3)
        
        # Stage 2: Triage Agent
        st.write("🔄 Engaging TriageAgent...")
        agents = load_agent()
        agentric_layer, triage_agent, res_agent, auto_agent = agents
        ticket = {"title": title, "description": desc}
        triage_result = triage_agent.run(ticket, classification)
        result["triage"] = triage_result
        time.sleep(0.2)
        
        # Stage 3: RAG retrieval + ranking
        st.write("🔄 Retrieving & ranking evidence...")
        rag = load_rag_engine()
        rag_result = rag.suggest_resolution(title, desc)
        result["rag"] = rag_result
        # Also get ranked chunks separately for ResolutionAgent
        query_embedding = rag.embedding_model.encode(f"{title} {desc}").tolist()
        raw_results = rag.collection.query(
            query_embeddings=[query_embedding], n_results=6,
            include=["documents", "metadatas", "distances"]
        )
        ranked_chunks = rag._rank_retrieved_chunks(raw_results)[:3]
        result["ranked_chunks"] = ranked_chunks
        time.sleep(0.2)
        
        if enable_rag:
            # Stage 4: Resolution Agent
            st.write("🔄 ResolutionAgent generating structured fix...")
            res_result = res_agent.run(ticket, ranked_chunks)
            result["resolution"] = res_result
            time.sleep(0.2)
            
            # Stage 5: Judge
            st.write("🔄 LLM-as-Judge evaluating resolution quality...")
            judge = load_judge()
            resolution_text = "\n".join(res_result.get("resolution_steps", []))
            judge_result = judge.judge(
                {"title": title, "description": desc, "category": classification.get("category", "Unknown")},
                resolution_text
            )
            result["judge"] = judge_result
            time.sleep(0.2)
            
            # Stage 6: Automation Discovery (post-resolution)
            st.write("🔄 AutomationDiscoveryAgent scanning patterns...")
            auto_result = auto_agent.run({
                "title": title, "description": desc,
                "category": classification.get("category", "Unknown"),
                "resolution": resolution_text,
            })
            result["automation"] = auto_result
        else:
            result["resolution"] = None
            result["judge"] = None
            # Still run automation discovery
            auto_result = auto_agent.run({
                "title": title, "description": desc,
                "category": classification.get("category", "Unknown"),
                "resolution": "",
            })
            result["automation"] = auto_result
        
        status.update(label="✅ Full Pipeline Complete", state="complete", expanded=False)
    
    result["title"] = title
    result["description"] = desc
    return result


# ── Main Content: 5 Tabs ─────────────────────────────────────
tab_submit, tab_classify, tab_rag, tab_agent, tab_judge = st.tabs([
    "🎫 Submit Ticket", "🧠 Classification", "🔍 RAG Evidence",
    "🤖 Agent Decisions", "⚖️ Resolution + Judge"
])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1: SUBMIT TICKET (UI-01)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_submit:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_input, col_status = st.columns([1.2, 1], gap="large")
    
    with col_input:
        st.markdown('<h4>Describe the Issue</h4>', unsafe_allow_html=True)
        with st.form("ticket_form", clear_on_submit=False):
            ticket_title = st.text_input(
                "Subject Line",
                placeholder="e.g., VPN connection drops after 5 minutes with error 619"
            )
            ticket_desc = st.text_area(
                "Issue Details",
                placeholder="Provide context: error messages, affected users, timestamps, logs...",
                height=220
            )
            submitted = st.form_submit_button("⚡ Engage Full AI Pipeline", use_container_width=True, type="primary")
    
    with col_status:
        if submitted and ticket_title and ticket_desc:
            result = run_full_pipeline(ticket_title, ticket_desc, generate_resolution)
            st.session_state.pipeline_result = result
            
            # Quick summary card
            clf = result["classification"]
            st.markdown(f"""
            <div class="glass-panel animated-content">
                <h4>⚡ Pipeline Summary</h4>
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span style="color:#94a3b8;">Category</span>
                    <strong style="color:#c084fc;">{clf.get('category', 'N/A')}</strong>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span style="color:#94a3b8;">Confidence</span>
                    <strong style="color:{confidence_color(clf.get('confidence', 0))};">{clf.get('confidence', 0):.1%}</strong>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span style="color:#94a3b8;">Route To</span>
                    <strong style="color:#e2e8f0;">{clf.get('department', 'N/A')}</strong>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#94a3b8;">Safety Gate</span>
                    <strong style="color:{'#4ade80' if result.get('judge', {}).get('safety_gate') == 'PASS' else '#f87171'};">
                        {result.get('judge', {}).get('safety_gate', 'N/A')}
                    </strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("👉 Navigate to the other tabs to inspect each pipeline stage in detail.")
            
            # Save to history
            st.session_state.history.append({
                "title": ticket_title,
                "category": clf.get("category"),
                "department": clf.get("department"),
                "confidence": clf.get("confidence"),
                "priority": clf.get("priority_suggestion", "P3 Medium"),
                "method": clf.get("method"),
                "safety_gate": result.get("judge", {}).get("safety_gate", "N/A"),
                "escalated": result.get("triage", {}).get("escalate", False),
            })
            
            st.toast("Pipeline complete! Check all tabs.", icon="✅")
            
        elif submitted:
            st.error("⚠️ Please provide both a Subject and Issue Details.")
        
        elif st.session_state.pipeline_result is None:
            st.markdown("""
            <div class="glass-panel" style="text-align:center; padding:3rem;">
                <p style="color:#64748b; font-size:1.1rem;">Submit a ticket to see the full pipeline in action</p>
                <p style="color:#475569; font-size:0.9rem;">Classification → RAG → Agents → Resolution → Judge</p>
            </div>
            """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2: CLASSIFICATION (UI-02)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_classify:
    st.markdown("<br>", unsafe_allow_html=True)
    pr = st.session_state.pipeline_result
    
    if pr is None:
        st.info("Submit a ticket first to see classification results.")
    else:
        clf = pr["classification"]
        conf = clf.get("confidence", 0)
        cat = clf.get("category", "Unknown")
        dept = clf.get("department", "N/A")
        method = clf.get("method", "centroid")
        is_novel = clf.get("is_novel", False)
        pri = clf.get("priority_suggestion", "P3 Medium")
        
        # Cascade path badge
        badge_text, badge_color, badge_bg = CASCADE_BADGES.get(
            method, ("❓ UNKNOWN", "#94a3b8", "rgba(148,163,184,0.15)")
        )
        
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:16px;">
            <span style="background:{badge_bg}; color:{badge_color}; border:1px solid {badge_color};
                         padding:8px 24px; border-radius:24px; font-weight:700; font-size:1.1rem;
                         letter-spacing:1px;">
                {badge_text}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        col_clf1, col_clf2 = st.columns([1, 1], gap="large")
        
        with col_clf1:
            # Classification details
            st.markdown(f"""
            <div class="glass-panel">
                <h4>🎯 Classification Result</h4>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                    <span style="color:#94a3b8;">Predicted Category</span>
                    <strong style="color:#c084fc; font-size:1.1rem;">{cat}</strong>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                    <span style="color:#94a3b8;">Target Department</span>
                    <strong style="color:#e2e8f0;">{dept}</strong>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                    <span style="color:#94a3b8;">System Confidence</span>
                    <strong style="color:{confidence_color(conf)}; font-size:1.1rem;">{conf:.1%}</strong>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                    <span style="color:#94a3b8;">Cascade Path</span>
                    <strong style="color:{badge_color};">{badge_text}</strong>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                    <span style="color:#94a3b8;">Novel Ticket?</span>
                    <strong style="color:{'#a855f7' if is_novel else '#4ade80'};">{'🆕 YES' if is_novel else '✅ NO'}</strong>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#94a3b8;">Priority Suggestion</span>
                    {priority_badge(pri)}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # LLM Judge rationale (if medium-confidence path was taken)
            llm_rationale = clf.get("llm_rationale")
            if llm_rationale:
                st.markdown(f"""
                <div style="background:rgba(245,158,11,0.08); border-left:3px solid #f59e0b;
                            border-radius:8px; padding:10px 14px; margin-top:8px;
                            color:#fde68a; font-size:0.88rem;">
                    <strong>LLM Judge Rationale:</strong> {llm_rationale}
                </div>
                """, unsafe_allow_html=True)
        
        with col_clf2:
            # Category scores bar chart
            scores = clf.get("all_scores", {})
            if scores:
                fig_scores = go.Figure(go.Bar(
                    x=list(scores.values()),
                    y=list(scores.keys()),
                    orientation='h',
                    marker=dict(
                        color=['#c084fc' if k == cat else '#334155' for k in scores.keys()],
                        line=dict(width=0)
                    ),
                    text=[f"{v:.1%}" for v in scores.values()],
                    textposition='outside',
                    textfont=dict(color='#e2e8f0')
                ))
                fig_scores.update_layout(
                    height=280, margin=dict(l=0, r=40, t=10, b=0),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#94a3b8', size=11, family="Outfit"),
                    xaxis=dict(showgrid=False, range=[0, 1], visible=False),
                    yaxis=dict(showgrid=False, tickfont=dict(size=12))
                )
                st.markdown('<div class="glass-panel"><h4>📊 Category Confidence Scores</h4>', unsafe_allow_html=True)
                st.plotly_chart(fig_scores, use_container_width=True, config={'displayModeBar': False})
                st.markdown('</div>', unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3: RAG EVIDENCE (UI-03)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_rag:
    st.markdown("<br>", unsafe_allow_html=True)
    pr = st.session_state.pipeline_result
    
    if pr is None:
        st.info("Submit a ticket first to see RAG evidence.")
    else:
        ranked_chunks = pr.get("ranked_chunks", [])
        rag_result = pr.get("rag", {})
        
        if not ranked_chunks:
            st.warning("No similar tickets found in the vector store.")
        else:
            st.markdown("### 🏆 Hop 1 — Ranked Evidence Chunks")
            st.caption("Chunks ranked by: **Semantic (60%)** + **Recency (20%)** + **Outcome (20%)**")
            
            for i, chunk in enumerate(ranked_chunks):
                sem = chunk.get("semantic", 0)
                rec = chunk.get("recency", 0)
                out = chunk.get("outcome", 0)
                final = chunk.get("final_score", 0)
                meta = chunk.get("metadata", {})
                
                st.markdown(f"""
                <div class="glass-panel">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <h4 style="margin:0; border:none; padding:0;">#{i+1} — {chunk.get('id', 'N/A')}</h4>
                        <span style="background:rgba(129,140,248,0.15); color:#818cf8; padding:4px 14px;
                                     border-radius:20px; font-weight:700; font-size:0.95rem;">
                            Score: {final:.2f}
                        </span>
                    </div>
                    <div style="display:flex; gap:16px; margin-bottom:12px;">
                        <span style="color:#94a3b8; font-size:0.82rem;">
                            🎯 Semantic: <strong style="color:#c084fc;">{sem:.2f}</strong>
                        </span>
                        <span style="color:#94a3b8; font-size:0.82rem;">
                            📅 Recency: <strong style="color:#fbbf24;">{rec:.2f}</strong>
                        </span>
                        <span style="color:#94a3b8; font-size:0.82rem;">
                            ✅ Outcome: <strong style="color:#4ade80;">{out:.2f}</strong>
                        </span>
                    </div>
                    <div style="color:#cbd5e1; font-size:0.9rem; margin-bottom:8px;">
                        <strong>Issue:</strong> {chunk.get('document', '')[:250]}
                    </div>
                    <div style="color:#94a3b8; font-size:0.85rem; border-top:1px solid #334155; padding-top:8px;">
                        <strong>Past Resolution:</strong> {meta.get('resolution', 'N/A')[:300]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Hop 2 — Multi-hop KB context
        context = rag_result.get("context_used", "")
        if "Hop 2" in context:
            hop2_text = context.split("## Linked Category DB Insight (Hop 2):")[1].strip() if "## Linked Category DB Insight (Hop 2):" in context else ""
            if hop2_text and "No additional" not in hop2_text:
                st.markdown("### 🔗 Hop 2 — Category KB Cross-Reference")
                st.markdown(f"""
                <div class="glass-panel" style="border-left:3px solid #a855f7;">
                    <h4 style="color:#c084fc;">Linked Knowledge Base Insights</h4>
                    <div style="color:#cbd5e1; font-size:0.9rem; white-space:pre-wrap;">{hop2_text}</div>
                </div>
                """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4: AGENT DECISIONS (UI-04)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_agent:
    st.markdown("<br>", unsafe_allow_html=True)
    pr = st.session_state.pipeline_result
    
    if pr is None:
        st.info("Submit a ticket first to see agent decisions.")
    else:
        triage = pr.get("triage", {})
        auto = pr.get("automation", {})
        
        # ── Triage Agent ──
        st.markdown("### 🏥 TriageAgent")
        decision = triage.get("decision", "N/A")
        escalate = triage.get("escalate", False)
        urgency = triage.get("urgency_boost", False)
        
        decision_colors = {
            "AUTO_ROUTE": ("#22c55e", "rgba(34,197,94,0.1)"),
            "ROUTE_WITH_LLM_ASSIST": ("#f59e0b", "rgba(245,158,11,0.1)"),
            "ESCALATE_LOW_CONFIDENCE": ("#ef4444", "rgba(239,68,68,0.1)"),
            "ESCALATE_NOVEL": ("#a855f7", "rgba(168,85,247,0.1)"),
        }
        d_color, d_bg = decision_colors.get(decision, ("#94a3b8", "rgba(148,163,184,0.1)"))
        
        st.markdown(f"""
        <div class="glass-panel">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <h4 style="margin:0; border:none; padding:0;">Routing Decision</h4>
                <span style="background:{d_bg}; color:{d_color}; border:1px solid {d_color};
                             padding:6px 16px; border-radius:20px; font-weight:700;">
                    {decision}
                </span>
            </div>
            <div style="color:#cbd5e1; font-size:0.9rem; margin-bottom:10px;">
                <strong>Rationale:</strong> {triage.get('rationale', 'N/A')}
            </div>
            <div style="display:flex; gap:20px;">
                <span style="color:#94a3b8;">Route To: <strong style="color:#e2e8f0;">{triage.get('route_to', 'N/A')}</strong></span>
                <span style="color:#94a3b8;">Escalate: <strong style="color:{'#ef4444' if escalate else '#4ade80'};">{'YES' if escalate else 'NO'}</strong></span>
                <span style="color:#94a3b8;">Urgency Boost: <strong style="color:{'#f59e0b' if urgency else '#4ade80'};">{'⚠ YES' if urgency else 'NO'}</strong></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if urgency:
            keywords = triage.get("urgency_keywords", [])
            st.markdown(f"""
            <div style="background:rgba(245,158,11,0.08); border-left:3px solid #f59e0b;
                        border-radius:8px; padding:10px 14px; color:#fde68a; font-size:0.88rem;">
                <strong>⚠ Urgency Keywords Detected:</strong> {', '.join(keywords)}
            </div>
            """, unsafe_allow_html=True)
        
        if escalate:
            st.markdown(f"""
            <div class="escalation-banner" style="margin-top:12px;">
                <h4 style="margin:0;color:#fca5a5;">🚨 ESCALATION PROTOCOL INITIATED</h4>
                <p style="margin:5px 0 0 0;font-size:0.9rem;">{triage.get('rationale', '')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ── Automation Discovery Agent ──
        st.markdown("### 🤖 AutomationDiscoveryAgent")
        should_auto = auto.get("should_automate", False)
        pattern_count = auto.get("pattern_count", 0)
        
        st.markdown(f"""
        <div class="glass-panel">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <h4 style="margin:0; border:none; padding:0;">Pattern Detection</h4>
                <span style="background:{'rgba(59,130,246,0.15)' if should_auto else 'rgba(34,197,94,0.1)'};
                             color:{'#3b82f6' if should_auto else '#4ade80'};
                             border:1px solid {'#3b82f6' if should_auto else '#4ade80'};
                             padding:6px 16px; border-radius:20px; font-weight:700;">
                    {'🤖 AUTOMATION SUGGESTED' if should_auto else '✅ NO PATTERN'}
                </span>
            </div>
            <div style="color:#94a3b8;">Similar tickets found: <strong style="color:#e2e8f0;">{pattern_count}</strong> (threshold: {config.REPEAT_THRESHOLD})</div>
        </div>
        """, unsafe_allow_html=True)
        
        if should_auto:
            st.markdown(f"""
            <div class="automation-banner">
                <h4 style="margin:0;color:#93c5fd;">🤖 RUNBOOK AUTOMATION TRIGGERED</h4>
                <p style="margin:5px 0 0 0;font-size:0.9rem;">{auto.get('suggested_runbook', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 5: RESOLUTION + JUDGE (UI-05)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_judge:
    st.markdown("<br>", unsafe_allow_html=True)
    pr = st.session_state.pipeline_result
    
    if pr is None:
        st.info("Submit a ticket first to see resolution and judge results.")
    elif pr.get("resolution") is None:
        st.warning("Enable **🧠 Generative RAG** in the sidebar and resubmit to see resolution + judge.")
    else:
        res = pr["resolution"]
        judge = pr.get("judge", {})
        
        col_res, col_judge = st.columns([1.2, 1], gap="large")
        
        with col_res:
            st.markdown("### 🔧 Resolution Steps")
            steps = res.get("resolution_steps", [])
            res_conf = res.get("confidence", 0)
            
            st.markdown(f"""
            <div class="glass-panel">
                <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                    <h4 style="margin:0; border:none; padding:0;">AI-Generated Resolution</h4>
                    <span style="color:{confidence_color(res_conf)}; font-weight:600;">
                        Confidence: {res_conf:.0%}
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            for i, step in enumerate(steps):
                st.markdown(f"""
                <div style="background:rgba(30,41,59,0.5); border-radius:8px; padding:10px 14px;
                            margin-bottom:8px; border-left:3px solid #818cf8; color:#e2e8f0; font-size:0.9rem;">
                    {step}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Source tickets
            source_ids = res.get("source_ids", [])
            if source_ids:
                st.caption(f"📚 Evidence sources: {', '.join(source_ids)}")
        
        with col_judge:
            st.markdown("### ⚖️ Quality Rubric")
            
            if not judge:
                st.warning("Judge results not available.")
            else:
                # Safety gate banner
                gate = judge.get("safety_gate", "PASS")
                if gate == "PASS":
                    st.markdown("""
                    <div class="safety-pass">
                        <strong>🛡️ SAFETY GATE: PASS</strong> — Resolution is safe for auto-deployment.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="safety-blocked">
                        <strong>🚫 SAFETY GATE: BLOCKED</strong> — Resolution flagged as potentially dangerous. Requires human review.
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Rubric scores
                st.markdown(f"""
                <div class="glass-panel">
                    <h4>📊 4-Axis Evaluation</h4>
                    {rubric_bar("Correctness", judge.get("correctness", 0))}
                    {rubric_bar("Completeness", judge.get("completeness", 0))}
                    {rubric_bar("Safety", judge.get("safety", 0))}
                    {rubric_bar("Clarity", judge.get("clarity", 0))}
                    <div style="border-top:1px solid #334155; padding-top:10px; margin-top:8px;
                                display:flex; justify-content:space-between;">
                        <span style="color:#94a3b8; font-weight:600;">Overall Score</span>
                        <span style="color:{rubric_color(int(judge.get('overall', 0)))}; font-size:1.3rem; font-weight:700;">
                            {judge.get('overall', 0):.1f}/5.0
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Critique
                critique = judge.get("critique", "")
                if critique:
                    st.markdown(f"""
                    <div class="glass-panel" style="border-left:3px solid #f59e0b;">
                        <h4 style="color:#fde68a;">💬 Judge Critique</h4>
                        <p style="color:#cbd5e1; font-size:0.9rem;">{critique}</p>
                    </div>
                    """, unsafe_allow_html=True)
