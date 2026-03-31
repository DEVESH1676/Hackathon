"""
🎫 Intelligent Ticket Routing & Resolution Agent
Streamlit Dashboard — Hackathon Demo (Premium Version)
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
    .stTabs [data-baseweb="tab-list"] { gap: 12px; border-bottom: none; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 41, 59, 0.5); border-radius: 10px;
        border: 1px solid transparent; color: #94a3b8; padding: 10px 24px; font-weight: 500;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(129, 140, 248, 0.1) !important;
        color: #818cf8 !important; border: 1px solid rgba(129, 140, 248, 0.3);
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
    from core.agent import AgenticLayer
    return AgenticLayer()

@st.cache_data(show_spinner=False)
def load_ticket_data():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "synthetic_tickets.csv")
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return pd.DataFrame()


# ── Session State Init ───────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []


# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="hero-title">Nexus Agent</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">L1 Support Automation</p>', unsafe_allow_html=True)
    st.divider()
    
    st.markdown("#### 🎛️ Agent Control Panel")
    confidence_threshold = st.slider(
        "Human Escalation Threshold", 0.0, 1.0, config.CONFIDENCE_THRESHOLD, 0.05,
        help="Tickets falling below this confidence score bypass the AI and route immediately to Human L2 Triage."
    )
    similarity_threshold = st.slider(
        "Automation Trigger Threshold", 0.0, 1.0, config.SIMILARITY_THRESHOLD, 0.05,
        help="If >3 past tickets match a new issue above this similarity, an automated runbook is attached."
    )
    generate_resolution = st.toggle("🧠 Enable Generative RAG", value=False,
        help="Forces Ollama/Groq to compose a final step-by-step resolution synthesized from past fixes."
    )
    
    st.divider()
    st.markdown("#### ⚡ Infrastructure")
    st.markdown(f'<div style="color:#94a3b8; font-size:0.85rem;"><b>Reasoning:</b> {config.OLLAMA_MODEL}<br><b>Vectors:</b> {config.EMBEDDING_MODEL_NAME}<br><b>Storage:</b> ChromaDB Enterprise</div>', unsafe_allow_html=True)
    
    st.divider()
    st.caption("Hackathon MVP Build · Deployed Local")


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


# ── Main Content ─────────────────────────────────────────────
tab_submit, tab_dashboard, tab_history = st.tabs([
    "🚀 Submit Ticket", "📊 Nexus Analytics", "📋 Agent Log"
])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1: SUBMIT TICKET
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_submit:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_input, col_result = st.columns([1.2, 1], gap="large")
    
    with col_input:
        st.markdown('<h4>Describe the Issue</h4>', unsafe_allow_html=True)
        with st.form("ticket_form", clear_on_submit=False):
            ticket_title = st.text_input(
                "Subject Line",
                placeholder="e.g., Critical database latency on primary US-East cluster"
            )
            ticket_desc = st.text_area(
                "Issue Details",
                placeholder="Provide as much context as possible. Output from logs, application errors, impacted users...",
                height=220
            )
            submitted = st.form_submit_button("⚡ Engage AI Analysis", use_container_width=True, type="primary")
    
    with col_result:
        if submitted and ticket_title and ticket_desc:
            
            # Interactive Status Loading
            with st.status("🔗 Nexus AI initializing analysis...", expanded=True) as status:
                st.write("Extracting semantic embeddings...")
                clf = load_classifier()
                time.sleep(0.4)
                
                st.write("Matching vector centroids & historical data...")
                classification = clf.classify(ticket_title, ticket_desc)
                time.sleep(0.3)
                
                st.write("Evaluating escalation and automation pathways...")
                agent = load_agent()
                agent_result = agent.process(ticket_title, ticket_desc, classification)
                time.sleep(0.3)
                
                status.update(label="✅ Analysis Complete", state="complete", expanded=False)
            
            # Display Results in Animated Div
            st.markdown('<div class="animated-content">', unsafe_allow_html=True)
            
            conf = classification["confidence"]
            cat = classification["category"]
            dept = classification["department"]
            pri = classification["priority_suggestion"]
            
            # ── Agent Actions (High Priority Visuals) ──
            if agent_result.get("requires_human"):
                for action in agent_result["agent_actions"]:
                    if action["type"] == "ESCALATE":
                        st.markdown(f"""
                        <div class="escalation-banner">
                            <h4 style="margin:0;color:#fca5a5;">🚨 ESCALATION PROTOCOL INITIATED</h4>
                            <p style="margin:5px 0 0 0;font-size:0.9rem;">{action['reason']}</p>
                            <p style="margin:5px 0 0 0;font-size:0.85rem;opacity:0.8;">Action: {action['action']}</p>
                        </div>
                        <br>
                        """, unsafe_allow_html=True)
            
            if agent_result.get("suggests_automation"):
                for action in agent_result["agent_actions"]:
                    if action["type"] == "SUGGEST_AUTOMATION":
                        st.markdown(f"""
                        <div class="automation-banner">
                            <h4 style="margin:0;color:#93c5fd;">🤖 RUNBOOK AUTOMATION TRIGGERED</h4>
                            <p style="margin:5px 0 0 0;font-size:0.9rem;">{action['reason']}</p>
                            <p style="margin:5px 0 0 0;font-size:0.85rem;opacity:0.8;">Action: {action['action']}</p>
                        </div>
                        <br>
                        """, unsafe_allow_html=True)
            
            # ── Beautiful Classification Result Box ──
            st.markdown(f"""
            <div class="glass-panel">
                <h4>🎯 Routing Vectors</h4>
                <div style="display:flex; justify-content:space-between; margin-bottom: 12px;">
                    <span style="color:#94a3b8;">Predicted Category</span>
                    <strong style="color:#c084fc; font-size:1.1rem;">{cat}</strong>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom: 12px;">
                    <span style="color:#94a3b8;">Target Department</span>
                    <strong style="color:#e2e8f0;">{dept}</strong>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom: 12px;">
                    <span style="color:#94a3b8;">System Confidence</span>
                    <strong style="color:{confidence_color(conf)}; font-size:1.1rem;">{conf:.1%}</strong>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#94a3b8;">Urgency Class</span>
                    {priority_badge(pri)}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # ── Category Scores Bar ──
            scores = classification.get("all_scores", {})
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
                    height=200, margin=dict(l=0, r=30, t=10, b=0),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#94a3b8', size=11, family="Outfit"),
                    xaxis=dict(showgrid=False, range=[0, 1], visible=False),
                    yaxis=dict(showgrid=False, tickfont=dict(size=12))
                )
                st.plotly_chart(fig_scores, use_container_width=True, config={'displayModeBar': False})
            
            # ── RAG UI (Chatbot style) ──
            if generate_resolution:
                st.markdown('<h4 style="color:#f1f5f9; margin-top:20px;">🤖 Synthesized Resolution</h4>', unsafe_allow_html=True)
                with st.spinner("Compiling past data points..."):
                    rag = load_rag_engine()
                    rag_result = rag.suggest_resolution(ticket_title, ticket_desc)
                
                with st.chat_message("assistant", avatar="✨"):
                    st.markdown(rag_result['suggested_resolution'])
                    with st.expander("📚 View Reference Vectors", expanded=False):
                        for i, doc in enumerate(rag_result['context_docs']):
                            st.caption(f"**Doc {i+1}:** {doc[:150]}...")
            
            # ── Similar Tickets ──
            similar = classification.get("similar_tickets", [])
            if similar and not generate_resolution:
                with st.expander("🔍 Explore Historical Matches based on Cosine Similarity", expanded=False):
                    for i, t in enumerate(similar):
                        st.markdown(f"""
                        <div style="padding:10px; background:rgba(30,41,59,0.3); border-radius:8px; margin-bottom:8px; border-left:3px solid #818cf8;">
                            <strong>{i+1}.</strong> {priority_badge(t['priority'])} <span style="color:#94a3b8;">({t['category']})</span><br>
                            <span style="font-size:0.85rem; color:#cbd5e1;">Match: {t['similarity']:.1%}</span><br>
                            <div style="font-size:0.85rem; margin-top:5px;"><em>"{t['document'][:140]}..."</em></div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # ── Save to History ──
            st.session_state.history.append({
                "title": ticket_title,
                "category": cat,
                "department": dept,
                "confidence": conf,
                "priority": pri,
                "escalated": agent_result.get("requires_human", False)
            })
            
            # Success Toast
            st.toast('Analysis processed successfully!', icon='✅')
            if conf > 0.90:
                st.balloons()
            
        elif submitted:
            st.error("⚠️ Diagnostics halted. Please input both Subject and Details.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2: ANALYTICS DASHBOARD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_dashboard:
    st.markdown("<br>", unsafe_allow_html=True)
    df = load_ticket_data()
    
    if df.empty:
        st.warning("Database empty. Vectorize data before visualizing analytics.")
    else:
        # ── Glassmorphism Metric Row ──
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f"""<div class="metric-card">
            <h2>{len(df)}</h2><p>Tickets Processed</p></div>""", unsafe_allow_html=True)
        
        m2.markdown(f"""<div class="metric-card">
            <h2>{df['category'].nunique()}</h2><p>Clusters</p></div>""", unsafe_allow_html=True)
        
        p1_count = len(df[df['priority'].str.contains('P1', case=False, na=False)])
        m3.markdown(f"""<div class="metric-card">
            <h2 style="color:#fca5a5;">{p1_count}</h2><p>Critical P1</p></div>""", unsafe_allow_html=True)
        
        session_count = len(st.session_state.history)
        escalated = sum(1 for h in st.session_state.history if h.get("escalated"))
        rate = f"{escalated/session_count:.0%}" if session_count > 0 else "N/A"
        m4.markdown(f"""<div class="metric-card">
            <h2 style="color:#93c5fd;">{rate}</h2><p>L2 Escalation Rate</p></div>""", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # ── Charts Row ──
        chart1, chart2 = st.columns(2)
        
        with chart1:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            cat_counts = df['category'].value_counts()
            fig_pie = px.pie(
                values=cat_counts.values, names=cat_counts.index,
                title="Semantic Distribution",
                color_discrete_sequence=px.colors.sequential.PuRd_r,
                hole=0.6
            )
            fig_pie.update_traces(textinfo='percent', hoverinfo='label+value', rotation=45)
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1', family="Outfit"), height=320,
                margin=dict(l=0, r=0, t=40, b=0), showlegend=True,
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.85)
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        
        with chart2:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            pri_counts = df['priority'].value_counts()
            colors_map = {
                'P1 Critical': '#ef4444', 'P2 High': '#f97316',
                'P3 Medium': '#3b82f6', 'P4 Low': '#22c55e'
            }
            fig_bar = px.bar(
                x=pri_counts.index, y=pri_counts.values,
                title="Priority Heatmap",
                color=pri_counts.index, color_discrete_map=colors_map,
                text=pri_counts.values
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1', family="Outfit"), height=320,
                margin=dict(l=0, r=0, t=40, b=0),
                xaxis=dict(showgrid=False, title=""), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title=""),
                showlegend=False
            )
            fig_bar.update_traces(textposition='outside')
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3: TICKET HISTORY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_history:
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not st.session_state.history:
        st.info("Log is empty. Submit a ticket in the main portal to populate the session ledger.")
    else:
        st.markdown('<div class="glass-panel"><h4>Active Session Execution Log</h4>', unsafe_allow_html=True)
        hist_df = pd.DataFrame(st.session_state.history)
        
        st.dataframe(
            hist_df,
            use_container_width=True, hide_index=True,
            column_config={
                "title": st.column_config.TextColumn("Ticket Subject", width="large"),
                "category": st.column_config.TextColumn("Class"),
                "confidence": st.column_config.ProgressColumn("Conf.", min_value=0, max_value=1, format="%.2f"),
                "escalated": st.column_config.CheckboxColumn("Bypassed AI? (L2)")
            }
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🗑️ Purge Local Session Data"):
            st.session_state.history = []
            st.rerun()
