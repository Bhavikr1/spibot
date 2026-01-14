# 🎉 Local Testing Guide - Your Bot is LIVE!

## ✅ What's Running

### Backend Server
- **Status**: ✅ RUNNING
- **URL**: http://localhost:8000
- **Port**: 8000
- **Dataset**: 701 Bhagavad Gita verses loaded
- **Components**: RAG ✅ | ASR ✅ | TTS ✅

### Frontend Server
- **Status**: ✅ RUNNING
- **URL**: http://localhost:3000
- **Port**: 3000

---

## 🚀 Quick Test (Right Now!)

### 1. Test Backend API

```bash
curl -X POST http://localhost:8000/api/text/query \
  -H "Content-Type: application/json" \
  -d '{"query":"How do I control my mind?","language":"en"}'
```

**Expected**: You'll get relevant verses from Bhagavad Gita Chapter 6!

### 2. Open Frontend

**Open in your browser:**
```
http://localhost:3000
```

You should see the Spiritual Voice Bot interface!

---

## 🎤 Testing Voice Features

### Voice Input (Speak to the Bot)

1. **Open** http://localhost:3000
2. **Grant microphone permission** when prompted
3. **Click** the microphone/record button
4. **Speak clearly**: "How can I find inner peace?"
5. **Click** stop recording
6. **Watch**: Bot transcribes → searches verses → responds!

### Voice Output (Hear Responses)

- Responses are automatically converted to speech
- You'll hear the bot speak the answer
- Uses Google TTS for natural speech

---

## 📊 What's Working

### ✅ Data & Search
- **701 complete Bhagavad Gita verses** (all 18 chapters)
- **Semantic search** with 768-dimensional embeddings
- **Top-5 relevant verses** for each query
- **Multi-language support** (English, Hindi, Sanskrit)

### ✅ Backend API Endpoints

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Text Query:**
```bash
curl -X POST http://localhost:8000/api/text/query \
  -H "Content-Type: application/json" \
  -d '{"query":"YOUR_QUESTION","language":"en"}'
```

**API Documentation:**
```
http://localhost:8000/docs
```
Interactive Swagger UI to test all endpoints!

### ✅ Voice Processing
- **ASR (Speech Recognition)**: Whisper model
- **TTS (Text-to-Speech)**: Google TTS (gTTS)
- **Audio formats**: Supports webm, mp4, wav

---

## 🧪 Test Scenarios

### Scenario 1: Stress Management
**Query**: "I'm feeling very stressed about work"

**Expected Response**:
- Finds verses about Karma Yoga (action without attachment)
- Bhagavad Gita 2.47, 2.48
- Modern conversational tone

### Scenario 2: Mind Control
**Query**: "How do I control my mind?"

**Expected Response**:
- Chapter 6 verses about meditation
- Verses 6.26, 6.35, 6.34
- Practical advice from scriptures

### Scenario 3: Fear & Anxiety
**Query**: "I'm afraid of failure"

**Expected Response**:
- Verses about equanimity and surrender
- References to detachment from results
- Wisdom about fear

### Scenario 4: Purpose of Life
**Query**: "What is the meaning of life?"

**Expected Response**:
- Philosophical verses about dharma
- Soul and self-realization
- Multiple perspectives

---

## 🔧 Backend Logs

**View real-time logs:**
```bash
tail -f /tmp/backend.log
```

**What to look for:**
```
✅ Loaded 701 verses from Bhagavad Gita dataset
INFO: Application startup complete
```

---

## 🎨 Frontend Access

### Main Interface
**URL**: http://localhost:3000

**Features**:
- Text input for typing questions
- Voice recording button
- Response display
- Audio playback
- Language selector (EN/HI)

### Browser Requirements
- **Chrome/Edge**: Full support
- **Firefox**: Full support
- **Safari**: Works (may need mic permissions)

**Note**: HTTPS not required on localhost!

---

## 💡 Example Questions to Try

### Philosophical
- "What is dharma?"
- "What happens after death?"
- "What is the nature of the soul?"
- "How do I find enlightenment?"

### Practical
- "How do I deal with difficult people?"
- "What should I do when I'm confused?"
- "How can I improve my concentration?"
- "What is the right way to work?"

### Emotional
- "I feel angry all the time"
- "How do I overcome grief?"
- "I'm struggling with anxiety"
- "How do I find happiness?"

### Spiritual
- "What is meditation?"
- "How do I practice yoga?"
- "What is devotion (bhakti)?"
- "Tell me about Krishna's teachings"

---

## 🔍 Verifying It's Working

### Check 1: Dataset Loaded
```bash
curl http://localhost:8000/health
```
Should show: `"rag": true`

### Check 2: Search Quality
Ask: "Tell me about karma"
Should get: Verses specifically about karma yoga

### Check 3: Multiple Results
Each query returns **5 relevant verses** with similarity scores

### Check 4: Voice Pipeline
Record audio → Should transcribe → Get response → Play audio

---

## 📈 Performance

### Response Times
- **Text query**: 1-3 seconds
- **Voice query**: 4-7 seconds (includes ASR + TTS)
- **First query**: Slightly slower (model loading)

### Dataset Coverage
- **Total verses**: 701
- **Chapters**: All 18
- **Languages**: EN (primary), HI, SK (partial)

---

## ⚙️ Current Configuration

### LLM Mode
**Status**: Fallback templates (no API key)

**To enable Claude AI**:
1. Get API key from https://console.anthropic.com/
2. Add to `backend/.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```
3. Restart backend
4. Get intelligent, conversational responses!

**With Claude**: Custom responses for each question
**Without Claude**: Template responses (still works!)

---

## 🐛 Troubleshooting

### Backend Not Responding
```bash
# Check if running
lsof -ti:8000

# Restart
cd backend
source venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Not Loading
```bash
# Check if running
lsof -ti:3000

# Restart
cd frontend
npm run dev
```

### Microphone Not Working
- Check browser permissions (click lock icon in address bar)
- Allow microphone access
- Refresh page

### No Audio Output
- Check system volume
- Check browser audio permissions
- Verify gTTS is installed: `pip list | grep gtts`

### "No verses found"
- Check backend logs: `tail -f /tmp/backend.log`
- Verify: "✅ Loaded 701 verses" appears
- If not, rerun ingestion: `python3 scripts/ingest_bhagavad_gita_simple.py`

---

## 📱 Testing Checklist

- [ ] Backend health check passes
- [ ] Text query returns relevant verses
- [ ] Frontend loads at localhost:3000
- [ ] Can type question and get response
- [ ] Microphone permission granted
- [ ] Voice recording works
- [ ] Transcription appears
- [ ] Voice response plays
- [ ] Multiple questions work
- [ ] Different topics return different verses

---

## 🎯 Success Indicators

### You'll know it's working when:

1. **Backend logs show**:
   ```
   ✅ Loaded 701 verses from Bhagavad Gita dataset
   INFO: Application startup complete
   ```

2. **Health endpoint returns**:
   ```json
   {
     "status": "healthy",
     "components": {"rag": true, "asr": true, "tts": true}
   }
   ```

3. **Query returns 5 verses** with:
   - Chapter and verse numbers
   - Actual verse text
   - Scripture reference
   - Similarity scores

4. **Frontend shows**:
   - Clean interface
   - Working buttons
   - Response text
   - Audio controls

---

## 🚀 Next Steps

### To Enhance Further:

1. **Add Claude AI** (for intelligent responses)
   - Get API key
   - Add to .env
   - Restart backend

2. **Load More Scriptures**
   - Add Upanishads
   - Add other texts
   - Run ingestion

3. **Deploy to Cloud**
   - AWS/GCP/Azure
   - Get HTTPS (required for mic in production)
   - Scale as needed

---

## 📞 Quick Commands Reference

```bash
# Start Backend
cd backend && source venv/bin/activate && python3 -m uvicorn main:app --reload

# Start Frontend
cd frontend && npm run dev

# Test Backend
curl http://localhost:8000/health

# View Backend Logs
tail -f /tmp/backend.log

# View Frontend Logs
tail -f /tmp/frontend.log

# Stop Backend
lsof -ti:8000 | xargs kill

# Stop Frontend
lsof -ti:3000 | xargs kill
```

---

## 🎉 You're Live!

Your spiritual voice bot is running with:
- ✅ 701 Bhagavad Gita verses
- ✅ Semantic search
- ✅ Voice input/output
- ✅ Web interface
- ✅ REST API

**Open http://localhost:3000 and start asking questions!** 🕉️

---

**Need help?** Check logs or see troubleshooting section above.
