# Voice Bot Fix Guide - Conversational AI with Voice I/O

## What Was Fixed

### 1. **Missing gTTS Dependency** ✅
- **Problem**: `gtts` library was used in code but missing from `requirements.txt`
- **Fix**: Added `gtts==2.5.1` to requirements.txt
- **Impact**: Voice output will now work instead of returning error beeps

### 2. **Modern Conversational Tone** ✅
- **Problem**: Responses were formal and template-like ("Dear seeker...", "Om Shanti Shanti Shanti")
- **Fix**: Updated response templates to be casual and relatable:
  - **Before**: "Dear seeker, In response to your question..."
  - **After**: "Hey! I get it - stress can be overwhelming. Let me share some ancient wisdom..."
- **Features**:
  - Conversational intros that acknowledge the user's feelings
  - Modern language ("basically", "super relevant", "like mental gym training")
  - Friendly tone with emojis 🙏
  - Still references sacred texts but explains them in everyday language

### 3. **Enhanced Error Logging** ✅
- **Problem**: Silent failures made debugging impossible
- **Fix**: Added detailed logging to both ASR and TTS modules:
  - Import status with installation instructions
  - Detailed step-by-step processing logs
  - Audio byte sizes, conversion steps, and error traces
  - Full stack traces for exceptions

### 4. **Audio Format Handling** ✅
- **Status**: Existing code already handles format conversion properly
- **How it works**:
  - Frontend sends webm/mp4 from browser
  - Backend uses pydub to convert to proper format
  - Both ASR and TTS use standardized WAV format internally

---

## Installation Steps

### 1. Install Backend Dependencies

```bash
cd /Users/ankit1609/Downloads/Voice\ Bot\ POC/spiritual-voice-bot/backend

# Install all requirements including the new gtts package
pip install -r requirements.txt

# If you have a virtual environment (recommended):
python -m venv venv
source venv/bin/activate  # On Mac/Linux
# or
venv\Scripts\activate  # On Windows

pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd /Users/ankit1609/Downloads/Voice\ Bot\ POC/spiritual-voice-bot/frontend

npm install
# or
yarn install
```

### 3. Install System Dependencies (if needed)

For audio processing, you may need ffmpeg:

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from: https://ffmpeg.org/download.html

---

## Running the Application

### 1. Start Backend Server

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     gTTS library loaded successfully
INFO:     Whisper library loaded successfully
INFO:     All components initialized successfully!
```

**Check the logs carefully**:
- ✅ "gTTS library loaded successfully" = Voice output will work
- ❌ "Failed to import gTTS" = Need to install: `pip install gtts`
- ✅ "Whisper library loaded successfully" = Voice input will work
- ❌ "Failed to import Whisper" = Need to install: `pip install openai-whisper torch`

### 2. Start Frontend Server

```bash
cd frontend
npm run dev
# or
yarn dev
```

Frontend will run on: http://localhost:3000

---

## Testing Voice Features

### Test 1: Check API Health

Open browser to: http://localhost:8000/health

Expected response:
```json
{
  "status": "healthy",
  "components": {
    "rag": true,
    "asr": true,
    "tts": true
  }
}
```

### Test 2: Test Voice Output (TTS)

```bash
curl -X POST "http://localhost:8000/api/voice/synthesize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hey! This is a test of the modern voice output.", "language": "en"}'
```

- Should return audio/wav file
- If you get a 0.3 second beep, TTS is not working (check logs)

### Test 3: Test Text Query (Check Conversational Tone)

```bash
curl -X POST "http://localhost:8000/api/text/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I handle stress?", "language": "en"}'
```

Expected response style:
```
Hey! I get it - stress can be overwhelming. Let me share some ancient wisdom that might help.

There's this beautiful verse in Bhagavad Gita 2.47 that speaks to this:

"[scripture verse]"

Basically, focus on doing your best without obsessing over outcomes - that's where real peace comes from. This ancient wisdom is super relevant even today.

Hope this helps! 🙏
```

### Test 4: Test Voice Input + Voice Output (Full Flow)

1. Open http://localhost:3000 in your browser
2. **Grant microphone permission** when prompted
3. Click the "Start Recording" button
4. Speak your question: "How do I control my mind?"
5. Click "Stop Recording"
6. Watch for:
   - Status: "Transcribing audio..."
   - Status: "Getting response..."
   - Status: "Playing audio response..."
   - Response text appears in modern conversational tone
   - Audio plays automatically

---

## Example Queries to Test Conversational Tone

Try these to see the modern, friendly responses:

1. **"I'm feeling really stressed lately"**
   - Response starts with: "Hey! I get it - stress can be overwhelming..."

2. **"How can I control my mind?"**
   - Response starts with: "Hey! Controlling the mind - that's a universal struggle!..."

3. **"What should I do about my work duties?"**
   - Response starts with: "Hey! Great question! Let's see what the wisdom says about action and duty..."

4. **"I'm afraid of failure"**
   - Response starts with: "Hey! It's totally normal to feel fear..."

Compare this to the old style which was:
- "Dear seeker, In response to your question..."
- Very formal and ceremonial

---

## Troubleshooting

### Problem: Voice output returns beep sound

**Symptoms**: When testing TTS, you get a 0.3 second tone instead of speech

**Solution**:
1. Check backend logs for: "Failed to import gTTS"
2. Install gTTS: `pip install gtts`
3. Restart backend server
4. Verify in logs: "gTTS library loaded successfully"

### Problem: Voice input returns "[ASR disabled in lightweight mode]"

**Symptoms**: Transcription always returns placeholder text

**Solution**:
1. Check backend logs for: "Failed to import Whisper"
2. Install Whisper: `pip install openai-whisper torch`
3. First run downloads ~139MB Whisper base model (one-time)
4. Restart backend server
5. Verify in logs: "Whisper library loaded successfully"

### Problem: Microphone permission denied

**Symptoms**: "Microphone permission denied" error in browser

**Solution**:
- Chrome: Click lock icon in address bar → Allow microphone
- Firefox: Click microphone icon in address bar → Allow
- Safari: Safari menu → Settings → Websites → Microphone → Allow
- **Note**: HTTPS required in production (localhost works with HTTP)

### Problem: No audio output in browser

**Symptoms**: Response received but no sound plays

**Check**:
1. Browser console for errors (F12 → Console tab)
2. System volume is not muted
3. Response status shows "Playing audio response..."
4. Check browser's audio autoplay policy (may need user interaction first)

### Problem: Audio format errors

**Symptoms**: "Failed to convert audio" or "Unsupported audio format"

**Solution**:
1. Install ffmpeg (see Installation Steps section)
2. Verify: `ffmpeg -version`
3. Restart backend server

### Problem: Responses still sound formal

**Symptoms**: Still seeing "Dear seeker..." instead of "Hey!"

**Solution**:
- Backend code was updated, but you need to **restart the server**
- Kill the uvicorn process: `Ctrl+C`
- Start again: `python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000`
- Check that it reloads the updated `rag/pipeline.py`

---

## Sample Response Comparison

### OLD (Formal):
```
Dear seeker,

In response to your question, Bhagavad Gita 2.47 states:

"You have a right to perform your prescribed duties, but you are not entitled to the fruits of your actions."

This verse teaches us that we should focus on our duties without attachment to results, as this brings inner peace.

May you find peace and wisdom on your spiritual journey.

Om Shanti Shanti Shanti.
```

### NEW (Conversational):
```
Hey! I get it - stress can be overwhelming. Let me share some ancient wisdom that might help.

There's this beautiful verse in Bhagavad Gita 2.47 that speaks to this:

"You have a right to perform your prescribed duties, but you are not entitled to the fruits of your actions."

Basically, focus on doing your best without obsessing over outcomes - that's where real peace comes from. This ancient wisdom is super relevant even today.

Hope this helps! 🙏
```

---

## Architecture Overview

### Voice Input Flow:
1. **Browser** → Records audio (MediaRecorder API)
2. **Frontend** → Sends webm/mp4 to `/api/voice/transcribe`
3. **ASR (asr.py)** → Converts to WAV, runs Whisper model
4. **Transcription** → Returns text to frontend

### Voice Output Flow:
1. **Frontend** → Sends text to `/api/voice/synthesize`
2. **TTS (tts.py)** → Uses gTTS to generate MP3
3. **Conversion** → Converts MP3 to WAV
4. **Response** → Streams audio back to browser
5. **Browser** → Plays audio automatically

### Full Conversation Flow:
1. User speaks (voice input) → Transcribed by Whisper
2. Text query → RAG pipeline retrieves relevant scripture
3. Response generation → Modern conversational template
4. Text response → TTS converts to speech
5. Audio playback → User hears friendly voice response

---

## Current Capabilities

### Data Sources:
- **8 Bhagavad Gita verses** currently loaded in memory
- Topics covered: Karma Yoga, Mind Control, Equanimity, Liberation, Soul
- Both English and Sanskrit versions

### Languages Supported:
- **English** (en) - Full support for ASR, TTS, responses
- **Hindi** (hi) - Full support with Devanagari script

### Sample Verses Available:
1. Bhagavad Gita 2.47 - Karma Yoga (action without attachment)
2. Bhagavad Gita 6.35 - Mind Control through practice
3. Bhagavad Gita 2.48 - Equanimity in success/failure
4. Bhagavad Gita 18.66 - Surrender and liberation
5. Bhagavad Gita 2.20 - Eternal nature of the soul
6. Bhagavad Gita 2.14 - Dealing with pleasure and pain
7. Bhagavad Gita 4.7-8 - Divine incarnation for protection
8. Bhagavad Gita 9.22 - Divine care for devotees

---

## Next Steps for Full Production

### To expand the bot further:

1. **Add More Data Sources**:
   - Load full Bhagavad Gita (700 verses)
   - Add Upanishads, Vedas, other texts
   - Use Qdrant vector DB (already configured in docker-compose)

2. **Integrate Real LLM** (Optional):
   - Replace template-based responses with GPT-4/Claude
   - More nuanced, context-aware conversations
   - Better handling of complex questions

3. **Improve Voice Quality**:
   - Use Google Cloud TTS for better voices
   - Add voice customization (speed, pitch, gender)
   - Support more languages

4. **Add Conversation Memory**:
   - Track conversation history
   - Remember user preferences
   - Provide personalized guidance

5. **Deploy to Production**:
   - Set up HTTPS (required for microphone in production)
   - Configure CORS properly
   - Add authentication if needed

---

## Quick Start (TL;DR)

```bash
# 1. Install backend dependencies
cd backend
pip install -r requirements.txt

# 2. Start backend
python -m uvicorn main:app --reload --port 8000

# 3. In a new terminal, install frontend dependencies
cd frontend
npm install

# 4. Start frontend
npm run dev

# 5. Open browser to http://localhost:3000
# 6. Grant microphone permission
# 7. Test voice input/output!
```

---

## Support

**Backend logs**: Watch the terminal running uvicorn for detailed debug info
**Frontend logs**: Open browser DevTools (F12) → Console tab
**API docs**: http://localhost:8000/docs (Interactive Swagger UI)

All voice components now have extensive logging to help debug issues!
