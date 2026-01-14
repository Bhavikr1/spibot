# Manual Setup Guide (Without Docker)

## Quick Fix for Docker Issues

If Docker isn't running or you prefer not to use it, follow this guide to run the application manually.

---

## Prerequisites

Make sure you have:
- Python 3.10 or higher
- Node.js 18 or higher
- ffmpeg (for audio processing)

Check versions:
```bash
python3 --version  # Should be 3.10+
node --version     # Should be 18+
ffmpeg -version    # Should show ffmpeg info
```

---

## Step 1: Install System Dependencies

### For Mac (using Homebrew):
```bash
# If you don't have Homebrew:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required packages
brew install python@3.10 node ffmpeg
```

### For Ubuntu/Debian Linux:
```bash
sudo apt update
sudo apt install python3.10 python3-pip nodejs npm ffmpeg
```

### For Windows:
1. Install Python from https://www.python.org/downloads/
2. Install Node.js from https://nodejs.org/
3. Install ffmpeg from https://ffmpeg.org/download.html

---

## Step 2: Setup Backend

Open a terminal and run:

```bash
# Navigate to project
cd /Users/ankit1609/Downloads/"Voice Bot POC"/spiritual-voice-bot

# Go to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Mac/Linux
# OR
venv\Scripts\activate     # On Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies (this may take 5-10 minutes)
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env if needed (optional for POC)
# You can use defaults for testing
```

---

## Step 3: Start Backend Server

In the same terminal (with venv activated):

```bash
# Make sure you're in backend directory
cd /Users/ankit1609/Downloads/"Voice Bot POC"/spiritual-voice-bot/backend

# Activate virtual environment if not already active
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Keep this terminal open!** The backend is now running.

---

## Step 4: Setup Frontend

Open a **NEW** terminal (keep backend running):

```bash
# Navigate to frontend directory
cd /Users/ankit1609/Downloads/"Voice Bot POC"/spiritual-voice-bot/frontend

# Install dependencies (this may take 3-5 minutes)
npm install

# Create environment file (optional)
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

---

## Step 5: Start Frontend Server

In the same terminal:

```bash
# Make sure you're in frontend directory
cd /Users/ankit1609/Downloads/"Voice Bot POC"/spiritual-voice-bot/frontend

# Start development server
npm run dev
```

You should see:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

---

## Step 6: Open Application

Open your web browser and go to:
```
http://localhost:3000
```

You should see the Spiritual Voice Bot interface! 🎉

---

## Testing the Application

### 1. Test Backend API

Open a third terminal:

```bash
# Test health endpoint
curl http://localhost:8000/health

# You should see:
# {"status":"healthy","components":{...}}
```

### 2. Test Text Query

In the web interface:
1. Type: "What does the Bhagavad Gita say about the mind?"
2. Press Enter
3. You should see a response with scripture citations

### 3. Test Voice Query

1. Click the microphone button 🎤
2. Allow browser to access microphone
3. Speak clearly: "What is Karma?"
4. Click microphone again to stop
5. Wait for processing (3-5 seconds)
6. Listen to the audio response

---

## Troubleshooting

### Backend Issues

**Error: "No module named 'fastapi'"**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Error: "Port 8000 already in use"**
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --reload --port 8001
```

**Error: "Cannot import whisper"**
```bash
pip install openai-whisper
```

### Frontend Issues

**Error: "Command not found: npm"**
- Install Node.js from https://nodejs.org/

**Error: "Port 3000 already in use"**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different port
npm run dev -- -p 3001
```

**Error: "Cannot connect to backend"**
- Make sure backend is running (check terminal)
- Check backend URL in browser: http://localhost:8000/health
- Update .env.local if using different port

### Voice Issues

**Microphone not working:**
1. Grant browser permission when prompted
2. Check System Preferences → Security & Privacy → Microphone
3. Try different browser (Chrome recommended)
4. Check microphone in system settings

**No audio output:**
1. Check system volume
2. Check browser audio settings
3. Try different browser
4. Check Console for errors (F12 → Console tab)

---

## Quick Commands Reference

### Start Everything (2 Terminals)

**Terminal 1 (Backend):**
```bash
cd /Users/ankit1609/Downloads/"Voice Bot POC"/spiritual-voice-bot/backend
source venv/bin/activate
uvicorn main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd /Users/ankit1609/Downloads/"Voice Bot POC"/spiritual-voice-bot/frontend
npm run dev
```

### Stop Everything

Press `Ctrl+C` in both terminals

---

## Performance Tips

### Faster Response Times

1. **Use GPU (if available):**
   ```bash
   # In backend/.env
   LLM_DEVICE=cuda
   ```

2. **Use smaller models:**
   ```bash
   # In backend/.env
   ASR_MODEL=openai/whisper-base  # Instead of large
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   ```

3. **Reduce model loading time:**
   - Models are loaded on first request
   - Subsequent requests are faster
   - Keep servers running for best performance

---

## Verifying Setup

### Check Backend

```bash
# Health check
curl http://localhost:8000/health

# Test API docs
open http://localhost:8000/docs
```

### Check Frontend

```bash
# Open in browser
open http://localhost:3000
```

### Run Full Tests

```bash
cd backend
source venv/bin/activate
python test_api.py
```

Expected output:
```
Testing health endpoint... ✓
Testing text query endpoint... ✓
Testing scripture search endpoint... ✓
Testing Hindi query... ✓
All tests completed!
```

---

## Common Questions

**Q: How long does setup take?**
A: First time: 10-15 minutes (downloading models). After that: 30 seconds to start.

**Q: Do I need to run setup every time?**
A: No! Once setup is done, just start the servers (Step 3 and 5).

**Q: Can I use this offline?**
A: Yes, after initial model downloads. Everything runs locally.

**Q: How much disk space is needed?**
A: ~2GB for models and dependencies.

**Q: Why is the first query slow?**
A: Models are loaded on first use. Subsequent queries are faster.

---

## Next Steps

Once everything is running:

1. ✅ Test with sample questions
2. ✅ Try voice features
3. ✅ Switch between English and Hindi
4. ✅ Review scripture citations
5. ✅ Check API documentation at http://localhost:8000/docs

---

## Need More Help?

- Check logs in terminal for error messages
- Review QUICKSTART.md for detailed info
- Check ARCHITECTURE.md for technical details
- Read GETTING_STARTED.md for usage tips

---

**You're all set! Enjoy using the Spiritual Voice Bot!** 🙏

**Om Shanti Shanti Shanti**
