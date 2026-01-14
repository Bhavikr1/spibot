"""
Text-to-Speech (TTS) using gTTS (Google Text-to-Speech)
"""
import numpy as np
import io
import logging
from pydub import AudioSegment

from config import settings

logger = logging.getLogger(__name__)

# Try to import gTTS; otherwise use a dummy fallback
try:
    from gtts import gTTS as GoogleTTS
    TTS_AVAILABLE = True
    logger.info("gTTS library loaded successfully")
except Exception as e:
    GoogleTTS = None
    TTS_AVAILABLE = False
    logger.error(f"Failed to import gTTS: {str(e)}. Install with: pip install gtts")


class TTSProcessor:
    """
    TTS processor wrapper: uses gTTS if available, otherwise a dummy implementation
    """

    def __init__(self):
        self.initialized = False

        # Auto-initialize if available
        if TTS_AVAILABLE:
            logger.info("gTTS is available and ready to use")
            self.initialized = True
        else:
            logger.warning("gTTS not available; speech synthesis is disabled")

    async def initialize(self):
        """Initialize TTS (gTTS doesn't need initialization)"""
        if not TTS_AVAILABLE:
            logger.warning("TTS not available; speech synthesis is disabled in lightweight mode")
            return

        logger.info("gTTS initialized successfully")
        self.initialized = True

    async def synthesize(
        self,
        text: str,
        language: str = "en",
        speaker: str = None
    ) -> bytes:
        """
        Convert text to speech using gTTS. If TTS is not available, returns a short beep audio.
        """
        if not TTS_AVAILABLE:
            logger.error("TTS_AVAILABLE is False - gTTS library not loaded. Please install: pip install gtts")
            return self._generate_error_audio()

        if not self.initialized:
            logger.error("TTS not initialized - call initialize() first")
            return self._generate_error_audio()

        try:
            logger.info(f"Synthesizing speech for text (length: {len(text)} chars): {text[:50]}...")

            # Map language codes (gTTS uses 'hi' for Hindi, 'en' for English)
            lang_code = 'hi' if language == 'hi' else 'en'
            logger.info(f"Using language code: {lang_code}")

            # Generate speech using gTTS
            tts = GoogleTTS(text=text, lang=lang_code, slow=False)

            # Save to BytesIO buffer
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            logger.info(f"Generated MP3 audio: {len(mp3_fp.getvalue())} bytes")

            # Convert MP3 to WAV format for consistency
            audio_segment = AudioSegment.from_mp3(mp3_fp)
            logger.info(f"Converted to AudioSegment: duration={len(audio_segment)}ms")

            # Export as WAV
            wav_fp = io.BytesIO()
            audio_segment.export(wav_fp, format="wav")
            wav_fp.seek(0)

            audio_bytes = wav_fp.read()
            logger.info(f"Speech synthesis complete - generated {len(audio_bytes)} bytes of WAV audio")
            return audio_bytes

        except Exception as e:
            logger.error(f"TTS error during synthesis: {str(e)}", exc_info=True)
            # Return simple error message as audio
            return self._generate_error_audio()

    def _array_to_audio_bytes(self, wav: np.ndarray, sample_rate: int = 22050) -> bytes:
        """
        Convert numpy array to audio bytes (WAV format)

        Args:
            wav: Audio waveform as numpy array
            sample_rate: Sample rate in Hz

        Returns:
            Audio bytes in WAV format
        """
        try:
            # Ensure wav is numpy array
            if isinstance(wav, list):
                wav = np.array(wav)

            # Normalize to int16 range
            wav = np.clip(wav, -1, 1)
            wav = (wav * 32767).astype(np.int16)

            # Create audio segment
            audio_segment = AudioSegment(
                wav.tobytes(),
                frame_rate=sample_rate,
                sample_width=2,  # 16-bit
                channels=1  # mono
            )

            # Export to bytes
            buffer = io.BytesIO()
            audio_segment.export(buffer, format="wav")
            buffer.seek(0)

            return buffer.read()

        except Exception as e:
            logger.error(f"Audio conversion error: {str(e)}")
            raise

    def _generate_error_audio(self) -> bytes:
        """Generate simple error message audio"""
        try:
            # Generate a simple sine wave beep as error indicator
            sample_rate = 22050
            duration = 0.3  # seconds
            frequency = 440  # Hz (A4 note)

            t = np.linspace(0, duration, int(sample_rate * duration))
            wav = np.sin(2 * np.pi * frequency * t) * 0.3

            return self._array_to_audio_bytes(wav, sample_rate)

        except:
            # Return empty audio
            return b""

    def get_available_speakers(self) -> list:
        """Get list of available speakers"""
        if TTS_AVAILABLE and self.model and hasattr(self.model, 'speakers'):
            return self.model.speakers
        return []

    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return ["en", "hi"]  # English, Hindi
