"""
PersonaWrite AI — Voice Assistant Module (v2)

STT: OpenAI Whisper (local model, high accuracy, no random tokens)
TTS: gTTS → in-memory MP3 bytes for Streamlit st.audio() playback

Completely decoupled from Streamlit — no UI logic here.
"""

import re
import numpy as np
import sounddevice as sd
import whisper


# ===================== WHISPER MODEL (LAZY SINGLETON) =====================

_whisper_model = None


def _get_whisper_model(model_name: str = "base"):
    """
    Load Whisper model once and cache it for the process lifetime.
    Uses 'base' by default — good accuracy, fast on M1/M2 Mac.
    """
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model(model_name)
    return _whisper_model


# ===================== MICROPHONE RECORDING =====================

def record_audio(duration: int = 8, sample_rate: int = 16000) -> np.ndarray:
    """
    Record audio from the default microphone.

    Args:
        duration: Recording length in seconds.
        sample_rate: Sample rate (Whisper expects 16 kHz).

    Returns:
        Numpy float32 array of audio samples (mono, 1D).
    """
    # Record as float32 mono
    audio_data = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
    )
    sd.wait()  # Block until recording finishes

    # Flatten to 1D (Whisper expects shape (N,) not (N,1))
    return audio_data.flatten()


# ===================== WHISPER TRANSCRIPTION =====================

def transcribe(audio: np.ndarray) -> str:
    """
    Transcribe audio using OpenAI Whisper.

    Args:
        audio: Float32 numpy array of audio samples at 16 kHz.

    Returns:
        Raw transcription text.
    """
    model = _get_whisper_model()
    # Pass numpy array directly — no ffmpeg needed
    result = model.transcribe(audio, fp16=False, language="en")
    return result.get("text", "").strip()


# ===================== FULL LISTEN PIPELINE =====================

def listen_speech(duration: int = 8) -> str:
    """
    Full pipeline: record → transcribe with Whisper → clean text.

    Args:
        duration: Recording length in seconds.

    Returns:
        Cleaned transcription, or empty string on any failure.
    """
    try:
        audio = record_audio(duration=duration)
        raw_text = transcribe(audio)
        return clean_text(raw_text)
    except Exception:
        return ""


# ===================== TEXT CLEANING =====================

def clean_text(raw: str) -> str:
    """
    Remove speech-recognition noise artifacts from transcribed text.

    Handles:
      - Stray dimensional tokens: "1D", "2D", "3D"
      - Isolated single characters/digits
      - Repeated punctuation or random symbols
      - Extra whitespace
    """
    if not raw:
        return ""

    # Remove tokens like "1D", "2D", "3D" (case-insensitive)
    cleaned = re.sub(r'\b\d+[dD]\b', '', raw)

    # Remove isolated single digits
    cleaned = re.sub(r'\b\d\b', '', cleaned)

    # Remove isolated single letters (except "I" and "A")
    cleaned = re.sub(r'\b(?![IAia])[a-zA-Z]\b', '', cleaned)

    # Remove stray symbols that aren't normal punctuation
    cleaned = re.sub(r'[^\w\s.,!?\'"-]', '', cleaned)

    # Collapse multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned