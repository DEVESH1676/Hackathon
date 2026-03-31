"""
🎫 Intelligent Ticket Routing Agent - Chat UI Version
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

# ── Page Config (Collapsed sidebar for app-like feel) ────────
st.set_page_config(
    page_title="Nexus Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS for Chat App Look ─────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&family=Inter:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Top Navigation Header  */
    .top-header {
        background: #0f172a;
        padding: 1rem 2rem;
        border-bottom: 1px solid #1e293b;
        display: flex;
        align-items: center;
        justify-content: space-between;
        z-index: 999;
    }
    .top-header h1 {
        margin: 0; font-size: 1.5rem; color: #f8fafc;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .top-header {
        position: relative; /* Fixed sticky overlay issues with chat layout */
    }
    
    /* Main Background */
    .stApp { background-color: #0b0f19; }
    
    /* Chat Messages */
    div[data-testid="stChatMessage"] {
        background-color: transparent;
        padding: 1.5rem;
        border-bottom: 1px solid #1e293b;
        word-wrap: break-word;
        overflow-wrap: break-word;
        white-space: pre-wrap;
    }
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(30, 41, 59, 0.4);
    }
    
    /* Global text wrapping for markdown */
    .stMarkdown p, .stMarkdown div {
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    /* Classification Badges in Chat */
    .chat-badge {
        display: inline-block; padding: 4px 10px;
        border-radius: 6px; font-size: 0.75rem; font-weight: 600;
        margin-right: 8px; margin-bottom: 8px;
        font-family: 'Fira Code', monospace;
    }
    .badge-cat { background: rgba(59, 130, 246, 0.1); color: #60a5fa; border: 1px solid #3b82f6; }
    .badge-dept { background: rgba(168, 85, 247, 0.1); color: #c084fc; border: 1px solid #a855f7; }
    .badge-conf { background: rgba(34, 197, 94, 0.1); color: #4ade80; border: 1px solid #22c55e; }
    .badge-warn { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid #ef4444; }
    
    /* Floating Chat Input area */
    div[data-testid="stChatInput"] {
        padding-bottom: 2rem !important;
    }
    div[data-testid="stChatInput"] textarea {
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
        background-color: #1e293b !important;
    }
    
    /* Hide default header */
    header[data-testid="stHeader"] { display: none; }
</style>

<div class="top-header">
    <h1>⚡ Nexus L1 Autonomous Agent</h1>
    <span style="color:#64748b; font-size:0.9rem;">Hackathon MVP Build</span>
</div>
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


# ── State Session ────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to Nexus Support. Provide your issue description, and I will route the ticket and suggest a resolution immediately.", "type": "text"}
    ]

# ── Sidebar Tools (Hidden by default) ────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    conf_thresh = st.slider("Escalation Threshold", 0.0, 1.0, config.CONFIDENCE_THRESHOLD, 0.05)
    generate_res = st.toggle("Enable Generative RAG", value=True)
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()


# ── Render Chat Interface ────────────────────────────────────
# We create a container for chat to preserve layout
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"**{msg['title']}**\n\n{msg['content']}")
        else:
            with st.chat_message("assistant", avatar="⚡"):
                if msg["type"] == "text":
                    st.markdown(msg["content"])
                
                elif msg["type"] == "analysis":
                    # Draw beautiful analysis block
                    html_badges = f"""
                    <div style="margin-top: 10px; margin-bottom: 15px;">
                        <span class="chat-badge badge-cat">📁 {msg['cat']}</span>
                        <span class="chat-badge badge-dept">🏢 {msg['dept']}</span>
                        <span class="chat-badge badge-conf">🎯 {msg['conf']:.1%} Conf</span>
                    """
                    if "P1" in msg['pri'] or "Critical" in msg['pri']:
                        html_badges += f'<span class="chat-badge badge-warn">🔥 {msg["pri"]}</span>'
                    else:
                        html_badges += f'<span class="chat-badge badge-cat">✅ {msg["pri"]}</span>'
                    html_badges += "</div>"
                    
                    st.markdown(html_badges, unsafe_allow_html=True)
                    
                    # Escalation Flags
                    if msg.get('escalated'):
                        st.error(f"🚨 **Escalation Triggered:** {msg['escalation_reason']}")
                    
                    if msg.get('automation'):
                        st.info(f"🤖 **Runbook Triggered:** {msg['automation_reason']}")
                    
                    # Generative Resolution
                    if msg.get('resolution'):
                        st.markdown("### 🛠️ Suggested Resolution Action")
                        st.markdown(f"><span style='color:#e2e8f0;'> {msg['resolution']} </span>", unsafe_allow_html=True)
                        
                        with st.expander("View Reference Data"):
                            for i, doc in enumerate(msg['context']):
                                st.caption(f"Ref {i+1}: {doc[:100]}...")


# ── Chat Input & Processing ──────────────────────────────────
prompt = st.chat_input("Describe your IT issue (Title | Description)...")

if prompt:
    # 1. Parse user input
    parts = prompt.split("|", 1)
    if len(parts) > 1:
        title, desc = parts[0].strip(), parts[1].strip()
    else:
        title, desc = "IT Request", prompt.strip()
        
    user_msg = {"role": "user", "title": title, "content": desc}
    st.session_state.messages.append(user_msg)
    
    # Render user message exactly where it should be
    with chat_container:
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"**{title}**\n\n{desc}")
            
        # 2. Process Assistant Response
        with st.chat_message("assistant", avatar="⚡"):
            with st.status("Analyzing routing vectors...", expanded=True) as status:
                st.write("Extracting semantic embeddings...")
                clf = load_classifier()
                classification = clf.classify(title, desc)
                
                st.write("Evaluating policy engines...")
                agent = load_agent()
                agent_result = agent.process(title, desc, classification)
                
                rag_result = None
                if generate_res:
                    st.write("Synthesizing resolution from RAG...")
                    rag = load_rag_engine()
                    rag_result = rag.suggest_resolution(title, desc)
                
                status.update(label="Analysis Complete", state="complete", expanded=False)
            
            # Build assistant response object
            response_data = {
                "role": "assistant",
                "type": "analysis",
                "content": "",
                "cat": classification["category"],
                "dept": classification["department"],
                "conf": classification["confidence"],
                "pri": classification["priority_suggestion"],
                "escalated": agent_result.get("requires_human", False),
                "automation": agent_result.get("suggests_automation", False)
            }
            
            if response_data["escalated"]:
                response_data["escalation_reason"] = [a['reason'] for a in agent_result['agent_actions'] if a['type'] == 'ESCALATE'][0]
            
            if response_data["automation"]:
                response_data["automation_reason"] = [a['reason'] for a in agent_result['agent_actions'] if a['type'] == 'SUGGEST_AUTOMATION'][0]
            
            if rag_result:
                response_data["resolution"] = rag_result['suggested_resolution']
                response_data["context"] = rag_result['context_docs']
                
            # Draw beautiful analysis block
            html_badges = f"""
            <div style="margin-top: 10px; margin-bottom: 15px;">
                <span class="chat-badge badge-cat">📁 {response_data['cat']}</span>
                <span class="chat-badge badge-dept">🏢 {response_data['dept']}</span>
                <span class="chat-badge badge-conf">🎯 {response_data['conf']:.1%} Conf</span>
            """
            if "P1" in response_data['pri'] or "Critical" in response_data['pri']:
                html_badges += f'<span class="chat-badge badge-warn">🔥 {response_data["pri"]}</span>'
            else:
                html_badges += f'<span class="chat-badge badge-cat">✅ {response_data["pri"]}</span>'
            html_badges += "</div>"
            
            st.markdown(html_badges, unsafe_allow_html=True)
            
            # Escalation Flags
            if response_data.get('escalated'):
                st.error(f"🚨 **Escalation Triggered:** {response_data['escalation_reason']}")
            
            if response_data.get('automation'):
                st.info(f"🤖 **Runbook Triggered:** {response_data['automation_reason']}")
            
            # Generative Resolution
            if response_data.get('resolution'):
                st.markdown("### 🛠️ Suggested Resolution Action")
                st.markdown(f"><span style='color:#e2e8f0;'> {response_data['resolution']} </span>", unsafe_allow_html=True)
                
                with st.expander("View Reference Data"):
                    for i, doc in enumerate(response_data['context']):
                        st.caption(f"Ref {i+1}: {doc[:100]}...")
            
            # Save assistant message to state so it persists on next app reload
            st.session_state.messages.append(response_data)

