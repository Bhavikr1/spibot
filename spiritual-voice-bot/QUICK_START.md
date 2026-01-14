# Quick Start - Intelligent Spiritual Voice Bot

## 🚀 Get Up and Running in 5 Minutes

### Step 1: Install Dependencies (2 minutes)

```bash
# Navigate to backend
cd backend

# Install Python packages (including new LLM support)
pip install -r requirements.txt

# Navigate to frontend
cd ../frontend

# Install Node packages
npm install
```

### Step 2: Get Your Anthropic API Key (2 minutes)

1. Visit: **https://console.anthropic.com/**
2. Sign up (get $5 free credit!)
3. Click "Get API Keys"
4. Create a new key
5. Copy it (starts with `sk-ant-...`)

### Step 3: Configure API Key (30 seconds)

```bash
cd backend

# Copy example config
cp .env.example .env

# Edit the file and paste your API key
nano .env
# or use any text editor
```

Replace this line:
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

With your actual key:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
```

Save and close!

### Step 4: Start the Application (30 seconds)

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

Wait for:
```
✓ gTTS library loaded successfully
✓ Whisper library loaded successfully
✓ Anthropic SDK loaded successfully
✓ LLM Service initialized successfully with Claude
✓ All components initialized successfully!
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Step 5: Test It! (1 minute)

1. Open: **http://localhost:3000**
2. Grant microphone permission
3. Click "Start Recording"
4. Ask: **"Why do I feel stressed all the time?"**
5. Get an intelligent, personalized answer! 🎉

---

## What Makes This Special?

### Before (Template):
```
Dear seeker,

In response to your question, Bhagavad Gita 2.47 states:
[verse]

This verse teaches us that we should focus on our duties...

Om Shanti Shanti Shanti.
```

### After (LLM-Powered):
```
Hey! I totally get it - stress is exhausting. Let me share
some ancient wisdom that's super relevant today.

The Bhagavad Gita 2.47 says:
[verse]

What this basically means is: focus on doing your best without
obsessing over outcomes. That's where real peace comes from.
Think of it like this - you can control your effort, not the
results. When you let go of that attachment to specific outcomes,
the anxiety naturally fades.

This 5000-year-old wisdom is honestly perfect for modern life!

Hope this helps! 🙏
```

---

## ✨ Features

✅ **Voice Input** - Speak your questions naturally
✅ **Voice Output** - Hear responses in natural voice
✅ **Intelligent Answers** - LLM understands context and nuance
✅ **Scripture-Grounded** - Always references Bhagavad Gita
✅ **Modern Tone** - Friendly, relatable, not preachy
✅ **Bilingual** - English and Hindi support
✅ **Custom Responses** - Every answer is unique to your question

---

## Troubleshooting

### "LLM Service not available"
→ API key not set. Check your `.env` file and restart backend.

### "Microphone permission denied"
→ Click the lock icon in your browser address bar and allow microphone.

### "Import error: anthropic"
→ Run `pip install anthropic` in the backend folder.

### Still getting template responses?
→ Check backend logs. Look for "LLM Service initialized successfully"

---

## Cost

- ~$0.003 per conversation
- Free $5 credit = ~1,500 conversations
- Very affordable for personal use!

---

## Next Steps

📖 Read the full guide: **[LLM_INTEGRATION_GUIDE.md](LLM_INTEGRATION_GUIDE.md)**
📖 Voice setup details: **[VOICE_FIX_GUIDE.md](VOICE_FIX_GUIDE.md)**

---

## Need Help?

**Check the logs:**
- Backend: Terminal running uvicorn
- Frontend: Browser DevTools (F12 → Console)
- API docs: http://localhost:8000/docs

**Common Issues:**
1. Port already in use? Change port: `--port 8001`
2. Module not found? Check you're in correct directory
3. API errors? Verify API key is valid at console.anthropic.com

---

## Architecture

```
User Voice → Whisper ASR → Text Query
                              ↓
                         RAG Pipeline
                    (finds relevant scriptures)
                              ↓
                         Claude LLM
                  (generates custom response)
                              ↓
                      gTTS → Voice Output
```

Enjoy your intelligent spiritual companion! 🙏✨
