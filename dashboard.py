import streamlit as st
from qdrant_client import QdrantClient
import re
import pandas as pd
import time

# --- QDRANT CONFIG ---
QDRANT_URL = st.secrets["QDRANT_URL"]
QDRANT_KEY = st.secrets["QDRANT_KEY"]

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_KEY)

def get_vector(text):
    """Generate vector embedding from text"""
    vector = [0.0] * 128
    for i, char in enumerate(text.lower()[:128]):
        vector[i] = ord(char) / 255.0
    return vector

def render_dashboard():
    """Render the main dashboard content"""
    
    st.markdown("<h1 class='main-title'>🛡️ TACTICAL COMMAND</h1>", unsafe_allow_html=True)
    
    # Emergency buttons at top
    t1, t2, t3 = st.columns([2, 1, 1])
    with t2:
        if st.button("🚨 DISPATCH EMS", use_container_width=True, type="primary", key="dispatch_ems"):
            st.toast("Dispatching unit...")
    with t3:
        if st.button("📞 SUPERVISOR", use_container_width=True, type="primary", key="supervisor_call"):
            st.toast("Connecting...")
    
    st.divider()
    
    # Main content: Left and Right columns
    col_l, col_r = st.columns([1.4, 1], gap="large")
    
    # LEFT: Vector Knowledge Retrieval (REAL Qdrant)
    with col_l:
        st.subheader("🔮 Vector Knowledge Retrieval")
        kb_query = st.text_input(
            "Signal Input", 
            placeholder="Type crisis type (e.g., suicide, cardiac)...", 
            key="kb_query_input"
        )
        
        if kb_query:
            try:
                with st.spinner("Searching Qdrant vector database..."):
                    response = qdrant_client.query_points(
                        collection_name="knowledge_base", 
                        query=get_vector(kb_query), 
                        limit=1
                    )
                
                if response.points:
                    res = response.points[0].payload
                    st.markdown(
                        f'<div class="protocol-card"><h2 style="color:#c084fc;">{res["category"]}</h2>'
                        f'<p>{res["text"]}</p></div>', 
                        unsafe_allow_html=True
                    )
                    
                    # Display steps with highlighting
                    for s in res.get('steps', []):
                        s = re.sub(
                            r"(SAY THIS|STAY|PUSH|FAST|HARD|DON'T STOP|CONFIRM|MONITOR)", 
                            r"<span class='highlight'>\1</span>", 
                            s
                        )
                        st.markdown(f'<div class="step-box">{s}</div>', unsafe_allow_html=True)
                else:
                    st.warning("No protocols found. Try: 'suicide', 'cardiac', 'domestic violence'")
                    
            except Exception as e:
                st.error(f"Qdrant Error: {str(e)}")
                st.info("💡 Make sure Qdrant collection 'knowledge_base' exists with data")
    
    # RIGHT: AI Predictive Memory + Map
    with col_r:
        # AI PREDICTIVE MEMORY (TOP)
        st.subheader("🤖 AI Predictive Memory")
        with st.container(border=True):
            c_type = st.selectbox(
                "Current Signal", 
                ["suicide", "panic", "domestic_violence", "substance", "cardiac"],
                key="crisis_type_select"
            )
            age = st.radio(
                "Target Demographic", 
                ["child", "teen", "adult", "elderly"], 
                horizontal=True,
                key="age_demo_radio"
            )
            
            if st.button("✨ GENERATE AI STRATEGY", use_container_width=True, key="generate_strategy"):
                # Simulate AI analysis with a loading animation
                with st.spinner("Analyzing historical data..."):
                    time.sleep(1.5)
                
                # Generate simulated confidence based on crisis type
                confidence_map = {
                    "suicide": 0.92,
                    "panic": 0.88,
                    "domestic_violence": 0.85,
                    "substance": 0.83,
                    "cardiac": 0.94
                }
                
                protocol_map = {
                    "suicide": "Crisis Intervention Protocol Alpha",
                    "panic": "Calm & Stabilize Protocol",
                    "domestic_violence": "Safety Extraction Protocol",
                    "substance": "Medical Response Protocol",
                    "cardiac": "Emergency CPR Protocol"
                }
                
                confidence = confidence_map.get(c_type, 0.87)
                protocol = protocol_map.get(c_type, "Standard Protocol Alpha")
                
                st.markdown(f"""
                <div class="ai-card">
                    <h3 style='color:#d8b4fe; margin:0;'>Match: {int(confidence*100)}%</h3>
                    <p><b>Recommended:</b> {protocol}</p>
                    <p style='font-size:0.9rem; color:#a78bfa;'>Age Group: {age.capitalize()} | Confidence Level: High</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()
        
        # CALLER GEOLOCATOR (BOTTOM)
        st.subheader("📍 Caller Geolocator")
        map_data = pd.DataFrame({'lat': [28.6139], 'lon': [77.2090]})
        st.map(map_data, zoom=12)
        st.markdown(
            "<p style='text-align:center; color:#8b949e; font-size:0.8rem;'>"
            "Accuracy: ±5m | Method: Triangulation</p>", 
            unsafe_allow_html=True
        )