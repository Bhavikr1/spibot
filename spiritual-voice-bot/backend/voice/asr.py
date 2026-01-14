"""
Automatic Speech Recognition (ASR) using Whisper
"""
import numpy as np
import io
import logging
from pydub import AudioSegment

from config import settings

logger = logging.getLogger(__name__)

# Try to import heavy ASR deps; otherwise provide a dummy fallback
try:
    import torch
    import whisper
    ASR_AVAILABLE = True
    logger.info("Whisper library loaded successfully")
except Exception as e:
    torch = None
    whisper = None
    ASR_AVAILABLE = False
    logger.error(f"Failed to import Whisper: {str(e)}. Install with: pip install openai-whisper")


class ASRProcessor:
    """
    ASR processor wrapper: uses Whisper when available, otherwise dummy implementation
    """

    def __init__(self):
        self.model = None
        if ASR_AVAILABLE and torch is not None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = "cpu"

        # Auto-initialize if available
        if ASR_AVAILABLE:
            logger.info("ASR is available, will initialize on first use")

    async def initialize(self):
        """Load Whisper model"""
        if not ASR_AVAILABLE:
            logger.warning("Whisper not available; ASR functionality is disabled in lightweight mode")
            return

        try:
            logger.info(f"Loading Whisper model on {self.device}...")
            # Use base model for POC
            self.model = whisper.load_model("base", device=self.device)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {str(e)}")
            raise

    async def transcribe(
        self,
        audio_bytes: bytes,
        language: str = "en"
    ) -> str:
        """
        Transcribe audio to text. If Whisper not available, returns a descriptive placeholder.
        """
        if not ASR_AVAILABLE:
            logger.error("ASR_AVAILABLE is False - Whisper library not loaded. Please install: pip install openai-whisper")
            return "[ASR disabled in lightweight mode]"

        try:
            logger.info(f"Starting transcription - audio size: {len(audio_bytes)} bytes, language: {language}")

            # Load model if not loaded
            if self.model is None:
                logger.info("Model not loaded, initializing...")
                await self.initialize()

            # Convert audio bytes to numpy array
            logger.info("Converting audio bytes to numpy array...")
            audio = self._audio_bytes_to_array(audio_bytes)
            logger.info(f"Audio array shape: {audio.shape}, dtype: {audio.dtype}")

            # Transcribe
            logger.info(f"Running Whisper transcription on {self.device}...")
            result = self.model.transcribe(
                audio,
                language=language if language == "hi" else "en",
                task="transcribe",
                fp16=torch.cuda.is_available() if torch else False
            )

            transcription = result["text"].strip()
            logger.info(f"Transcription complete: '{transcription[:100]}...' (length: {len(transcription)} chars)")

            return transcription

        except Exception as e:
            logger.error(f"Transcription error: {str(e)}", exc_info=True)
            raise

    def _audio_bytes_to_array(self, audio_bytes: bytes) -> np.ndarray:
        """
        Convert audio bytes to numpy array for Whisper

        Args:
            audio_bytes: Audio file bytes

        Returns:
            Numpy array (mono, 16kHz)
        """
        try:
            # Load audio using pydub
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))

            # Convert to mono
            audio_segment = audio_segment.set_channels(1)

            # Resample to 16kHz (Whisper requirement)
            audio_segment = audio_segment.set_frame_rate(16000)

            # Convert to numpy array
            samples = np.array(audio_segment.get_array_of_samples())

            # Normalize to [-1, 1]
            samples = samples.astype(np.float32) / 32768.0

            return samples

        except Exception as e:
            logger.error(f"Audio conversion error: {str(e)}")
            raise

    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        if ASR_AVAILABLE:
            return ["en", "hi", "sa"]  # English, Hindi, Sanskrit
        return ["en"]
