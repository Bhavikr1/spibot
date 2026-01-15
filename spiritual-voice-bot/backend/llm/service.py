"""
LLM Service for conversational response generation using Google Gemini
"""
import logging
from typing import List, Dict, Optional
from config import settings
from llm.formatter import get_formatter, ResponseFormatter

logger = logging.getLogger(__name__)

# Try to import Google Generative AI SDK
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
    logger.info("Google Generative AI SDK loaded successfully")
except Exception as e:
    genai = None
    GEMINI_AVAILABLE = False
    logger.error(f"Failed to import Google Generative AI SDK: {str(e)}. Install with: pip install google-generativeai")


class LLMService:
    """
    LLM service for generating conversational responses using Gemini
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize LLM service

        Args:
            api_key: Gemini API key (if not provided, uses env variable)
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = None
        self.available = False
        self.formatter = None

        if not GEMINI_AVAILABLE:
            logger.error("Google Generative AI SDK not available - install with: pip install google-generativeai")
            return

        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set - LLM responses will use fallback templates")
            return

        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            self.available = True

            # Initialize formatter
            self.formatter = get_formatter(self.api_key)

            logger.info("LLM service initialized with Gemini")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {str(e)}")

    async def generate_response(
        self,
        query: str,
        context_docs: List[Dict],
        language: str = "en",
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate conversational response using Gemini with RAG context

        Args:
            query: User's question
            context_docs: Retrieved scripture documents with metadata
            language: Language code (en or hi)
            conversation_history: Optional chat history for context

        Returns:
            Generated response text
        """
        if not self.available or not self.model:
            logger.error("LLM service not available - using fallback")
            return self._generate_fallback_response(query, context_docs, language)

        try:
            logger.info(f"Generating LLM response for query: {query[:100]}...")

            # Build context from retrieved documents
            context = self._build_context(context_docs)

            # Build the complete prompt with system instructions
            prompt = self._build_prompt(query, context, language, conversation_history)

            logger.info(f"Calling Gemini API...")

            # Call Gemini API with updated temperature for more conversational responses
            response = await self.model.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.8,  # Increased for more natural conversation
                    max_output_tokens=1024,
                    top_p=0.9,
                )
            )

            # Extract response text
            response_text = response.text

            logger.info(f"Generated response length: {len(response_text)} chars")

            # Format response for better readability
            if self.formatter and self.formatter.available:
                logger.info("Formatting response for better readability...")
                response_text = await self.formatter.format_response(response_text)

            return response_text

        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}", exc_info=True)
            return self._generate_fallback_response(query, context_docs, language)

    async def generate_response_stream(
        self,
        query: str,
        context_docs: List[Dict],
        language: str = "en",
        conversation_history: Optional[List[Dict]] = None
    ):
        """
        Generate streaming conversational response using Gemini with RAG context

        Args:
            query: User's question
            context_docs: Retrieved scripture documents with metadata
            language: Language code (en or hi)
            conversation_history: Optional chat history for context

        Yields:
            Chunks of generated response text
        """
        if not self.available or not self.model:
            logger.error("LLM service not available - using fallback")
            yield self._generate_fallback_response(query, context_docs, language)
            return

        try:
            logger.info(f"Generating streaming LLM response for query: {query[:100]}...")

            # Build context from retrieved documents
            context = self._build_context(context_docs)

            # Build the complete prompt with system instructions
            prompt = self._build_prompt(query, context, language, conversation_history)

            logger.info(f"Calling Gemini API for streaming...")

            # Call Gemini API with streaming
            response = await self.model.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.8,
                    max_output_tokens=1024,
                    top_p=0.9,
                ),
                stream=True
            )

            # Stream the response chunks
            async for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            logger.error(f"Error generating streaming LLM response: {str(e)}", exc_info=True)
            yield self._generate_fallback_response(query, context_docs, language)

    def _build_context(self, docs: List[Dict]) -> str:
        """
        Build context string from retrieved documents

        Args:
            docs: List of document dictionaries with scripture info

        Returns:
            Formatted context string
        """
        if not docs:
            return "No specific scripture found for this query."

        context_parts = []
        for i, doc in enumerate(docs, 1):
            scripture = doc.get('scripture', 'Unknown')
            reference = doc.get('reference', '')
            text = doc.get('text', '')
            topic = doc.get('topic', '')

            context_parts.append(f"""
Scripture {i}:
- Source: {scripture} {reference}
- Topic: {topic}
- Verse: "{text}"
""")

        return "\n".join(context_parts)

    def _build_prompt(
        self,
        query: str,
        context: str,
        language: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Build the complete prompt with system instructions and context

        Args:
            query: User's question
            context: Retrieved scripture context
            language: Language code
            conversation_history: Optional chat history

        Returns:
            Formatted prompt string
        """
        lang_instruction = ""
        if language == "hi":
            lang_instruction = "\n\nIMPORTANT: Respond in Hindi (Devanagari script)."

        # Build conversation history if provided
        history_text = ""
        if conversation_history and len(conversation_history) > 0:
            history_text = "\n\nPrevious Conversation:\n"
            # Include last 6 messages for context (last 3 exchanges)
            recent_history = conversation_history[-6:] if len(conversation_history) > 6 else conversation_history
            for msg in recent_history:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                history_text += f"{'User' if role == 'user' else 'You'}: {content}\n"
            history_text += "\nRemember what the user has shared and build on it naturally.\n"

        # Simple instruction - always provide Bhagavad Gita wisdom
        stage_guidance = "\n\n🕉️ RESPOND AS A BHAGAVAD GITA GURU:\nYou must IMMEDIATELY share relevant Bhagavad Gita verses from the context provided below. Do not give generic advice. Quote Krishna's exact words to Arjuna and explain their meaning."

        # Context handling - STRICT mode
        context_note = ""
        if context and "No specific scripture" not in context:
            context_note = f"""

📿 SACRED BHAGAVAD GITA VERSES - USE THESE EXACT VERSES:
{context}

⚠️ CRITICAL INSTRUCTIONS - DO NOT VIOLATE:
1. You MUST quote AT LEAST ONE of these verses word-for-word
2. You MUST cite it as "In Bhagavad Gita [Chapter].[Verse], Krishna says: [EXACT TEXT]"
3. You MUST explain what Krishna was teaching Arjuna
4. DO NOT make up your own teachings or use knowledge outside these verses
5. If these verses don't match the query, say "Let me find the right teaching" instead of making things up

THESE ARE THE ONLY VERSES YOU CAN USE. DO NOT HALLUCINATE OR CREATE TEACHINGS."""
        else:
            context_note = "\n\n⚠️ NO BHAGAVAD GITA VERSES FOUND IN CONTEXT.\nYou must say: 'I apologize, but I need to find the right verse from the Bhagavad Gita for your question. Could you rephrase what you're seeking guidance on?' DO NOT give generic advice."

        prompt = f"""{settings.SYSTEM_PROMPT}
{lang_instruction}
{history_text}
{stage_guidance}
{context_note}

Current User Message: {query}

🚨 CRITICAL FORMATTING RULES - YOU MUST FOLLOW EXACTLY:

1. AFTER EVERY 2-3 SENTENCES, YOU MUST ADD TWO NEWLINE CHARACTERS (\\n\\n)
2. Each paragraph = 2-3 sentences MAXIMUM, then \\n\\n
3. When quoting a verse, put it in its own paragraph with \\n\\n before and after
4. NO long blocks of text - they are unreadable
5. NO asterisks (*word*) or markdown **bold**
6. Proper spaces between all words

YOUR RESPONSE MUST LOOK EXACTLY LIKE THIS:

"Brief acknowledgment sentence. Perhaps one more sentence.\\n\\nIn Bhagavad Gita 3.22, Krishna says: 'Quote the verse here.'\\n\\nExplanation of what this means. Another sentence about the teaching.\\n\\nHow this applies to their life. Final thought.\\n\\nA question to engage them?"

WRONG - DO NOT DO THIS (no line breaks):
"Brief acknowledgment. In Bhagavad Gita 3.22, Krishna says: 'Quote.' Explanation here. Application here. Question?"

RIGHT - DO THIS (with line breaks):
"Brief acknowledgment.\\n\\nIn Bhagavad Gita 3.22, Krishna says: 'Quote.'\\n\\nExplanation here.\\n\\nApplication here.\\n\\nQuestion?"

REMEMBER: Every 2-3 sentences, add \\n\\n (blank line). No exceptions!"""

        return prompt

    def _generate_fallback_response(
        self,
        query: str,
        context_docs: List[Dict],
        language: str
    ) -> str:
        """
        Generate a simple fallback response when LLM is unavailable

        Args:
            query: User's question
            context_docs: Retrieved documents
            language: Language code

        Returns:
            Fallback response text
        """
        if not context_docs:
            if language == "hi":
                return "क्षमा करें, मुझे आपके प्रश्न के लिए कोई प्रासंगिक शास्त्र नहीं मिला।"
            return "I couldn't find a relevant scripture for your question."

        doc = context_docs[0]
        scripture = doc.get('scripture', 'Scripture')
        reference = doc.get('reference', '')
        text = doc.get('text', '')

        if language == "hi":
            return f"""नमस्ते! आपके प्रश्न के संदर्भ में, {scripture} {reference} में कहा गया है:

"{text}"

यह श्लोक आपके प्रश्न से संबंधित है। अधिक विस्तृत जानकारी के लिए, कृपया GEMINI_API_KEY सेट करें।"""

        return f"""Hey! Regarding your question, {scripture} {reference} says:

"{text}"

This verse relates to your question. For more detailed explanations, please set up your GEMINI_API_KEY."""


# Singleton instance
_llm_service = None


def get_llm_service() -> LLMService:
    """Get or create LLM service singleton"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
