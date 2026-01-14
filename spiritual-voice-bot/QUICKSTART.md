# Spiritual Voice Bot - Quick Start Guide

## ✨ NOW WITH INTELLIGENT LLM-POWERED RESPONSES! ✨

This bot has been **upgraded** from template-based to **AI-powered conversational responses** using Claude!

## 🚀 Quick Setup Guides

Choose your starting point:

1. **[QUICK_START.md](QUICK_START.md)** - Get running in 5 minutes! 🏃
2. **[LLM_INTEGRATION_GUIDE.md](LLM_INTEGRATION_GUIDE.md)** - Complete LLM setup guide 📖
3. **[VOICE_FIX_GUIDE.md](VOICE_FIX_GUIDE.md)** - Voice feature details 🎤
4. **[TRANSFORMATION_SUMMARY.md](TRANSFORMATION_SUMMARY.md)** - See what changed 📊

---

## Overview

This is an **intelligent voice-enabled conversational spiritual companion** grounded in Sanatan Dharma scriptures (Bhagavad Gita, Vedas, Upanishads).

### ✨ Features

✅ **LLM-Powered Responses** - Intelligent, custom answers using Claude AI (NEW!)
✅ **Scripture-Grounded** - Always references Bhagavad Gita verses
✅ **Voice Input** - Speak naturally (Whisper ASR)
✅ **Voice Output** - Hear responses (Google TTS) - NOW WORKING!
✅ **Modern Conversational Tone** - Friendly, relatable guidance
✅ **Bilingual Support** - English and Hindi
✅ **RAG Pipeline** - Semantic search for relevant teachings
✅ **Web UI** - Clean, modern interface
✅ **REST API** - Easy integration

### What Makes This Special

**NOT just a chatbot** - This is an AI spiritual companion that:
- Understands your specific situation and context
- Generates unique, personalized responses every time
- References authentic scriptures (Bhagavad Gita)
- Speaks in modern, relatable language
- Works with voice - speak and listen naturally

### Example Conversation

**You:** "I'm stressed about failing at my job"

**Bot:** *"Hey! I totally get it - job pressure can be intense. Let me share some wisdom that might shift your perspective.*

*The Bhagavad Gita 2.47 says: "You have a right to perform your prescribed duties, but you are not entitled to the fruits of your actions."*

*Here's the thing - you can control your effort, not the outcome. When you focus on doing excellent work without obsessing over success/failure, you actually perform better AND feel less stressed. Think of it like this: the best athletes aren't focused on winning during the game - they're fully present in each moment.*

*This 5000-year-old wisdom is honestly perfect for modern workplace stress!*

*Hope this helps! 🙏"*

---

## 🎯 Updated POC Status

### What's Working Now

✅ **LLM Integration** - Claude AI generates intelligent responses
✅ **Voice Output Fixed** - gTTS properly installed and working
✅ **Modern Tone** - Conversational, friendly, relatable
✅ **Custom Answers** - Every response is unique to your question
✅ **Voice Input** - Whisper transcription with improved logging
✅ **Text Q&A** - Full text interface with citations
✅ **Bilingual** - English and Hindi support
✅ **RAG Pipeline** - Semantic search for scriptures

### What's Enhanced

🚀 **Response Generation** - From templates to intelligent AI
🚀 **Conversational Quality** - Natural, context-aware dialogue
🚀 **Error Logging** - Detailed debugging information
🚀 **Documentation** - Comprehensive setup and usage guides

---

## Installation Methods

### Method 1: Docker (Recommended)

**Prerequisites:**
- Docker Desktop
- Docker Compose
- 4GB RAM minimum (8GB recommended for first-time model download)
- (Optional) NVIDIA GPU with CUDA for faster processing

**Steps:**

```bash
# 1. Navigate to project directory
cd spiritual-voice-bot

# 2. Start all services
docker-compose up -d

# 3. Check if services are running
docker-compose ps

# 4. View logs (first time may take 5-10 minutes to download ML models)
docker-compose logs -f backend

# 5. Wait for initialization to complete
# Look for: "All components initialized successfully!"

# 6. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Health Check: http://localhost:8000/health
```

**First-time Setup Notes:**
- The backend will download ~560MB of ML models on first run:
  - Sentence Transformers model (~420MB) for embeddings
  - Whisper model (~139MB) for speech recognition
- Models are cached in Docker volumes for faster subsequent starts
- Initialization takes 5-10 minutes on first run, ~30 seconds after

**To stop:**
```bash
docker-compose down
```

---

### Method 2: Manual Setup (Development)

**Prerequisites:**
- Python 3.10+
- Node.js 18+
- ffmpeg (for audio processing)

#### Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and configure environment
cp .env.example .env
# Edit .env with your settings

# 5. Start the server
uvicorn main:app --reload

# Server will start at http://localhost:8000
```

#### Frontend Setup

```bash
# 1. Navigate to frontend directory (in a new terminal)
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev

# Server will start at http://localhost:3000
```

---

## Usage Guide

### Web Interface

1. **Open Browser**: Navigate to `http://localhost:3000`

2. **Select Language**: Choose English or Hindi from the dropdown

3. **Ask Questions**:
   - **Text Input**: Type your question and press Enter or click Send
   - **Voice Input**: Click the microphone button, speak, then click again to stop

4. **View Responses**:
   - Read the answer with scriptural citations
   - Listen to audio responses (in voice mode)

### Example Questions

**English:**
- "What does the Bhagavad Gita say about controlling the mind?"
- "How can I deal with stress according to Hindu philosophy?"
- "What is Karma Yoga?"
- "Tell me about the nature of the soul"

**Hindi:**
- "मन को कैसे नियंत्रित करें?"
- "कर्म योग क्या है?"
- "आत्मा के बारे में बताएं"

---

## API Usage

### REST API Endpoints

#### 1. Health Check
```bash
curl http://localhost:8000/health
```

#### 2. Text Query
```bash
curl -X POST http://localhost:8000/api/text/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does Krishna say about duty?",
    "language": "en",
    "include_citations": true
  }'
```

#### 3. Voice Query
```bash
curl -X POST http://localhost:8000/api/voice/query \
  -F "audio=@query.wav" \
  -F "language=en" \
  --output response.wav
```

#### 4. Scripture Search
```bash
curl "http://localhost:8000/api/scripture/search?query=mind%20control&limit=5"
```

### Python Client Example

```python
import requests

# Text query
response = requests.post(
    "http://localhost:8000/api/text/query",
    json={
        "query": "How to control the mind?",
        "language": "en"
    }
)
result = response.json()
print(result["answer"])
for citation in result["citations"]:
    print(f"{citation['reference']}: {citation['text']}")
```

### API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate

# Run test script
python test_api.py

# Expected output:
# - Health check: ✓
# - Text query: ✓
# - Scripture search: ✓
# - Hindi query: ✓
```

### Voice Testing

1. Open the web interface at `http://localhost:3000`
2. Click the microphone button (ensure browser has microphone permission)
3. Speak: "What does the Bhagavad Gita say about the mind?"
4. Click microphone again to stop recording
5. Wait for processing
6. Listen to the audio response

---

## Troubleshooting

### Backend Issues

**Issue**: "ModuleNotFoundError: No module named 'transformers'"
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Issue**: "CUDA out of memory"
```bash
# Edit backend/.env
LLM_DEVICE=cpu
```

**Issue**: "Cannot connect to Qdrant"
```bash
# If using Docker:
docker-compose restart qdrant

# If manual setup: Qdrant is optional for POC (uses in-memory storage)
```

### Frontend Issues

**Issue**: "Cannot connect to API"
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check CORS settings in backend/main.py
```

**Issue**: "npm install fails"
```bash
# Clear npm cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Voice Issues

**Issue**: "Microphone not working"
- Grant browser permission to access microphone
- Use HTTPS or localhost (HTTP won't allow microphone on other domains)

**Issue**: "No audio output"
- Check browser audio settings
- Ensure speakers/headphones are connected
- Check audio file downloads in browser

---

## Performance Optimization

### CPU-only Systems

```bash
# In backend/.env
LLM_DEVICE=cpu
ASR_MODEL=openai/whisper-base  # Smaller model
```

### GPU Systems

```bash
# In backend/.env
LLM_DEVICE=cuda

# Verify GPU is detected
python -c "import torch; print(torch.cuda.is_available())"
```

### Memory Optimization

For systems with limited RAM (< 8GB):
```bash
# Use smaller models
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
ASR_MODEL=openai/whisper-tiny
```

---

## Next Steps

### Expanding the POC

1. **Add More Scriptures**:
   - Download from sources in research docs
   - Process and add to vector store
   - See `backend/scripts/ingest_scriptures.py` (to be created)

2. **Improve LLM**:
   - Integrate Airavata/OpenHathi model
   - Fine-tune on spiritual Q&A dataset
   - Implement proper prompt engineering

3. **Add Knowledge Graph**:
   - Build Neo4j database
   - Map deities, relationships, avatars
   - Implement GraphRAG

4. **Enhanced Voice**:
   - Use Indic-TTS for better Hindi pronunciation
   - Fine-tune Whisper for Sanskrit/Hindi spiritual terms

5. **Deploy to Production**:
   - Setup cloud infrastructure
   - Add authentication
   - Implement rate limiting
   - Add analytics

---

## Production Roadmap

Based on the research documents, the full production system will include:

- **Phase 1**: Complete RAG pipeline with all scriptures ✅ (POC)
- **Phase 2**: Fine-tuned Airavata LLM with spiritual persona
- **Phase 3**: Knowledge Graph integration (Neo4j)
- **Phase 4**: Multi-lingual support (Tamil, Telugu, Kannada, Marathi)
- **Phase 5**: Mobile apps (iOS/Android)
- **Phase 6**: Advanced features (user memory, personalization, multi-modal)

---

## Support & Contribution

### Reporting Issues
- Create an issue on GitHub
- Include error logs and system info
- Describe steps to reproduce

### Contributing
- Fork the repository
- Create a feature branch
- Submit pull request with description

### Resources
- Research Documents: See PDF files in project root
- API Documentation: http://localhost:8000/docs
- Project README: README.md

---

## License & Credits

### Code License
MIT License - See LICENSE file

### Scripture Texts
All scriptures used are from public domain translations (pre-1928)

### Credits
- LLM: AI4Bharat Airavata (template-based in POC)
- Embeddings: Sentence Transformers (paraphrase-multilingual-mpnet-base-v2)
- ASR: OpenAI Whisper (base model)
- TTS: Google Text-to-Speech (gTTS)
- Framework: FastAPI, Next.js, React
- Vector Store: Qdrant

---

## Contact

For questions, feedback, or collaboration:
- Email: support@spiritual-ai.com
- GitHub Issues: [Link]
- Documentation: [Link]

---

**Om Shanti Shanti Shanti** 🙏
