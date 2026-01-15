"""
Main FastAPI application for Spiritual Voice Bot
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import io
import json
import logging

from config import settings
from rag.pipeline import RAGPipeline
from voice.asr import ASRProcessor
from voice.tts import TTSProcessor
from llm.service import get_llm_service
from llm.formatter import get_refiner, get_reformatter

# Setup logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Voice-enabled conversational AI for Sanatan Dharma"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Transcription", "X-Citations"]  # Expose custom headers
)

# Initialize components
rag_pipeline: Optional[RAGPipeline] = None
asr_processor: Optional[ASRProcessor] = None
tts_processor: Optional[TTSProcessor] = None


# Pydantic models
class TextQuery(BaseModel):
    query: str
    language: str = "en"
    include_citations: bool = True
    conversation_history: Optional[List[dict]] = None


class TextResponse(BaseModel):
    answer: str
    citations: List[dict]
    language: str
    confidence: float


@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    global rag_pipeline, asr_processor, tts_processor

    logger.info("Starting Spiritual Voice Bot API...")

    try:
        # Initialize RAG Pipeline
        logger.info("Initializing RAG Pipeline...")
        rag_pipeline = RAGPipeline()
        await rag_pipeline.initialize()

        # Initialize ASR
        logger.info("Initializing ASR...")
        asr_processor = ASRProcessor()
        try:
            await asr_processor.initialize()
            logger.info("ASR initialized successfully")
        except Exception as e:
            logger.warning(f"ASR initialization failed (will use fallback): {str(e)}")

        # Initialize TTS
        logger.info("Initializing TTS...")
        tts_processor = TTSProcessor()
        try:
            await tts_processor.initialize()
            logger.info("TTS initialized successfully")
        except Exception as e:
            logger.warning(f"TTS initialization failed (will use fallback): {str(e)}")

        # Initialize LLM Service
        logger.info("Initializing LLM Service...")
        llm_service = get_llm_service()
        if llm_service.available:
            logger.info("LLM Service initialized successfully with Gemini")
        else:
            logger.warning("LLM Service not available - will use fallback templates. Set GEMINI_API_KEY to enable.")

        # Initialize Query Refiner
        logger.info("Initializing Query Refiner...")
        refiner = get_refiner(settings.GEMINI_API_KEY)
        if refiner and refiner.available:
            logger.info("Query Refiner initialized successfully")
        else:
            logger.warning("Query Refiner not available")

        # Initialize Response Reformatter
        logger.info("Initializing Response Reformatter...")
        reformatter = get_reformatter(settings.GEMINI_API_KEY)
        if reformatter and reformatter.available:
            logger.info("Response Reformatter initialized successfully")
        else:
            logger.warning("Response Reformatter not available")

        logger.info("All components initialized successfully!")

    except Exception as e:
        logger.error(f"Failed to initialize components: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Spiritual Voice Bot API...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Spiritual Voice Bot API",
        "version": settings.API_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "components": {
            "rag": rag_pipeline is not None,
            "asr": asr_processor is not None,
            "tts": tts_processor is not None
        }
    }


@app.post("/api/text/query", response_model=TextResponse)
async def text_query(query: TextQuery):
    """
    Process text query and return text response with citations
    """
    try:
        if not rag_pipeline:
            raise HTTPException(status_code=500, detail="RAG pipeline not initialized")

        logger.info(f"Processing text query: {query.query[:50]}...")

        # Get response from RAG pipeline with conversation history
        result = await rag_pipeline.query(
            query=query.query,
            language=query.language,
            include_citations=query.include_citations,
            conversation_history=query.conversation_history
        )

        return TextResponse(
            answer=result["answer"],
            citations=result["citations"],
            language=query.language,
            confidence=result["confidence"]
        )

    except Exception as e:
        logger.error(f"Error processing text query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/text/query/stream")
async def text_query_stream(query: TextQuery):
    """
    Process text query and return streaming text response
    """
    try:
        if not rag_pipeline:
            raise HTTPException(status_code=500, detail="RAG pipeline not initialized")

        logger.info(f"Processing streaming text query: {query.query[:50]}...")

        async def generate_stream():
            try:
                # Stream response from RAG pipeline with conversation history
                async for chunk in rag_pipeline.query_stream(
                    query=query.query,
                    language=query.language,
                    include_citations=query.include_citations,
                    conversation_history=query.conversation_history
                ):
                    # For SSE format, we need to escape newlines in the chunk
                    # because \n\n terminates an SSE event
                    # Replace actual newlines with escaped newlines for JSON compatibility
                    import json
                    # JSON encode the chunk to escape special characters
                    chunk_escaped = json.dumps(chunk)
                    # Send as Server-Sent Events format
                    yield f"data: {chunk_escaped}\n\n"
            except Exception as e:
                logger.error(f"Error in stream generation: {str(e)}")
                yield f"data: [ERROR] {str(e)}\n\n"

        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )

    except Exception as e:
        logger.error(f"Error processing streaming text query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/voice/query")
async def voice_query(
    audio: UploadFile = File(...),
    language: str = Form("en")
):
    """
    Process voice query and return voice response
    """
    try:
        if not all([rag_pipeline, asr_processor, tts_processor]):
            raise HTTPException(status_code=500, detail="Components not initialized")

        logger.info(f"Processing voice query in {language}...")

        # Read audio file
        audio_bytes = await audio.read()

        # Transcribe audio to text
        logger.info("Transcribing audio...")
        transcription = await asr_processor.transcribe(audio_bytes, language)
        logger.info(f"Transcription: {transcription[:100]}...")

        # Get response from RAG pipeline
        logger.info("Getting RAG response...")
        result = await rag_pipeline.query(
            query=transcription,
            language=language,
            include_citations=True
        )

        # Convert response to speech
        logger.info("Generating speech...")
        audio_response = await tts_processor.synthesize(
            text=result["answer"],
            language=language
        )

        # Return audio response
        return StreamingResponse(
            io.BytesIO(audio_response),
            media_type="audio/wav",
            headers={
                "X-Transcription": transcription,
                "X-Citations": str(result["citations"])
            }
        )

    except Exception as e:
        logger.error(f"Error processing voice query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/scripture/search")
async def search_scripture(
    query: str,
    scripture: Optional[str] = None,
    language: str = "en",
    limit: int = 5
):
    """
    Search scriptures directly
    """
    try:
        if not rag_pipeline:
            raise HTTPException(status_code=500, detail="RAG pipeline not initialized")

        results = await rag_pipeline.search(
            query=query,
            scripture_filter=scripture,
            language=language,
            top_k=limit
        )

        return {
            "query": query,
            "results": results,
            "count": len(results)
        }

    except Exception as e:
        logger.error(f"Error searching scripture: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/embeddings/generate")
async def generate_embeddings(text: str):
    """
    Generate embeddings for text (utility endpoint)
    """
    try:
        if not rag_pipeline:
            raise HTTPException(status_code=500, detail="RAG pipeline not initialized")

        embeddings = await rag_pipeline.generate_embeddings(text)

        return {
            "text": text,
            "embeddings": embeddings.tolist(),
            "dimension": len(embeddings)
        }

    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
