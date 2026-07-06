import streamlit as st

st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the Hybrid UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&display=swap');

    /* Base Styling */
    .stApp {
        background-color: #FAFAFA;
        color: #1A1A1A;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E5EA;
    }
    
    /* Hide Streamlit Header */
    header {visibility: hidden;}
    .block-container {
        padding-top: 1rem;
        max-width: 900px;
        margin: auto;
    }

    /* Sidebar Links (HTML injection) */
    .sidebar-section {
        font-size: 11px;
        text-transform: uppercase;
        font-weight: 600;
        color: #8E8E93;
        margin-bottom: 8px;
        margin-top: 24px;
    }

    .sidebar-link {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 12px 14px;
        border-radius: 12px;
        color: #111827;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s;
        text-decoration: none;
    }
    
    .sidebar-link:hover {
        background-color: #F3F4F6;
    }
    
    .sidebar-link.active {
        background-color: #EBEBFA;
        color: #5E5CE6;
    }

    /* Main Title */
    .hero-title {
        font-family: 'Instrument Serif', serif;
        font-size: 52px;
        font-weight: 400;
        margin-bottom: 40px;
        color: #1A1A1A;
        text-align: center;
        margin-top: 10vh;
    }

    /* Custom Search Box Styling */
    .search-box-container {
        background: white;
        border-radius: 24px;
        padding: 8px 16px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04);
        border: 1px solid #E5E5EA;
        margin-bottom: 24px;
    }

    .stTextInput > div > div > input {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        padding: 12px 4px !important;
        font-size: 16px !important;
        color: #1A1A1A;
    }
    
    /* Pill Buttons */
    .suggestion-container {
        display: flex;
        gap: 12px;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .stButton > button {
        background-color: #FFFFFF;
        border: 1px solid #E5E5EA;
        border-radius: 24px;
        padding: 6px 18px;
        color: #4B5563;
        font-size: 13px;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #F9F9F9;
        border-color: #D1D1D6;
        color: #1A1A1A;
    }

</style>
""", unsafe_allow_html=True)

# -----------------
# SIDEBAR
# -----------------
with st.sidebar:
    # Custom SVG Blue Book Logo
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 32px; padding-left: 8px;">
        <svg width="36" height="36" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="50" fill="#2CB5E8"/>
            <path d="M15 75C25 70 35 70 50 80V35C35 25 25 25 15 30V75Z" fill="white"/>
            <path d="M85 75C75 70 65 70 50 80V35C65 25 75 25 85 30V75Z" fill="white"/>
            <path d="M50 35V80" stroke="#2CB5E8" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M22 42C30 38 40 40 46 45" stroke="#2CB5E8" stroke-width="2" stroke-linecap="round"/>
            <path d="M22 52C30 48 40 50 46 55" stroke="#2CB5E8" stroke-width="2" stroke-linecap="round"/>
            <path d="M22 62C30 58 40 60 46 65" stroke="#2CB5E8" stroke-width="2" stroke-linecap="round"/>
            <path d="M78 42C70 38 60 40 54 45" stroke="#2CB5E8" stroke-width="2" stroke-linecap="round"/>
            <path d="M78 52C70 48 60 50 54 55" stroke="#2CB5E8" stroke-width="2" stroke-linecap="round"/>
            <path d="M78 62C70 58 60 60 54 65" stroke="#2CB5E8" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <span style="font-size: 18px; font-weight: 700; color: #111827;">ResearchMind</span>
    </div>
    
    <div class="sidebar-section">Workspace</div>
    <div class="sidebar-link active"><span>➕</span> New Research</div>
    <div class="sidebar-link"><span>🕒</span> Recents</div>
    <div class="sidebar-link"><span>📚</span> Library</div>
    
    <div class="sidebar-section">Features</div>
    <div class="sidebar-link"><span>🔍</span> Deep Search</div>
    <div class="sidebar-link"><span>📄</span> Document Analysis</div>
    <div class="sidebar-link"><span>📊</span> Generated Reports</div>
    
    <div style="margin-top: 150px;">
        <div class="sidebar-link"><span>⚙️</span> Settings</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------
# MAIN CONTENT
# -----------------
st.markdown('<h1 class="hero-title">What would you like to research?</h1>', unsafe_allow_html=True)

# Fake search box container with Streamlit inputs inside
st.markdown('<div class="search-box-container">', unsafe_allow_html=True)

# Use columns to mimic the + button, text input, and send button
col1, col2 = st.columns([8, 1])

with col1:
    query = st.text_input("Search", label_visibility="collapsed", placeholder="Assign a research task...")
with col2:
    st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)
    submit_btn = st.button("⬆")

st.markdown('</div>', unsafe_allow_html=True)

# File uploader mimicking the '+' functionality
with st.expander("➕ Import PDFs / Files for Document Analysis", expanded=False):
    uploaded_file = st.file_uploader("Upload your document", type=['pdf', 'docx', 'txt'], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"Attached Document: {uploaded_file.name}")

st.markdown("<br>", unsafe_allow_html=True)

# Suggestion Pills
scol1, scol2, scol3, scol4 = st.columns([1,1,1,1])
with scol1:
    btn1 = st.button("📄 Analyze PDF")
with scol2:
    btn2 = st.button("🔍 Deep Web Search")
with scol3:
    btn3 = st.button("🖥️ Compare Datasets")
with scol4:
    btn4 = st.button("🧠 Fact Check")

if query or submit_btn or btn1 or btn2 or btn3 or btn4:
    action = query if query else "Selected Action"
    if uploaded_file:
        action += f" (with file: {uploaded_file.name})"
    
    st.markdown("<hr>", unsafe_allow_html=True)
    with st.spinner("Analyzing your request..."):
        import time
        time.sleep(2)
        
        st.success(f"Research Task Started: {action}")
        
        st.markdown("""
        <div style="border: 1px solid #E5E5EA; border-radius: 12px; padding: 20px; background: white; margin-top: 10px;">
            <h4 style="margin-top: 0; color: #111827;">Research Findings</h4>
            <p style="color: #4B5563; font-size: 14px;">The AI agents are compiling the most relevant sources and generating your deep analysis. Please wait while the graph executes.</p>
        </div>
        """, unsafe_allow_html=True)
