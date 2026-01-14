# Getting Started with Spiritual Voice Bot

## For Non-Technical Users

Welcome! This guide will help you get the Spiritual Voice Bot running on your computer in simple steps.

---

## What You'll Need

Before starting, make sure you have:

- ✅ A computer (Mac, Windows, or Linux)
- ✅ Internet connection (for downloading)
- ✅ Microphone (for voice features)
- ✅ Speakers or headphones (to hear responses)
- ✅ About 2GB of free disk space

---

## Installation Steps

### Step 1: Download the Code

1. Download the project folder to your computer
2. Unzip if it's in a ZIP file
3. Remember where you saved it!

### Step 2: Install Prerequisites

#### For Mac Users:

1. **Install Homebrew** (if not already installed):
   - Open Terminal (search for "Terminal" in Spotlight)
   - Copy and paste this command:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   - Press Enter and follow instructions

2. **Install Python and Node.js**:
   ```bash
   brew install python@3.10 node
   ```

3. **Install ffmpeg** (for audio):
   ```bash
   brew install ffmpeg
   ```

#### For Windows Users:

1. **Install Python**:
   - Go to https://www.python.org/downloads/
   - Download Python 3.10 or later
   - Run installer, CHECK "Add Python to PATH"

2. **Install Node.js**:
   - Go to https://nodejs.org/
   - Download LTS version
   - Run installer

3. **Install ffmpeg**:
   - Go to https://ffmpeg.org/download.html
   - Follow Windows installation guide

### Step 3: Run the Setup

1. **Open Terminal/Command Prompt**:
   - Mac: Open Terminal app
   - Windows: Search for "Command Prompt" or "PowerShell"

2. **Navigate to the project folder**:
   ```bash
   cd path/to/spiritual-voice-bot
   ```
   (Replace `path/to/spiritual-voice-bot` with actual path)

3. **Run setup**:
   - Mac/Linux:
   ```bash
   ./setup.sh
   ```
   - Windows:
   ```bash
   bash setup.sh
   ```

4. **Wait for setup to complete** (may take 5-10 minutes)

---

## Starting the Application

### Easy Way (Recommended):

1. **Run the start script**:
   - Mac/Linux:
   ```bash
   ./start.sh
   ```
   - Windows:
   ```bash
   bash start.sh
   ```

2. **Wait for services to start** (30-60 seconds)

3. **Open your web browser** and go to:
   ```
   http://localhost:3000
   ```

4. **You should see the Spiritual Voice Bot interface!** 🎉

---

## Using the Application

### Text Queries

1. **Type your question** in the text box at the bottom
2. **Press Enter** or click the Send button
3. **Read the response** with scripture citations

Example questions:
- "What does the Bhagavad Gita say about duty?"
- "How can I control my mind?"
- "What is Karma?"

### Voice Queries

1. **Click the microphone button** (🎤)
2. **Speak your question** clearly
3. **Click the microphone again** to stop recording
4. **Wait** for the response
5. **Listen** to the audio answer

### Switching Languages

- Click the **language dropdown** in the top right
- Choose **English** or **हिंदी (Hindi)**

---

## Troubleshooting

### "Cannot connect to server"

**Solution**:
1. Check if backend is running:
   - Open http://localhost:8000/health
   - Should show: `{"status": "healthy"}`
2. If not, restart the application

### "Microphone not working"

**Solution**:
1. Grant browser permission when asked
2. Check system microphone settings
3. Try a different browser (Chrome works best)

### "Application won't start"

**Solution**:
1. Check Python and Node.js are installed:
   ```bash
   python --version  # Should show 3.10+
   node --version    # Should show 18+
   ```
2. Re-run setup: `./setup.sh`
3. Check error messages in terminal

### "Models downloading slowly"

**Solution**:
- Be patient! First-time setup downloads AI models (~1-2GB)
- This only happens once
- Ensure stable internet connection

---

## Stopping the Application

### If using start.sh:

Press `Ctrl+C` in the terminal window

### If using Docker:

```bash
docker-compose down
```

---

## Tips for Best Results

### 1. Ask Clear Questions
✅ Good: "What does Krishna say about the mind in Bhagavad Gita?"
❌ Unclear: "mind stuff"

### 2. Use Proper Microphone
- Speak clearly and at normal pace
- Reduce background noise
- Use a good quality microphone if possible

### 3. Check Citations
- Always review scripture references
- Verify important spiritual guidance
- Cross-reference with original texts

### 4. Be Patient
- First query might take longer (loading models)
- Voice queries take 3-5 seconds
- Text queries are faster (1-2 seconds)

---

## Common Questions

### Q: Is internet required?

**A**: Yes, for initial setup to download models. After setup, you can run it offline (local queries only).

### Q: Which browsers work best?

**A**: Chrome and Safari work best. Firefox and Edge also work. Internet Explorer is not supported.

### Q: Can I use it on my phone?

**A**: Not yet! Mobile apps are planned for future. For now, you can access via mobile browser (limited features).

### Q: How accurate are the responses?

**A**: The POC uses sample data. Responses are based on authentic Bhagavad Gita verses but generated by AI. Always verify important spiritual guidance with qualified teachers.

### Q: What languages are supported?

**A**: Currently English and Hindi. Sanskrit text is displayed. More languages coming in future updates.

### Q: Is my data private?

**A**: Yes! Everything runs on your computer. No data is sent to external servers (except when using voice features which may use cloud APIs).

---

## Getting Help

### If you're stuck:

1. **Check the QUICKSTART.md file** - More detailed instructions
2. **Look at error messages** - They often tell you what's wrong
3. **Try the API tests**:
   ```bash
   cd backend
   python test_api.py
   ```
4. **Ask for help** - Contact your technical team

### Useful Links:

- Project README: [README.md](README.md)
- Detailed Guide: [QUICKSTART.md](QUICKSTART.md)
- Technical Docs: [ARCHITECTURE.md](ARCHITECTURE.md)
- API Docs: http://localhost:8000/docs (when running)

---

## Example Session

Here's what a typical session looks like:

1. **Start application**: `./start.sh`
2. **Wait**: "Starting services..." (30 seconds)
3. **Open browser**: Go to http://localhost:3000
4. **See welcome screen**: "Welcome, Seeker"
5. **Click language**: Choose English or Hindi
6. **Ask question**: "What is dharma?"
7. **Get response**: Answer + Bhagavad Gita citation
8. **Try voice**: Click mic, speak "Tell me about karma"
9. **Listen**: Audio response plays automatically
10. **Continue**: Ask more questions!
11. **Done**: Close browser, press Ctrl+C in terminal

---

## Visual Guide

### Main Interface:

```
┌─────────────────────────────────────────────────┐
│  📖 Spiritual Voice Bot              [En ▼]     │
├─────────────────────────────────────────────────┤
│                                                  │
│     Welcome, Seeker                              │
│                                                  │
│     Ask me anything about                        │
│     Sanatan Dharma scriptures                    │
│                                                  │
├─────────────────────────────────────────────────┤
│  [🎤]  [Type your question here...      ] [→]   │
└─────────────────────────────────────────────────┘
```

### After Asking:

```
┌─────────────────────────────────────────────────┐
│                                                  │
│  You: What is Karma Yoga?                   ◄── │
│                                                  │
│  ──► According to Bhagavad Gita 2.47...         │
│      [See Citation: Bhagavad Gita 2.47]         │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## Next Steps

Once you're comfortable with the basics:

1. **Explore different topics**: Try asking about mind control, duty, soul, liberation
2. **Test voice features**: Practice with clear pronunciation
3. **Read citations**: Learn from the original scripture references
4. **Switch languages**: Try asking questions in Hindi
5. **Review documentation**: Check out technical docs for advanced features

---

## Safety & Disclaimers

⚠️ **Important Notes**:

1. **Not a Replacement for Guru**: This AI is a learning tool, not a spiritual teacher
2. **Verify Important Decisions**: Always consult qualified teachers for serious spiritual questions
3. **Mental Health**: For mental health concerns, contact professional counselors
4. **Scripture Accuracy**: While we strive for accuracy, always cross-reference important verses
5. **POC Limitations**: This is a proof of concept with sample data

---

## Feedback Welcome!

We'd love to hear about your experience:

- What works well?
- What's confusing?
- What features would you like?
- Any bugs or errors?

Share your feedback with the development team!

---

**May your spiritual journey be filled with wisdom and peace!**

**Om Shanti Shanti Shanti** 🙏

---

*Last Updated: January 13, 2026*
