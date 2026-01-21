import streamlit as st
from qdrant_client import QdrantClient
import pandas as pd
import numpy as np
import plotly.express as px
from groq import Groq
import time
import re

# Import dashboard module
import dashboard

# --- CONFIG & GROQ ---
GROQ_KEY = st.secrets["GROQ_KEY"]
groq_client = Groq(api_key=GROQ_KEY)

# --- QDRANT CONFIG (from dashboard.py) ---
QDRANT_URL = st.secrets["QDRANT_URL"]
QDRANT_KEY =st.secrets["QDRANT_KEY"]
API_URL = "http://127.0.0.1:5005/recommend"

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_KEY)

st.set_page_config(page_title="CrisisTrace Ultra", layout="wide", page_icon="🛡️")

# --- HELPER FUNCTION FOR VECTOR (from dashboard.py) ---
def get_vector(text):
    vector = [0.0] * 128
    for i, char in enumerate(text.lower()[:128]):
        vector[i] = ord(char) / 255.0
    return vector

# --- UI CSS & FONT SIZE INCREASE ---
st.markdown("""
    <style>
    /* Global Font Size Increases */
    html, body, [class*="st-"] {
        font-size: 1.15rem !important; 
    }
    h1 { font-size: 3.5rem !important; }
    h2 { font-size: 2.5rem !important; }
    h3 { font-size: 1.8rem !important; }
    
    [data-testid="stSidebar"] { display: none; }
    .stApp { background: radial-gradient(circle at top, #1a0b2e 0%, #0d1117 100%); color: #e0d7ff; }
    
    .main-title { 
        background: linear-gradient(90deg, #9d50bb, #f0abfc); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-weight: 800; 
        text-align: center; 
    }
    
    .feature-card { 
        background: rgba(123, 44, 191, 0.1); 
        border: 2px solid #7b2cbf; 
        border-radius: 15px; 
        padding: 25px; 
    }
    
    /* Protocol Cards (from dashboard.py) */
    .protocol-card { 
        background: rgba(26, 11, 46, 0.6); 
        border: 1px solid #7b2cbf; 
        border-radius: 20px; 
        padding: 25px; 
        backdrop-filter: blur(10px); 
    }
    
    .ai-card { 
        background: linear-gradient(135deg, #240b36 0%, #1a0b2e 100%); 
        border: 1px solid #9d50bb; 
        border-radius: 20px; 
        padding: 25px; 
        margin-bottom: 20px; 
    }
    
    .step-box { 
        background: rgba(0, 0, 0, 0.4); 
        border-left: 5px solid #9d50bb; 
        padding: 15px; 
        margin: 10px 0; 
        border-radius: 5px; 
        font-family: 'JetBrains Mono', monospace; 
    }
    
    .highlight { 
        color: #f0abfc; 
        font-weight: bold; 
    }
    
    /* Input Label Font Styling */
    .stTextInput label, .stSelectbox label, .stRadio label {
        font-size: 1.3rem !important;
        font-weight: bold !important;
        color: #f0abfc !important;
    }
    
    /* Map Styling */
    [data-testid="stMap"] { 
        border: 2px solid #7b2cbf; 
        border-radius: 15px; 
        overflow: hidden; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATES ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'page' not in st.session_state: st.session_state.page = "Dashboard"
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()

# --- LOGIN ---
if not st.session_state.authenticated:
    st.markdown("""
        <style>
        .login-title {
            background: linear-gradient(90deg, #f0abfc, #9d50bb, #f0abfc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 4rem !important;
            font-weight: 900;
            text-align: center;
            margin-bottom: 20px;
            text-shadow: 0 0 30px rgba(240, 171, 252, 0.6);
            animation: glow 2s ease-in-out infinite;
        }
        
        @keyframes glow {
            0%, 100% { filter: brightness(1); }
            50% { filter: brightness(1.3); }
        }
        
        .login-subtitle {
            color: #c77dff;
            text-align: center;
            font-size: 1.3rem;
            margin-bottom: 40px;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([0.5, 2, 0.5])
    
    with col:
        st.markdown("<h1 class='login-title'>🛡️ CRISISTRACE ULTRA</h1>", unsafe_allow_html=True)
        st.markdown("<p class='login-subtitle'>Emergency Dispatch Command System</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("### 🔐 Operator Authentication")
            
            operator_id = st.text_input(
                "Operator ID", 
                value="ADMIN-MAS-TRACK",
                placeholder="Enter your operator ID",
                help="Enter your authorized operator identification"
            )
            
            pin = st.text_input(
                "Security PIN", 
                type="password", 
                value="1234",
                placeholder="Enter your 4-digit PIN",
                help="Enter your secure access PIN"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 INITIALIZE SYSTEM", use_container_width=True, type="primary"):
                    if operator_id and pin:
                        with st.spinner("Authenticating..."):
                            time.sleep(1)
                            st.session_state.authenticated = True
                            st.success("✅ Authentication Successful!")
                            time.sleep(0.5)
                            st.rerun()
                    else:
                        st.error("⚠️ Please enter both Operator ID and PIN")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center; color: #7b2cbf; font-size: 0.9rem;'>
                🔒 Encrypted Connection | Protocol Version 4.5 | Last Updated: Jan 2026
            </div>
        """, unsafe_allow_html=True)
else:
    # Top Navbar
    nav = st.columns(6)
    labels = ["Dashboard", "Deployment Map", "Vitals & Memory", "Mission Tracker", "Supervisor", "System Features"]
    for i, label in enumerate(labels):
        if nav[i].button(label, use_container_width=True):
            st.session_state.page = label

    left_content, chat_sidebar = st.columns([2.2, 0.8])

    with left_content:
        # --- PAGE: DASHBOARD (INTEGRATED FROM dashboard.py) ---
        if st.session_state.page == "Dashboard":
            # Call the dashboard render function
            dashboard.render_dashboard()

        # --- PAGE: DEPLOYMENT MAP ---
        elif st.session_state.page == "Deployment Map":
            st.markdown("<h1 class='main-title'>LIVE DEPLOYMENT MAP</h1>", unsafe_allow_html=True)
            with st.container(border=True):
                map_data = pd.DataFrame({'lat': [28.6139], 'lon': [77.2090]})
                st.map(map_data, zoom=12)
                
        # --- PAGE: VITALS & MEMORY ---
        elif st.session_state.page == "Vitals & Memory":
            st.markdown("<h1 class='main-title'>TACTICAL ANALYTICS</h1>", unsafe_allow_html=True)
            st.subheader("📈 Live Stress Monitor")
            st.line_chart(np.random.normal(75, 10, size=25), color="#e91e63")
                        
            st.subheader("🧠 3D Qdrant Memory Map")
            df = pd.DataFrame({'x': np.random.randn(50), 'y': np.random.randn(50), 'z': np.random.randn(50)})
            st.plotly_chart(px.scatter_3d(df, x='x', y='y', z='z', color_discrete_sequence=['#9d50bb']), use_container_width=True)

        # --- PAGE: MISSION TRACKER ---
        elif st.session_state.page == "Mission Tracker":
            st.markdown("<h1 class='main-title'>MISSION CONTROL</h1>", unsafe_allow_html=True)
            elapsed = int(time.time() - st.session_state.start_time)
            st.metric("⏱️ Active Session Timer", f"{elapsed//60:02d}:{elapsed%60:02d}", "Critical Window")
            st.checkbox("Location Triangulated", value=True)
            st.checkbox("EMS Dispatched")
            
        # --- PAGE: SUPERVISOR ---
        elif st.session_state.page == "Supervisor":
            st.markdown("<h1 class='main-title'>SUPERVISOR BRIDGE</h1>", unsafe_allow_html=True)
            st.error("🔒 SECURE LINE: MONITORING OPERATOR #901")
            st.text_area("Live Transcript Feed", "Operator: Please remain calm...", height=250)
            if st.button("🚀 INITIATE COMMAND HANDOVER"):
                st.toast("Handing over...")

        # --- PAGE: FEATURES ---
        elif st.session_state.page == "System Features":
            st.markdown("<h1 class='main-title'>SYSTEM CAPABILITIES</h1>", unsafe_allow_html=True)
            st.markdown("<div class='feature-card'><h3>🚀 Vector Pulse</h3>Qdrant-powered protocol retrieval with semantic search.</div><br>", unsafe_allow_html=True)
            st.markdown("<div class='feature-card'><h3>🤖 AI Memory Engine</h3>Predictive outcome analysis based on historical clusters.</div><br>", unsafe_allow_html=True)
            st.markdown("<div class='feature-card'><h3>📍 Real-time Geolocation</h3>Caller triangulation with ±5m accuracy.</div>", unsafe_allow_html=True)

    # --- THE RIGHT CHATBOX ---
    with chat_sidebar:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("### 🤖 Groq Assistant")
            
            # Clear button
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🗑️ Clear", key="clear_chat"):
                    st.session_state.chat_history = []
                    st.rerun()
            
            # Chat display
            chat_box = st.container(height=500)
            with chat_box:
                if len(st.session_state.chat_history) == 0:
                    st.info("👋 Ask about emergency protocols!")
                
                for msg in st.session_state.chat_history:
                    if msg["role"] == "user":
                        st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #9d50bb, #c77dff);
                                border: 2px solid #f0abfc;
                                border-radius: 15px;
                                padding: 15px;
                                margin: 10px 0;
                                box-shadow: 0 4px 15px rgba(157, 80, 187, 0.4);
                            ">
                                <p style="
                                    color: #ffffff;
                                    font-weight: 600;
                                    font-size: 1.15rem;
                                    margin: 0;
                                    text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
                                ">👤 {msg['content']}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #7b2cbf, #9d4edd);
                                border: 2px solid #c77dff;
                                border-radius: 15px;
                                padding: 15px;
                                margin: 10px 0;
                                box-shadow: 0 4px 15px rgba(123, 44, 191, 0.4);
                            ">
                                <p style="
                                    color: #e0d7ff;
                                    font-weight: 600;
                                    font-size: 1.15rem;
                                    margin: 0;
                                    line-height: 1.6;
                                ">🤖 {msg['content']}</p>
                            </div>
                        """, unsafe_allow_html=True)
            
            # Chat input
            prompt = st.chat_input("Ask about protocols...")
            if prompt:
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                
                try:
                    response = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "You are a professional emergency dispatch assistant. Be brief and tactical."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=500
                    )
                    
                    assistant_response = response.choices[0].message.content
                    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Groq Error: {str(e)}")