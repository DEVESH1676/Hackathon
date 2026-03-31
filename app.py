"""
🎫 Intelligent Ticket Routing & Resolution Agent
Streamlit Dashboard — Hackathon Demo
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
    page_title="AI Ticket Agent",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    
    /* ── Hero Header ── */
    .hero-title {
        font-size: 2rem; font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .hero-sub { color: #94a3b8; font-size: 0.95rem; margin-top: -0.3rem; }
    
    /* ── Metric Cards ── */
    .metric-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155; border-radius: 12px;
        padding: 1.2rem; text-align: center;
    }
    .metric-card h2 { color: #f8fafc; margin: 0; font-size: 1.8rem; }
    .metric-card p  { color: #94a3b8; margin: 0; font-size: 0.85rem; }
    
    /* ── Result Cards ── */
    .result-box {
        background: #1e293b; border: 1px solid #334155;
        border-radius: 12px; padding: 1.2rem; margin-bottom: 0.8rem;
    }
    .result-box h4 { color: #e2e8f0; margin-top: 0; }
    
    /* ── Priority Badges ── */
    .badge-p1 { background: #dc2626; color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
    .badge-p2 { background: #f97316; color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
    .badge-p3 { background: #3b82f6; color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
    .badge-p4 { background: #22c55e; color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }

    /* ── Escalation Banner ── */
    .escalation-banner {
        background: linear-gradient(135deg, #7f1d1d, #991b1b);
        border: 1px solid #dc2626; border-radius: 10px;
        padding: 1rem; color: #fecaca;
    }
    .automation-banner {
        background: linear-gradient(135deg, #1e3a5f, #1e40af);
        border: 1px solid #3b82f6; border-radius: 10px;
        padding: 1rem; color: #bfdbfe;
    }
    
    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown p { color: #cbd5e1; }
    
    /* ── Tab styling ── */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: #1e293b; border-radius: 8px;
        border: 1px solid #334155; color: #94a3b8;
        padding: 8px 18px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important; border: none;
    }
</style>
""", unsafe_allow_html=True)


# ── Cached Model Loading ─────────────────────────────────────
@st.cache_resource(show_spinner="Loading AI models...")
def load_classifier():
    from core.classifier import TicketClassifier
    return TicketClassifier()

@st.cache_resource(show_spinner="Loading RAG engine...")
def load_rag_engine():
    from core.rag import ResolutionEngine
    return ResolutionEngine()

@st.cache_resource(show_spinner="Loading agent layer...")
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
    st.markdown('<p class="hero-title">🎫 AI Ticket Agent</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Intelligent Routing & Resolution</p>', unsafe_allow_html=True)
    st.divider()
    
    st.markdown("#### ⚙️ Configuration")
    confidence_threshold = st.slider(
        "Escalation Threshold", 0.0, 1.0, config.CONFIDENCE_THRESHOLD, 0.05,
        help="Tickets below this confidence get escalated to L2 Human Triage."
    )
    similarity_threshold = st.slider(
        "Repeat Detection Threshold", 0.0, 1.0, config.SIMILARITY_THRESHOLD, 0.05,
        help="Cosine similarity above which tickets are considered duplicates."
    )
    generate_resolution = st.toggle("🤖 Generate AI Resolution", value=False,
        help="Enable to call the LLM for a step-by-step resolution. Requires Ollama connectivity."
    )
    
    st.divider()
    st.markdown("#### 📡 System Status")
    st.markdown(f"**LLM Backend:** `{config.OLLAMA_MODEL}`")
    st.markdown(f"**Embeddings:** `{config.EMBEDDING_MODEL_NAME}`")
    st.markdown(f"**Vector DB:** ChromaDB (local)")
    
    st.divider()
    st.caption("Built for 48hr Hackathon · v1.0")


# ── Helper Functions ─────────────────────────────────────────
def priority_badge(priority: str) -> str:
    p = priority.lower()
    if "p1" in p or "critical" in p: return f'<span class="badge-p1">{priority}</span>'
    if "p2" in p or "high" in p:     return f'<span class="badge-p2">{priority}</span>'
    if "p3" in p or "medium" in p:   return f'<span class="badge-p3">{priority}</span>'
    return f'<span class="badge-p4">{priority}</span>'

def confidence_color(conf: float) -> str:
    if conf >= 0.8: return "#22c55e"
    if conf >= 0.6: return "#f97316"
    return "#dc2626"


# ── Main Content ─────────────────────────────────────────────
tab_submit, tab_dashboard, tab_history = st.tabs([
    "🎫 Submit Ticket", "📊 Analytics Dashboard", "📋 Ticket History"
])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1: SUBMIT TICKET
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_submit:
    st.markdown("### 🎫 Submit a New IT Support Ticket")
    st.markdown("Enter the ticket details below. The AI will classify, route, and optionally resolve it in real time.")
    
    col_input, col_result = st.columns([1, 1], gap="large")
    
    with col_input:
        with st.form("ticket_form", clear_on_submit=False):
            ticket_title = st.text_input(
                "Ticket Title",
                placeholder="e.g., VPN connection dropping for remote users"
            )
            ticket_desc = st.text_area(
                "Description",
                placeholder="Describe the issue in detail. Include server names, error codes, and affected users...",
                height=180
            )
            submitted = st.form_submit_button("🚀 Analyze Ticket", use_container_width=True, type="primary")
    
    with col_result:
        if submitted and ticket_title and ticket_desc:
            # ── Step 1: Classify ──
            with st.spinner("🧠 Classifying ticket..."):
                clf = load_classifier()
                classification = clf.classify(ticket_title, ticket_desc)
                time.sleep(0.3)  # slight delay for visual effect
            
            # ── Step 2: Agent Layer ──
            with st.spinner("🤖 Running agentic checks..."):
                agent = load_agent()
                agent_result = agent.process(ticket_title, ticket_desc, classification)
                time.sleep(0.2)
            
            # ── Display Classification Result ──
            conf = classification["confidence"]
            cat = classification["category"]
            dept = classification["department"]
            pri = classification["priority_suggestion"]
            
            st.markdown(f"""
            <div class="result-box">
                <h4>✅ Classification Result</h4>
                <table style="width:100%; color: #cbd5e1;">
                    <tr><td style="padding: 4px 0;">📂 <strong>Category</strong></td>
                        <td style="text-align:right;"><strong style="color:#818cf8;">{cat}</strong></td></tr>
                    <tr><td style="padding: 4px 0;">🏢 <strong>Department</strong></td>
                        <td style="text-align:right;">{dept}</td></tr>
                    <tr><td style="padding: 4px 0;">🎯 <strong>Confidence</strong></td>
                        <td style="text-align:right;"><strong style="color:{confidence_color(conf)};">{conf:.1%}</strong></td></tr>
                    <tr><td style="padding: 4px 0;">🔥 <strong>Priority</strong></td>
                        <td style="text-align:right;">{priority_badge(pri)}</td></tr>
                    <tr><td style="padding: 4px 0;">⚙️ <strong>Method</strong></td>
                        <td style="text-align:right;">{classification["method"]}</td></tr>
                </table>
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
                        color=['#818cf8' if k == cat else '#334155' for k in scores.keys()],
                        line=dict(width=0)
                    ),
                    text=[f"{v:.1%}" for v in scores.values()],
                    textposition='auto'
                ))
                fig_scores.update_layout(
                    title="Category Similarity Scores",
                    height=250, margin=dict(l=0, r=0, t=40, b=0),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#94a3b8', size=11),
                    xaxis=dict(showgrid=False, range=[0, 1]),
                    yaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig_scores, use_container_width=True)
            
            # ── Agent Actions ──
            if agent_result.get("requires_human"):
                for action in agent_result["agent_actions"]:
                    if action["type"] == "ESCALATE":
                        st.markdown(f"""
                        <div class="escalation-banner">
                            ⚠️ <strong>ESCALATION REQUIRED</strong><br>
                            {action['reason']}<br>
                            <em>{action['action']}</em>
                        </div>
                        """, unsafe_allow_html=True)
            
            if agent_result.get("suggests_automation"):
                for action in agent_result["agent_actions"]:
                    if action["type"] == "SUGGEST_AUTOMATION":
                        st.markdown(f"""
                        <div class="automation-banner">
                            🤖 <strong>AUTOMATION SUGGESTED</strong><br>
                            {action['reason']}<br>
                            <em>{action['action']}</em>
                        </div>
                        """, unsafe_allow_html=True)
            
            # ── Similar Tickets ──
            similar = classification.get("similar_tickets", [])
            if similar:
                with st.expander(f"🔍 Top {len(similar)} Similar Past Tickets", expanded=False):
                    for i, t in enumerate(similar):
                        st.markdown(f"""
                        **{i+1}.** [{t['category']}] {priority_badge(t['priority'])} — 
                        Similarity: `{t['similarity']:.1%}`  
                        {t['document'][:120]}...
                        """, unsafe_allow_html=True)
                        if t.get("resolution"):
                            st.caption(f"📝 Past fix: {t['resolution'][:150]}...")
                        st.divider()
            
            # ── RAG Resolution ──
            if generate_resolution:
                with st.spinner("📝 Generating AI resolution..."):
                    rag = load_rag_engine()
                    rag_result = rag.suggest_resolution(ticket_title, ticket_desc)
                
                st.markdown("### 📝 AI-Suggested Resolution")
                st.markdown(f"""
                <div class="result-box">
                    {rag_result['suggested_resolution']}
                </div>
                """, unsafe_allow_html=True)
            
            # ── Save to History ──
            st.session_state.history.append({
                "title": ticket_title,
                "description": ticket_desc,
                "category": cat,
                "department": dept,
                "confidence": conf,
                "priority": pri,
                "escalated": agent_result.get("requires_human", False),
                "method": classification["method"]
            })
            
        elif submitted:
            st.warning("Please fill in both the title and description.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2: ANALYTICS DASHBOARD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_dashboard:
    st.markdown("### 📊 Analytics Dashboard")
    
    df = load_ticket_data()
    
    if df.empty:
        st.warning("No ticket data found. Ingest tickets first.")
    else:
        # ── Top Metrics ──
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""<div class="metric-card">
                <h2>{len(df)}</h2><p>Total Tickets</p>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class="metric-card">
                <h2>{df['category'].nunique()}</h2><p>Categories</p>
            </div>""", unsafe_allow_html=True)
        with m3:
            p1_count = len(df[df['priority'].str.contains('P1', case=False, na=False)])
            st.markdown(f"""<div class="metric-card">
                <h2>{p1_count}</h2><p>Critical (P1)</p>
            </div>""", unsafe_allow_html=True)
        with m4:
            session_count = len(st.session_state.history)
            escalated = sum(1 for h in st.session_state.history if h.get("escalated"))
            rate = f"{escalated/session_count:.0%}" if session_count > 0 else "N/A"
            st.markdown(f"""<div class="metric-card">
                <h2>{rate}</h2><p>Escalation Rate (session)</p>
            </div>""", unsafe_allow_html=True)
        
        st.markdown("")  # spacer
        
        # ── Charts Row ──
        chart1, chart2 = st.columns(2)
        
        with chart1:
            cat_counts = df['category'].value_counts()
            fig_pie = px.pie(
                values=cat_counts.values,
                names=cat_counts.index,
                title="Tickets by Category",
                color_discrete_sequence=px.colors.sequential.Purples_r,
                hole=0.45
            )
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'), height=350,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with chart2:
            pri_counts = df['priority'].value_counts()
            colors_map = {
                'P1 Critical': '#dc2626', 'P2 High': '#f97316',
                'P3 Medium': '#3b82f6', 'P4 Low': '#22c55e'
            }
            fig_bar = px.bar(
                x=pri_counts.index, y=pri_counts.values,
                title="Tickets by Priority",
                color=pri_counts.index,
                color_discrete_map=colors_map
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'), height=350,
                margin=dict(l=20, r=20, t=50, b=20),
                xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#1e293b'),
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # ── Department Routing Table ──
        st.markdown("#### 🏢 Department Routing Map")
        dept_df = df.groupby(['category', 'department']).size().reset_index(name='tickets')
        dept_df = dept_df.sort_values('tickets', ascending=False)
        st.dataframe(dept_df, use_container_width=True, hide_index=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3: TICKET HISTORY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_history:
    st.markdown("### 📋 Session Ticket History")
    
    if not st.session_state.history:
        st.info("No tickets analyzed yet in this session. Go to **🎫 Submit Ticket** to get started.")
    else:
        hist_df = pd.DataFrame(st.session_state.history)
        
        # Summary metrics
        h1, h2, h3 = st.columns(3)
        with h1:
            st.metric("Total Analyzed", len(hist_df))
        with h2:
            avg_conf = hist_df['confidence'].mean()
            st.metric("Avg Confidence", f"{avg_conf:.1%}")
        with h3:
            esc_count = hist_df['escalated'].sum()
            st.metric("Escalated", f"{esc_count}/{len(hist_df)}")
        
        st.dataframe(
            hist_df[['title', 'category', 'department', 'confidence', 'priority', 'escalated', 'method']],
            use_container_width=True, hide_index=True,
            column_config={
                "title": st.column_config.TextColumn("Title", width="large"),
                "confidence": st.column_config.ProgressColumn("Confidence", min_value=0, max_value=1, format="%.1%%"),
                "escalated": st.column_config.CheckboxColumn("Escalated?")
            }
        )
        
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
