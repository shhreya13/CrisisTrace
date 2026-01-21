# CrisisTrace Ultra - Emergency Dispatch Command System

🛡️ An AI-powered emergency dispatch system with vector search, real-time analytics, and intelligent protocol recommendations.

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```

4. **Access the application**
   - The app will automatically open in your browser
   - If not, navigate to: `http://localhost:8501`

### Default Login Credentials
- **Operator ID:** `ADMIN-MAS-TRACK`
- **PIN:** `1234`

## Features

### 🔮 Vector Knowledge Retrieval (Qdrant)
- Real-time semantic search through emergency protocols
- Powered by Qdrant vector database
- Instant protocol matching based on crisis keywords

### 🤖 AI Predictive Memory Engine
- Intelligent protocol recommendations
- Context-aware analysis based on:
  - Crisis type (suicide, cardiac, domestic violence, etc.)
  - Age demographics (child, teen, adult, elderly)
  - Historical success patterns
- Confidence scoring for recommended actions

### 📍 Live Deployment & Geolocation
- Real-time caller location tracking
- Interactive map visualization
- Triangulation with ±5m accuracy

### 💬 Groq AI Assistant
- Real-time chat support powered by Groq LLM (Llama 3.3 70B)
- Tactical emergency guidance
- Protocol clarification and support

### 📊 Tactical Analytics
- Live stress monitoring
- 3D vector memory visualization
- Session tracking and mission control

### 👨‍✈️ Supervisor Bridge
- Live operator monitoring
- Secure communication channels
- Command handover capabilities

## Tech Stack

- **Frontend:** Streamlit
- **AI/LLM:** Groq (Llama 3.3 70B)
- **Vector Database:** Qdrant Cloud
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly, Streamlit Maps
- **Backend Scripts:** 
  - Memory Engine (Python)
  - Crisis API handlers
  - Data ingestion pipelines

## Project Structure

```
QDRANT-MAIN/
├── __pycache__/         # Python cache files
   ├── memory_engine.cpython-312.pyc
   └── dashboard.cpython-314.pyc
├── main.py              # Main Streamlit application
├── dashboard.py         # Dashboard as a separate page
├── memory_engine.py     # AI memory and vector processing
├── crisis_api.py        # Crisis API endpoints
├── ingest_data.py       # Data ingestion for Qdrant
├── data.json            # Crisis protocol data
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Configuration

The application comes pre-configured with:
- **Qdrant Cloud** connection (vector database)
- **Groq API** for LLM chat assistance

### API Keys
API keys are included for demonstration purposes. In a production environment, these should be stored as environment variables.

## Usage Guide

### 1. Dashboard (Main Command Center)
- **Left Panel:** Search for emergency protocols using keywords
- **Right Panel:** 
  - AI strategy generator for crisis scenarios
  - Live caller geolocation map

### 2. Navigation Pages
- **Deployment Map:** Full-screen live unit tracking
- **Vitals & Memory:** Analytics and 3D vector visualization
- **Mission Tracker:** Active session monitoring
- **Supervisor:** Monitoring and command handover
- **System Features:** Capability overview

### 3. AI Chat Assistant (Right Sidebar)
- Ask questions about protocols
- Get tactical guidance
- Clear chat history with 🗑️ button

## Demo Search Keywords

Try searching these in the Vector Knowledge Retrieval:
- `suicide`
- `cardiac arrest`
- `domestic violence`
- `panic attack`
- `substance abuse`

## Troubleshooting

### Streamlit not found
```bash
pip install streamlit
# or
python -m pip install streamlit
```

### Qdrant connection issues
- Ensure you have internet connection
- The Qdrant cloud instance must be accessible
- Check if the collection `knowledge_base` exists

### Module import errors
```bash
pip install -r requirements.txt --upgrade
```

## Notes for Judges

- This is a **demonstration system** showcasing emergency dispatch capabilities
- All API keys are included for easy testing
- The system uses **real vector search** via Qdrant for protocol matching
- AI recommendations are **simulated** based on crisis context
- Login credentials are pre-filled for quick access

## Future Enhancements

- [ ] Real-time audio transcription
- [ ] Multi-language support
- [ ] Integration with actual emergency services
- [ ] Historical case database
- [ ] Advanced analytics dashboard
- [ ] Mobile app version

## License

This project is created for demonstration purposes.

## Contact

For questions or support, please contact the development team.

---

**🛡️ CrisisTrace Ultra v3.0** | Secure Tactical Interface | Last Updated: Jan 2026