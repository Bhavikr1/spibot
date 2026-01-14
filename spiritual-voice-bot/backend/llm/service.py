"""
LLM Service for conversational response generation using Anthropic Claude
"""
import logging
from typing import List, Dict, Optional
from config import settings

logger = logging.getLogger(__name__)

# Try to import Anthropic SDK
try:
    from anthropic import AsyncAnthropic
    ANTHROPIC_AVAILABLE = True
    logger.info("Anthropic SDK loaded successfully")
except Exception as e:
    AsyncAnthropic = None
    ANTHROPIC_AVAILABLE = False
    logger.error(f"Failed to import Anthropic SDK: {str(e)}. Install with: pip install anthropic")


class LLMService:
    """
    LLM service for generating conversational responses using Claude
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize LLM service

        Args:
            api_key: Anthropic API key (if not provided, uses env variable)
        """
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.client = None
        self.available = False

        if not ANTHROPIC_AVAILABLE:
            logger.error("Anthropic SDK not available - install with: pip install anthropic")
            return

        if not self.api_key:
            logger.warning("ANTHROPIC_API_KEY not set - LLM responses will use fallback templates")
            return

        try:
            self.client = AsyncAnthropic(api_key=self.api_key)
            self.available = True
            logger.info("LLM service initialized with Claude")
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {str(e)}")

    async def generate_response(
        self,
        query: str,
        context_docs: List[Dict],
        language: str = "en",
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate conversational response using Claude with RAG context

        Args:
            query: User's question
            context_docs: Retrieved scripture documents with metadata
            language: Language code (en or hi)
            conversation_history: Optional chat history for context

        Returns:
            Generated response text
        """
        if not self.available or not self.client:
            logger.error("LLM service not available - using fallback")
            return self._generate_fallback_response(query, context_docs, language)

        try:
            logger.info(f"Generating LLM response for query: {query[:100]}...")

            # Build context from retrieved documents
            context = self._build_context(context_docs)

            # Build user message
            user_message = self._build_user_message(query, context, language)

            # Build messages array
            messages = []

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)

            # Add current query
            messages.append({
                "role": "user",
                "content": user_message
            })

            logger.info(f"Calling Claude API with {len(messages)} messages...")

            # Call Claude API
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Latest Claude model
                max_tokens=1024,
                temperature=0.7,
                system=settings.SYSTEM_PROMPT,
                messages=messages
            )

            # Extract response text
            response_text = response.content[0].text

            logger.info(f"Generated response length: {len(response_text)} chars")

            return response_text

        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}", exc_info=True)
            return self._generate_fallback_response(query, context_docs, language)

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

    def _build_user_message(self, query: str, context: str, language: str) -> str:
        """
        Build the user message with query and context

        Args:
            query: User's question
            context: Retrieved scripture context
            language: Language code

        Returns:
            Formatted user message
        """
        lang_instruction = ""
        if language == "hi":
            lang_instruction = "\n\nPlease respond in Hindi (Devanagari script)."

        return f"""User's Question: {query}

Relevant Scriptures:
{context}

Please provide a conversational, friendly response that:
1. References the most relevant scripture verse provided above
2. Explains the wisdom in modern, relatable language
3. Connects it to the user's specific question
4. Keeps the tone warm and conversational{lang_instruction}"""

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

यह श्लोक आपके प्रश्न से संबंधित है। अधिक विस्तृत जानकारी के लिए, कृपया ANTHROPIC_API_KEY सेट करें।"""

        return f"""Hey! Regarding your question, {scripture} {reference} says:

"{text}"

This verse relates to your question. For more detailed explanations, please set up your ANTHROPIC_API_KEY."""


# Singleton instance
_llm_service = None


def get_llm_service() -> LLMService:
    """Get or create LLM service singleton"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
