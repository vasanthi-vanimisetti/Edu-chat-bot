import os
import streamlit as st
from google import genai
from datetime import datetime

# ---------- GEMINI CLIENT ----------
client = genai.Client(api_key=os.getenv("AIzaSyCPgR14Zvjv88Ci2s3eNv2Bmz6LjWPX61A"))

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="EduClarify AI | Examination & Evaluation Explainer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
    }
    
    /* Header styling */
    .main-header {
        background: white;
        padding: 2.5rem;
        border-radius: 24px;
        box-shadow: 0 12px 35px rgba(6, 182, 212, 0.15);
        margin-bottom: 2.5rem;
        border: 1px solid #e0f2fe;
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 12px 35px rgba(6, 182, 212, 0.1);
        height: 600px;
        overflow-y: auto;
        border: 1px solid #e0f2fe;
    }
    
    /* User message */
    .user-message {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: white;
        padding: 1.3rem;
        border-radius: 18px;
        margin: 1.2rem 0;
        max-width: 78%;
        margin-left: auto;
        border-bottom-right-radius: 8px;
        position: relative;
        box-shadow: 0 6px 20px rgba(249, 115, 22, 0.25);
    }
    
    .user-message::after {
        content: '';
        position: absolute;
        right: -10px;
        top: 50%;
        transform: translateY(-50%);
        border-width: 12px 0 12px 12px;
        border-style: solid;
        border-color: transparent transparent transparent #ea580c;
    }
    
    /* Bot message */
    .bot-message {
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
        padding: 1.3rem;
        border-radius: 18px;
        margin: 1.2rem 0;
        max-width: 78%;
        border-bottom-left-radius: 8px;
        position: relative;
        border: 2px solid #e0f2fe;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.1);
    }
    
    .bot-message::before {
        content: '';
        position: absolute;
        left: -10px;
        top: 50%;
        transform: translateY(-50%);
        border-width: 12px 12px 12px 0;
        border-style: solid;
        border-color: transparent #e0f2fe transparent transparent;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 18px;
        border: 2px solid #cbd5e1;
        padding: 16px 20px;
        font-size: 16px;
        background: white;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0ea5e9;
        box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.15);
        outline: none;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-teal {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
    }
    
    .badge-coral {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
    }
    
    .badge-emerald {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    /* Status bar */
    .status-bar {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.2rem 2rem;
        border-radius: 18px;
        margin-top: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.1);
        border: 1px solid #e0f2fe;
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.8rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        border: 1px solid #e0f2fe;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(14, 165, 233, 0.2);
        border-color: #0ea5e9;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.2rem;
        display: inline-block;
        padding: 1rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    }
    
    /* Custom button */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
        color: white;
        border: none;
        padding: 14px 32px;
        border-radius: 18px;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(14, 165, 233, 0.4);
        background: linear-gradient(135deg, #0284c7 0%, #0891b2 100%);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
        border-radius: 10px;
        border: 2px solid #f1f5f9;
    }
    
    /* Stats styling */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin-top: 1.5rem;
    }
    
    .stat-item {
        flex: 1;
        text-align: center;
        padding: 1.2rem;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.1);
        border: 1px solid #e0f2fe;
    }
    
    /* Warning/Info boxes */
    .stAlert {
        border-radius: 16px;
        border-left: 6px solid #0ea5e9;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 50%, #f97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Avatar styling */
    .avatar-user {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: white;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
    }
    
    .avatar-bot {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
        color: white;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
    }
    
    /* Divider */
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, #0ea5e9 0%, #06b6d4 50%, #f97316 100%);
        border-radius: 3px;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%); padding: 2.5rem 2rem; border-radius: 0 0 24px 24px; margin: -1rem -1rem 2rem -1rem;">
        <h2 style="color: white; margin: 0; font-size: 1.8rem;">🧠 EduClarify AI</h2>
        <p style="color: rgba(255,255,255,0.95); margin: 0.5rem 0 0 0; font-size: 0.95rem;">Intelligent Academic Guidance System</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚡ Quick Actions")
    with st.expander("💭 Suggested Queries", expanded=True):
        cols = st.columns(2)
        with cols[0]:
            if st.button("📊 Grading Systems", use_container_width=True):
                st.session_state.sample_question = "Explain different grading systems used in universities worldwide"
            if st.button("🎯 Exam Patterns", use_container_width=True):
                st.session_state.sample_question = "What are common exam patterns and their purposes?"
        with cols[1]:
            if st.button("📈 GPA vs CGPA", use_container_width=True):
                st.session_state.sample_question = "Explain the difference between GPA and CGPA with examples"
            if st.button("🔍 Evaluation Types", use_container_width=True):
                st.session_state.sample_question = "What are formative and summative evaluations?"
    
    st.markdown("### 🛡️ Ethics & Boundaries")
    st.warning("""
    **What I can help with:**
    - Exam format explanations
    - Grading methodology
    - Evaluation processes
    - Academic policies
    
    **What I cannot do:**
    - Answer specific exam questions
    - Predict grades or results
    - Solve assignment problems
    - Provide personal advice
    """, icon="⚠️")
    
    st.markdown("### 📋 System Info")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🤖 Model", "Gemini", delta="AI", delta_color="off")
    with col2:
        st.metric("⚡ Version", "2.2", delta="Latest", delta_color="off")
    
    st.markdown("### 📊 Usage Stats")
    st.progress(65, text="Daily API Usage: 65%")
    
    st.markdown("---")
    st.caption("🧪 **EduClarify AI** | v2.2.1 • Made with ❤️ for education")

# ---------- HEADER ----------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="main-header">
        <div style="text-align: center;">
            <h1 class="gradient-text" style="font-size: 3rem; margin: 0; font-weight: 800;">
                EduClarify AI
            </h1>
            <p style="color: #475569; font-size: 1.2rem; margin-top: 0.5rem; font-weight: 500;">
                Your Intelligent Academic Companion
            </p>
            <div style="display: flex; justify-content: center; gap: 0.75rem; margin-top: 1.5rem; flex-wrap: wrap;">
                <span class="badge badge-teal">AI-Powered</span>
                <span class="badge badge-coral">Real-time</span>
                <span class="badge badge-emerald">Education-First</span>
                <span class="badge badge-teal">24/7 Available</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- FEATURES ----------
st.markdown("### ✨ Key Capabilities")
features = st.columns(4)
with features[0]:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);">
            📚
        </div>
        <h4 style="color: #0f172a; margin-bottom: 0.5rem;">Exam Analysis</h4>
        <p style="color: #64748b; font-size: 0.9rem; line-height: 1.5;">Deep insights into examination formats and structures</p>
    </div>
    """, unsafe_allow_html=True)

with features[1]:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);">
            ⚖️
        </div>
        <h4 style="color: #0f172a; margin-bottom: 0.5rem;">Grading Guide</h4>
        <p style="color: #64748b; font-size: 0.9rem; line-height: 1.5;">Comprehensive grading system explanations</p>
    </div>
    """, unsafe_allow_html=True)

with features[2]:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);">
            📊
        </div>
        <h4 style="color: #0f172a; margin-bottom: 0.5rem;">Evaluation Expert</h4>
        <p style="color: #64748b; font-size: 0.9rem; line-height: 1.5;">Detailed assessment methodology breakdowns</p>
    </div>
    """, unsafe_allow_html=True)

with features[3]:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);">
            🎯
        </div>
        <h4 style="color: #0f172a; margin-bottom: 0.5rem;">Policy Clarifier</h4>
        <p style="color: #64748b; font-size: 0.9rem; line-height: 1.5;">Clear explanations of academic policies</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- CHAT HISTORY ----------
if "chat" not in st.session_state:
    st.session_state.chat = []
    st.session_state.message_count = 0
    st.session_state.last_activity = datetime.now().strftime("%H:%M")

if "sample_question" in st.session_state:
    question = st.session_state.pop("sample_question")
else:
    question = ""

# ---------- CHAT INTERFACE ----------
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

st.markdown("### 💬 Interactive Assistant")
col1, col2 = st.columns([3, 1])

with col1:
    user_input = st.text_input(
        "",
        value=question,
        placeholder="Ask me about examination patterns, grading systems, evaluation methods...",
        key="user_input",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("🚀 Ask EduClarify", use_container_width=True)

# ---------- CHAT DISPLAY ----------
st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)

if st.session_state.chat:
    for sender, message in st.session_state.chat:
        if sender == "user":
            st.markdown(f"""
            <div class="user-message">
                <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                    <div class="avatar-user">
                        👤
                    </div>
                    <div style="margin-left: 12px;">
                        <strong style="font-size: 1rem;">You</strong>
                        <div style="font-size: 0.8rem; opacity: 0.9;">Student</div>
                    </div>
                </div>
                <div style="font-size: 1.05rem; line-height: 1.6;">
                    {message}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-message">
                <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                    <div class="avatar-bot">
                        🧠
                    </div>
                    <div style="margin-left: 12px;">
                        <strong style="font-size: 1rem; color: #0ea5e9;">EduClarify AI</strong>
                        <div style="font-size: 0.8rem; color: #64748b;">Academic Assistant</div>
                    </div>
                </div>
                <div style="font-size: 1.05rem; line-height: 1.6; color: #334155;">
                    {message}
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; padding: 5rem 2rem; color: #64748b;">
        <div style="font-size: 5rem; margin-bottom: 1.5rem; opacity: 0.8;">🤖</div>
        <h3 style="color: #0ea5e9; margin-bottom: 1rem; font-size: 1.8rem;">Welcome to EduClarify AI</h3>
        <p style="font-size: 1.1rem; max-width: 600px; margin: 0 auto 2rem auto; line-height: 1.6;">
            Your intelligent partner for understanding academic evaluation systems. 
            Get clear explanations about exams, grading, and academic processes.
        </p>
        <div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); padding: 2rem; border-radius: 20px; max-width: 500px; margin: 0 auto; border: 2px dashed #cbd5e1;">
            <p style="color: #475569; font-weight: 600; margin-bottom: 1rem;">💡 Try asking:</p>
            <p style="color: #0ea5e9; font-style: italic; background: white; padding: 1rem; border-radius: 12px; border-left: 4px solid #0ea5e9;">
                "Explain the difference between GPA and CGPA with examples"
            </p>
            <p style="color: #0ea5e9; font-style: italic; background: white; padding: 1rem; border-radius: 12px; border-left: 4px solid #0ea5e9; margin-top: 0.5rem;">
                "What are common exam patterns in university education?"
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- STATUS BAR ----------
current_time = datetime.now().strftime("%I:%M %p")
st.markdown(f"""
<div class="status-bar">
    <div style="display: flex; align-items: center; gap: 1rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 12px; height: 12px; background: #10b981; border-radius: 50%;"></div>
            <span style="color: #475569; font-weight: 600;">Online</span>
        </div>
        <span style="color: #64748b;">•</span>
        <span style="color: #64748b;">📊 <strong>{len([m for m in st.session_state.chat if m[0] == "user"])}</strong> queries</span>
    </div>
    <div style="text-align: center;">
        <span style="color: #64748b;">🕐 Session started: <strong>{st.session_state.last_activity}</strong></span>
    </div>
    <div style="text-align: right;">
        <span style="color: #64748b;">⏰ Current time: <strong>{current_time}</strong></span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- PROCESS INPUT ----------
if send_button and user_input:
    # Update status
    st.session_state.last_activity = datetime.now().strftime("%I:%M %p")
    
    # Add user message
    st.session_state.chat.append(("user", user_input))
    
    # Generate response
    with st.spinner("🔍 Analyzing query..."):
        try:
            prompt = f"""You are EduClarify AI, an advanced academic assistant specializing in examination systems, grading methodologies, and evaluation processes.

ROLE & TONE:
- You are professional, clear, and educational
- You break down complex academic concepts into understandable parts
- You provide structured responses with clear headings or bullet points when helpful
- You use analogies and examples to clarify concepts
- You maintain a supportive, encouraging tone

ETHICAL BOUNDARIES:
- DO NOT answer specific exam questions or problems
- DO NOT predict grades, scores, or results
- DO NOT solve assignments or homework
- DO NOT provide personal academic advice
- DO focus on general explanations and educational guidance

USER QUESTION: {user_input}

Please provide a comprehensive yet clear explanation. Structure your response to be educational and helpful. Include examples or analogies if they would help understanding."""

            response = client.models.generate_content(
                model="models/gemini-flash-lite-latest",
                contents=prompt
            )
            
            st.session_state.chat.append(("bot", response.text))
            
        except Exception as e:
            st.session_state.chat.append(("bot", f"⚠️ I apologize, but I encountered an issue while processing your request. Please try rephrasing your question or try again in a moment. Technical details: {str(e)[:100]}..."))
    
    # Clear input and scroll to bottom
    st.rerun()

# ---------- SCROLL TO BOTTOM SCRIPT ----------
st.markdown("""
<script>
    // Scroll to bottom of chat container
    var container = window.parent.document.getElementById("chat-container");
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
</script>
""", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #64748b; font-size: 0.9rem;">
    <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 1rem;">
        <span>🔐 Secure & Private</span>
        <span>•</span>
        <span>📚 Academic Focus</span>
        <span>•</span>
        <span>⚡ Real-time Responses</span>
    </div>
    <div>
        © 2024 EduClarify AI • Made for educational purposes • Powered by Gemini AI
    </div>
</div>
""", unsafe_allow_html=True)