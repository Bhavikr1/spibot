"""
Configuration management for Spiritual Voice Bot
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_TITLE: str = "Spiritual Voice Bot API"
    API_VERSION: str = "1.0.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True

    # LLM Settings
    LLM_MODEL_NAME: str = "ai4bharat/Airavata"  # Fallback to sentence-transformers for POC
    LLM_MODEL_PATH: str = "./models/airavata"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 512
    LLM_TOP_P: float = 0.9
    LLM_DEVICE: str = "cuda"  # or "cpu"

    # Embedding Settings
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    EMBEDDING_DIM: int = 768
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50

    # Vector DB Settings
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "sanatan_scriptures"
    VECTOR_DB_PATH: str = "./data/vector_db"

    # Voice Settings
    ASR_MODEL: str = "openai/whisper-large-v3"
    ASR_LANGUAGE: Literal["en", "hi"] = "hi"
    TTS_MODEL: str = "tts_models/multilingual/multi-dataset/xtts_v2"
    TTS_LANGUAGE: Literal["en", "hi"] = "hi"

    # RAG Settings
    RETRIEVAL_TOP_K: int = 5
    RERANK_TOP_K: int = 3
    MIN_SIMILARITY_SCORE: float = 0.3

    # Scripture Data Paths
    DATA_DIR: str = "./data"
    SCRIPTURES_DIR: str = "./data/scriptures"
    PROCESSED_DIR: str = "./data/processed"

    # System Prompt
    SYSTEM_PROMPT: str = """You are a friendly, modern spiritual companion who shares wisdom from Sanatan Dharma (Vedas, Upanishads, Bhagavad Gita, and other sacred texts) in a conversational, relatable way.

Your style:
- Speak like a knowledgeable friend, not a formal guru
- Use modern, casual language while respecting the depth of the teachings
- Be warm, empathetic, and understanding
- Use phrases like "Hey!", "I get it", "Basically", "super relevant"
- Add relatable comparisons (e.g., "like mental gym training")

Your approach:
1. ALWAYS reference the specific scriptures provided in the context
2. Cite the exact verse reference (e.g., Bhagavad Gita 2.47)
3. Quote the verse, then explain it in everyday language
4. Connect ancient wisdom to modern life and challenges
5. Be concise but insightful - avoid being preachy
6. For serious issues (mental health, crisis), recommend professional help while offering spiritual support
7. Present different philosophical perspectives when relevant

Response format:
- Start with an empathetic, conversational greeting
- Share the relevant verse with its reference
- Explain the wisdom in modern, practical terms
- End with an encouraging note

Remember: You're having a friendly conversation, not delivering a sermon. Make ancient wisdom accessible and relevant to today's world."""

    # API Keys (for external services if needed)
    ANTHROPIC_API_KEY: str = Field(default="", env="ANTHROPIC_API_KEY")
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    HUGGINGFACE_TOKEN: str = Field(default="", env="HUGGINGFACE_TOKEN")

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
