# LLM Integration Guide - Intelligent Conversational AI

## What Changed

Your bot has been upgraded from **template-based responses** to **LLM-powered conversational AI**! 🎉

### Before (Template-Based):
- Pre-defined rule-based responses
- Only worked for specific keywords
- Same answer every time
- Limited to 8-9 question patterns

### After (LLM-Powered):
- **Intelligent understanding** of any question
- **Custom responses** based on your data (Bhagavad Gita verses)
- **Natural conversations** with context awareness
- **Infinite question variations** - ask anything about the scriptures!

---

## How It Works Now

```
User Question
    ↓
RAG Pipeline retrieves relevant scriptures (same as before)
    ↓
LLM (Claude) generates custom response using:
    - Retrieved scripture verses
    - Modern conversational tone
    - Understanding of the specific question
    ↓
Personalized, intelligent answer
```

---

## Setup Instructions

### Step 1: Get Your Anthropic API Key

1. Go to: **https://console.anthropic.com/**
2. Sign up / Log in
3. Click **"Get API Keys"** in the sidebar
4. Click **"Create Key"**
5. Copy your API key (starts with `sk-ant-...`)

**Pricing** (as of 2026):
- Claude Sonnet: ~$0.003 per request (very affordable!)
- Free tier: $5 credit for new accounts
- For this spiritual bot: ~300-500 conversations per dollar

### Step 2: Configure Your API Key

#### Option A: Using .env file (Recommended)

1. Navigate to the backend directory:
```bash
cd /Users/ankit1609/Downloads/Voice\ Bot\ POC/spiritual-voice-bot/backend
```

2. Copy the example file:
```bash
cp .env.example .env
```

3. Edit the .env file:
```bash
nano .env
# or use any text editor
```

4. Replace `your_anthropic_api_key_here` with your actual key:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

5. Save and close the file

#### Option B: Using Environment Variable

```bash
# Mac/Linux
export ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxxxxxxxxxxxx"

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxxxxxxxxxxxx"

# Windows (CMD)
set ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxx
```

### Step 3: Install New Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `anthropic==0.39.0` - The Claude SDK
- All other dependencies (including `gtts` from before)

### Step 4: Start the Backend

```bash
python -m uvicorn main:app --reload --port 8000
```

**Look for these success messages:**
```
INFO:     Anthropic SDK loaded successfully
INFO:     LLM Service initialized successfully with Claude
INFO:     All components initialized successfully!
```

**If you see this warning:**
```
WARNING:  LLM Service not available - will use fallback templates. Set ANTHROPIC_API_KEY to enable.
```
→ Your API key is not set correctly. Go back to Step 2.

### Step 5: Test It!

#### Test via Command Line:

```bash
curl -X POST "http://localhost:8000/api/text/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Why do I feel anxious all the time?", "language": "en"}'
```

#### Test via Frontend:

1. Start frontend: `cd frontend && npm run dev`
2. Open: http://localhost:3000
3. Ask: "Why do I feel anxious all the time?"

**Expected Response** (will be unique each time!):
```
Hey! I totally understand - anxiety can feel overwhelming. The Bhagavad Gita
has some wisdom that might help.

In Bhagavad Gita 2.47, Krishna tells us:

"You have a right to perform your prescribed duties, but you are not entitled
to the fruits of your actions."

What this basically means is that we create a lot of our own anxiety by being
too attached to outcomes. When you focus on doing your best in the moment,
without obsessing over how things will turn out, that's when you find real peace.

It's like showing up for a game - play your heart out, but don't torture yourself
about the scoreboard. This ancient wisdom is super relevant to modern stress!

Hope this helps! 🙏
```

---

## What Makes This Different

### 1. **Understands Context**

**Before:**
- Q: "I'm stressed" → Always the same response
- Q: "I'm anxious" → Different template response

**After with LLM:**
- Q: "I'm stressed about my job interview tomorrow"
  → Custom response about performance without attachment
- Q: "I'm anxious because my relationship is struggling"
  → Custom response about equanimity and compassion

### 2. **Handles Complex Questions**

**Before:**
- Q: "What if I fail at my duties?" → Generic fallback

**After with LLM:**
- Understands the nuance
- Combines multiple scripture teachings
- Addresses the specific concern about failure

### 3. **Natural Follow-up Conversations**

**Before:**
- Each question treated independently
- No conversation memory

**After with LLM:**
- Can reference previous questions (coming soon!)
- Builds on earlier context
- Feels like talking to a knowledgeable friend

### 4. **Adapts to User's Language Style**

**Before:**
- Fixed formal tone

**After with LLM:**
- Matches your communication style
- Can be casual or serious
- Adjusts depth based on question complexity

---

## Example Conversations

### Example 1: Career Stress

**User:** "I'm scared I won't succeed in my career"

**LLM Response:**
```
Hey! Career anxiety is so common - you're definitely not alone in this. Let me share
some timeless wisdom that might shift your perspective.

The Bhagavad Gita 2.47 talks about this exact thing:

"You have a right to perform your prescribed duties, but you are not entitled to the
fruits of your actions. Never consider yourself the cause of the results of your
activities, and never be attached to not doing your duty."

Here's the game-changer: success isn't about the destination, it's about showing up
fully for the journey. When you focus on doing excellent work for its own sake, rather
than constantly worrying about "making it," you actually perform better AND feel more
at peace.

Think of it like this - the best athletes don't obsess about winning during the game.
They're present, focused, giving their all to each moment. That's where real success lives.

The fear of not succeeding often creates more obstacles than actual lack of ability.
So focus on being excellent today, and let tomorrow take care of itself.

You've got this! 🙏
```

### Example 2: Relationship Issues

**User:** "How do I deal with someone who constantly criticizes me?"

**LLM Response:**
```
Hey! That's really tough - constant criticism can wear anyone down. The ancient
teachings have some surprisingly practical advice for this.

Bhagavad Gita 2.14 addresses this beautifully:

"The contact between the senses and sense objects gives rise to feelings of heat and
cold, pleasure and pain. These are temporary and fleeting; they come and go. Learn to
tolerate them."

What this means in your situation: That person's criticism is like weather - it comes
and goes, but it doesn't define who you are. The key is developing that inner stability
where you can hear feedback without letting it shake your core.

Here's the practical part: Some criticism might actually be useful (even if delivered
poorly), and some is just noise. When you're not emotionally reactive, you can sort the
wheat from the chaff. Take what helps you grow, let the rest roll off.

Also, remember - people who constantly criticize are often dealing with their own stuff.
Doesn't make it okay, but it helps you not take it so personally.

Stay grounded in who you are. 🙏
```

---

## Technical Details

### Files Modified:

1. **[requirements.txt](backend/requirements.txt)**
   - Added: `anthropic==0.39.0`

2. **[config.py](backend/config.py)**
   - Added: `ANTHROPIC_API_KEY` setting
   - Updated: System prompt for modern conversational tone

3. **[llm/service.py](backend/llm/service.py)** (NEW)
   - Claude API integration
   - Context building from RAG results
   - Fallback handling when API key missing

4. **[rag/pipeline.py](backend/rag/pipeline.py)**
   - Replaced template-based `_generate_response()`
   - Now calls LLM service with retrieved context
   - Passes scripture verses to Claude for intelligent responses

5. **[main.py](backend/main.py)**
   - Added LLM service initialization
   - Logs whether LLM is available

### Models Used:

- **Claude 3.5 Sonnet** (latest model as of 2026)
  - Model ID: `claude-3-5-sonnet-20241022`
  - Max tokens: 1024 (can be adjusted)
  - Temperature: 0.7 (balanced creativity)

### Cost Estimation:

**Per Conversation:**
- Input: ~800 tokens (system prompt + scriptures + query)
- Output: ~400 tokens (response)
- Cost: ~$0.003-0.005 per conversation

**For 1000 conversations:** ~$3-5

---

## Troubleshooting

### Issue 1: "LLM Service not available"

**Problem:** API key not found

**Solutions:**
1. Check `.env` file exists in backend folder
2. Verify key starts with `sk-ant-`
3. No quotes around the key in .env file
4. Restart the backend server after adding key

### Issue 2: "API key invalid" error

**Problem:** Wrong or expired API key

**Solutions:**
1. Generate new key at console.anthropic.com
2. Check for extra spaces in the key
3. Verify your account is active

### Issue 3: "Rate limit exceeded"

**Problem:** Too many requests

**Solutions:**
1. Free tier: 50 requests per day
2. Upgrade account for higher limits
3. Add rate limiting in your app (for production)

### Issue 4: Still getting template responses

**Problem:** API key set but not being used

**Check:**
1. Backend logs show: "LLM Service initialized successfully"
2. No warnings about fallback templates
3. Restart backend if you just added the key
4. Check .env file is in correct directory

### Issue 5: Responses are too long/short

**Solution:** Adjust max_tokens in [llm/service.py](backend/llm/service.py:92)

```python
# Current:
max_tokens=1024

# For shorter responses:
max_tokens=512

# For longer responses:
max_tokens=2048
```

---

## Without API Key (Fallback Mode)

If you don't set an API key, the bot still works but uses **enhanced templates**:

```
Hey! Regarding your question, Bhagavad Gita 2.47 says:

"[scripture verse]"

This verse relates to your question. For more detailed explanations,
please set up your ANTHROPIC_API_KEY.
```

- Still better than before (modern tone)
- Still references scriptures
- Just not custom-generated

---

## Security Best Practices

### DO:
✅ Use `.env` file (never commit to git)
✅ Add `.env` to `.gitignore`
✅ Use environment variables in production
✅ Rotate API keys periodically

### DON'T:
❌ Commit API keys to GitHub
❌ Share keys publicly
❌ Use same key for dev/prod
❌ Hardcode keys in source files

---

## Monitoring Usage

### Check Your Usage:

1. Visit: https://console.anthropic.com/settings/usage
2. See real-time costs and request counts
3. Set up billing alerts

### In Your App Logs:

```
INFO: Generating LLM response for query: Why do I feel anxious...
INFO: Calling Claude API with 1 messages...
INFO: Generated response length: 847 chars
```

---

## Next Steps

### 1. **Add More Scripture Data**
   - Currently: 8 Bhagavad Gita verses
   - Expand: Full Bhagavad Gita (700 verses)
   - Add: Upanishads, Vedas, other texts

### 2. **Enable Conversation Memory**
   - Track previous questions
   - Build conversation context
   - More personalized guidance

### 3. **Add Voice Personality**
   - Fine-tune system prompt
   - Create different "guru personas"
   - Multilingual improvements

### 4. **Production Deployment**
   - Add rate limiting
   - Implement caching
   - Monitor costs
   - Set up error tracking

---

## Cost Optimization Tips

### 1. **Cache Common Questions**
```python
# Store frequently asked questions and responses
# Only call LLM for new/unique questions
```

### 2. **Reduce Context Size**
```python
# Only send top 3 scriptures instead of 5
RETRIEVAL_TOP_K = 3
```

### 3. **Use Shorter System Prompt**
- Current: ~200 tokens
- Can optimize to ~100 tokens

### 4. **Batch Process**
- For analytics, batch multiple questions
- Use asynchronous processing

---

## Comparison: Template vs LLM

| Feature | Template-Based | LLM-Powered |
|---------|---------------|-------------|
| **Cost** | Free | ~$0.003/query |
| **Response Quality** | Basic | Excellent |
| **Flexibility** | Limited patterns | Any question |
| **Customization** | Hard-coded | Dynamic |
| **Context Awareness** | None | Full |
| **Setup Complexity** | Simple | API key needed |
| **Scalability** | Easy | API limits |
| **Offline Mode** | Yes | No (needs API) |

---

## API Key FAQ

**Q: Do I need a credit card?**
A: Yes, but new accounts get $5 free credit.

**Q: Can I use OpenAI instead?**
A: Yes! The code is structured to support multiple providers. Would need to modify `llm/service.py`.

**Q: What about local LLMs (free)?**
A: Possible with Ollama! Trade-off: slower, needs GPU, less capable than Claude.

**Q: Is my data private?**
A: Anthropic doesn't train on your API data. See: https://www.anthropic.com/privacy

**Q: Can I switch to a cheaper model?**
A: Yes, use `claude-3-haiku` instead of `claude-3-5-sonnet` in [service.py](backend/llm/service.py:83)

---

## Testing Examples

### Test 1: General Question
```bash
curl -X POST "http://localhost:8000/api/text/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the meaning of life?", "language": "en"}'
```

### Test 2: Specific Emotion
```bash
curl -X POST "http://localhost:8000/api/text/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "I am feeling lost and dont know my purpose", "language": "en"}'
```

### Test 3: Hindi
```bash
curl -X POST "http://localhost:8000/api/text/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "मैं तनाव में हूं", "language": "hi"}'
```

### Test 4: Complex Scenario
```bash
curl -X POST "http://localhost:8000/api/text/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "My boss is toxic and I want to quit but I need the money. What should I do?", "language": "en"}'
```

---

## Summary

🎉 **You now have a truly intelligent spiritual companion!**

**What you gained:**
- ✅ LLM-powered responses (Claude 3.5 Sonnet)
- ✅ Unlimited question variations
- ✅ Custom answers for each user
- ✅ Modern conversational tone
- ✅ Voice input still works
- ✅ Voice output still works
- ✅ All powered by your scripture data

**To activate:**
1. Get API key from console.anthropic.com
2. Add to .env file
3. Restart backend
4. Enjoy intelligent conversations!

**Need help?** Check the troubleshooting section or review the logs for detailed error messages.
